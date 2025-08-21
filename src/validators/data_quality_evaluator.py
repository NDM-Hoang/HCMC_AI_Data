#!/usr/bin/env python3
"""
Data Quality Evaluator

Checks:
- Validate required fields in media-info JSON files
- Verify mapping between keyframes, objects, and map-keyframes CSV
- Draw object bounding boxes on keyframe images and overlay fps + pts_time

Outputs:
- JSON summary at reports/data_quality_evaluation_results.json
- Annotated images under reports/data_quality_evaluation/overlays/<video_name>/
"""

import json
import csv
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
import random
import shutil

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False


@dataclass
class MediaInfoCheckResult:
    total_files: int = 0
    valid_count: int = 0
    invalid_count: int = 0
    missing_fields_by_file: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class FrameOverlayResult:
    keyframe: str
    objects_file: Optional[str]
    map_row_found: bool
    match_by_n: bool
    match_by_frame_idx: bool
    fps: Optional[float]
    pts_time: Optional[float]
    overlay_path: Optional[str]
    error: Optional[str] = None


@dataclass
class VideoEvaluationResult:
    video_name: str
    processed_frames: int = 0
    frame_results: List[FrameOverlayResult] = field(default_factory=list)


class DataQualityEvaluator:
    REQUIRED_MEDIA_FIELDS = [
        'title', 'publish_date', 'watch_url', 'leght', 'description', 'author', 'thumbnail_url'
    ]

    def __init__(self, data_path: str, output_root: str = 'reports/data_quality_evaluation'):
        self.data_path = Path(data_path)
        self.output_root = Path(output_root)
        self.output_overlays = self.output_root / 'overlays'
        self.output_annotated = self.output_root / 'annotated_keyframes'
        # Directories created lazily only if saving is enabled

    def _iter_media_info_files(self) -> List[Path]:
        media_dir = self.data_path / 'media-info'
        return sorted(media_dir.glob('*.json')) if media_dir.exists() else []

    def _iter_map_files(self) -> Dict[str, Path]:
        maps_dir = self.data_path / 'map-keyframes'
        if not maps_dir.exists():
            return {}
        return {f.stem: f for f in maps_dir.glob('*.csv')}

    def _iter_keyframe_dirs(self) -> Dict[str, Path]:
        keyframes_dir = self.data_path / 'keyframes'
        if not keyframes_dir.exists():
            return {}
        return {d.name: d for d in keyframes_dir.iterdir() if d.is_dir() and d.name.startswith('L')}

    def _iter_object_dirs(self) -> Dict[str, Path]:
        objects_dir = self.data_path / 'objects'
        if not objects_dir.exists():
            return {}
        return {d.name: d for d in objects_dir.iterdir() if d.is_dir() and d.name.startswith('L')}

    def verify_media_info_fields(self) -> MediaInfoCheckResult:
        result = MediaInfoCheckResult()
        json_files = self._iter_media_info_files()
        result.total_files = len(json_files)

        for jf in json_files:
            try:
                with open(jf, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                missing = []
                for field_name in self.REQUIRED_MEDIA_FIELDS:
                    if not isinstance(data, dict) or field_name not in data or data[field_name] in (None, ''):
                        missing.append(field_name)
                if missing:
                    result.invalid_count += 1
                    result.missing_fields_by_file[jf.name] = missing
                else:
                    result.valid_count += 1
            except Exception as e:
                result.invalid_count += 1
                result.missing_fields_by_file[jf.name] = [f'error: {e}']

        return result

    def _read_map_csv(self, csv_path: Path) -> Tuple[Dict[int, Dict[str, Any]], Dict[int, Dict[str, Any]]]:
        by_n: Dict[int, Dict[str, Any]] = {}
        by_frame_idx: Dict[int, Dict[str, Any]] = {}
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        n_val = int(row.get('n', '').strip()) if row.get('n') not in (None, '') else None
                    except Exception:
                        n_val = None
                    try:
                        fidx = int(row.get('frame_idx', '').strip()) if row.get('frame_idx') not in (None, '') else None
                    except Exception:
                        fidx = None
                    try:
                        fps = float(row.get('fps', '').strip()) if row.get('fps') not in (None, '') else None
                    except Exception:
                        fps = None
                    try:
                        pts_time = float(row.get('pts_time', '').strip()) if row.get('pts_time') not in (None, '') else None
                    except Exception:
                        pts_time = None

                    info = {
                        'n': n_val,
                        'frame_idx': fidx,
                        'fps': fps,
                        'pts_time': pts_time
                    }
                    if n_val is not None:
                        by_n[n_val] = info
                    if fidx is not None:
                        by_frame_idx[fidx] = info
        except Exception:
            pass

        return by_n, by_frame_idx

    def _parse_objects(self, objects_path: Optional[Path], image_path: Path, min_score: float = 0.3) -> Tuple[List[Tuple[int, int, int, int]], List[str]]:
        bboxes: List[Tuple[int, int, int, int]] = []
        labels: List[str] = []
        if objects_path is None or not objects_path.exists():
            return bboxes, labels
        try:
            with open(objects_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            return bboxes, labels

        # OpenImages-like parallel arrays: normalized boxes [ymin,xmin,ymax,xmax]
        if isinstance(data, dict) and all(k in data for k in ['detection_boxes', 'detection_class_entities', 'detection_scores']):
            try:
                if not PIL_AVAILABLE:
                    return bboxes, labels
                img = Image.open(image_path).convert('RGB')
                width, height = img.size
                img.close()

                boxes = data.get('detection_boxes') or []
                classes = data.get('detection_class_entities') or []
                scores = data.get('detection_scores') or []
                n = min(len(boxes), len(classes), len(scores))
                for i in range(n):
                    try:
                        s = float(scores[i])
                    except Exception:
                        s = 0.0
                    if s < min_score:
                        continue
                    box = boxes[i]
                    if isinstance(box, (list, tuple)) and len(box) == 4:
                        try:
                            y_min = float(box[0]); x_min = float(box[1]); y_max = float(box[2]); x_max = float(box[3])
                        except Exception:
                            continue
                        x1 = max(0, min(int(round(x_min * width)), width - 1))
                        y1 = max(0, min(int(round(y_min * height)), height - 1))
                        x2 = max(0, min(int(round(x_max * width)), width - 1))
                        y2 = max(0, min(int(round(y_max * height)), height - 1))
                        x = x1; y = y1; w = max(0, x2 - x1); h = max(0, y2 - y1)
                        if w > 1 and h > 1:
                            bboxes.append((x, y, w, h))
                            labels.append(str(classes[i]))
                return bboxes, labels
            except Exception:
                # fall through
                pass

        # Generic list-of-dicts formats
        candidates: List[Dict[str, Any]]
        if isinstance(data, list):
            candidates = data
        elif isinstance(data, dict):
            for key in ['objects', 'detections', 'items', 'annotations', 'labels']:
                if isinstance(data.get(key), list):
                    candidates = data[key]
                    break
            else:
                candidates = []
        else:
            candidates = []

        def clamp_int(v: Any, default: int = 0) -> int:
            try:
                return int(round(float(v)))
            except Exception:
                return default

        for item in candidates:
            if not isinstance(item, dict):
                continue
            lbl = str(item.get('label') or item.get('class') or '')
            if 'bbox' in item and isinstance(item['bbox'], (list, tuple)) and len(item['bbox']) == 4:
                x, y, w, h = item['bbox']
                bboxes.append((clamp_int(x), clamp_int(y), clamp_int(w), clamp_int(h)))
                labels.append(lbl)
                continue
            if all(k in item for k in ['x', 'y', 'w', 'h']):
                bboxes.append((clamp_int(item['x']), clamp_int(item['y']), clamp_int(item['w']), clamp_int(item['h'])))
                labels.append(lbl)
                continue
            if all(k in item for k in ['left', 'top', 'width', 'height']):
                bboxes.append((clamp_int(item['left']), clamp_int(item['top']), clamp_int(item['width']), clamp_int(item['height'])))
                labels.append(lbl)
                continue
            if all(k in item for k in ['x1', 'y1', 'x2', 'y2']):
                x1, y1, x2, y2 = (clamp_int(item['x1']), clamp_int(item['y1']), clamp_int(item['x2']), clamp_int(item['y2']))
                bboxes.append((x1, y1, max(0, x2 - x1), max(0, y2 - y1)))
                labels.append(lbl)
                continue

        return bboxes, labels

    def _render_overlay_image(self, image_path: Path, bboxes: List[Tuple[int, int, int, int]],
                              frame_number: Optional[int], time_sec: Optional[float],
                              write_note_if_empty: bool = True, labels: Optional[List[str]] = None,
                              video_name: Optional[str] = None):
        if not PIL_AVAILABLE:
            return None
        try:
            img = Image.open(image_path).convert('RGB')
            draw = ImageDraw.Draw(img)
            # try to load a default font; Pillow provides a basic font if truetype not found
            try:
                font = ImageFont.load_default()
            except Exception:
                font = None

            # color palette
            palette = [
                (255, 0, 0), (0, 200, 0), (0, 128, 255), (255, 165, 0), (186, 85, 211),
                (255, 105, 180), (50, 205, 50), (255, 215, 0), (70, 130, 180), (255, 69, 0)
            ]

            def color_for(idx: int, label: Optional[str]) -> Tuple[int, int, int]:
                if label:
                    s = sum(ord(c) for c in label)
                    return palette[s % len(palette)]
                return palette[idx % len(palette)]

            # draw boxes
            for idx, (x, y, w, h) in enumerate(bboxes):
                lbl = labels[idx] if labels and idx < len(labels) else None
                col = color_for(idx, lbl)
                draw.rectangle([x, y, x + max(0, w), y + max(0, h)], outline=col, width=3)
                if lbl:
                    label_text = str(lbl)
                    text_bg_w = 10 + 8 * len(label_text)
                    draw.rectangle([x, max(0, y - 20), x + text_bg_w, y], fill=col)
                    draw.text((x + 4, max(0, y - 18)), label_text, fill=(255, 255, 255), font=font)

            # overlay text
            text_lines = []
            if video_name:
                try:
                    vid_disp = video_name.replace('_', ' ')
                except Exception:
                    vid_disp = video_name
                text_lines.append(vid_disp)
            if frame_number is not None:
                text_lines.append(f"frame: {frame_number}")
            if time_sec is not None:
                text_lines.append(f"time: {time_sec:.3f}s")
            if write_note_if_empty and not text_lines and not bboxes:
                text_lines.append("no objects/map row")
            if text_lines:
                text = ' | '.join(text_lines)
                draw.rectangle([5, 5, 5 + 10 + 8 * len(text), 25 + 10], fill=(0, 0, 0))
                draw.text((10, 10), text, fill=(255, 255, 255), font=font)

            return img
        except Exception:
            return None

    def _draw_overlay(self, image_path: Path, bboxes: List[Tuple[int, int, int, int]],
                      frame_number: Optional[int], time_sec: Optional[float], output_path: Path,
                      write_note_if_empty: bool = True, labels: Optional[List[str]] = None,
                      video_name: Optional[str] = None) -> Optional[str]:
        img = self._render_overlay_image(image_path, bboxes, frame_number, time_sec, write_note_if_empty, labels, video_name=video_name)
        if img is None:
            return None
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(output_path)
            return str(output_path)
        except Exception:
            return None

    def evaluate(
        self,
        max_frames_per_video: int = 3,
        max_scan_frames_for_annotation: int = 50,
        min_annotated_per_video: int = 3,
        prefer_object_frames_for_overlays: bool = True,
        score_threshold: float = 0.3,
        display_only: bool = False,
        num_random_displays: int = 5,
        save_overlays: bool = True,
        cleanup_outputs: bool = True,
        save_per_video_previews: bool = False,
        save_annotated_per_video: bool = False,
        num_random_saves: int = 5
    ) -> Dict[str, Any]:
        summary: Dict[str, Any] = {
            'data_path': str(self.data_path),
            'media_info_check': {},
            'videos': {},
            'notes': [
                'display_only: if true, show random annotated frames across all videos instead of saving',
                'score_threshold filters detections by confidence'
            ]
        }

        # Optional cleanup to reduce storage
        if cleanup_outputs:
            for folder in [self.output_overlays, self.output_annotated]:
                try:
                    if folder.exists():
                        shutil.rmtree(folder)
                except Exception:
                    pass

        # 1) Media-info field validation
        media_res = self.verify_media_info_fields()
        summary['media_info_check'] = {
            'required_fields': self.REQUIRED_MEDIA_FIELDS,
            'total_files': media_res.total_files,
            'valid_count': media_res.valid_count,
            'invalid_count': media_res.invalid_count,
            'missing_fields_by_file': media_res.missing_fields_by_file
        }

        # 2) Build indices for keyframes, objects, maps
        keyframe_dirs = self._iter_keyframe_dirs()
        object_dirs = self._iter_object_dirs()
        map_files = self._iter_map_files()

        common_video_names = sorted(set(keyframe_dirs.keys()) & set(object_dirs.keys()))
        if not common_video_names:
            summary['notes'].append('No common videos between keyframes and objects found.')

        # 3) Iterate videos and produce overlays / collect display candidates
        annotated_candidates: List[Tuple[Path, List[Tuple[int,int,int,int]], List[str], Optional[int], Optional[float], str]] = []
        for video_name in common_video_names:
            video_result = VideoEvaluationResult(video_name=video_name)

            kf_dir = keyframe_dirs[video_name]
            obj_dir = object_dirs[video_name]
            map_csv = map_files.get(video_name)
            by_n, by_fidx = self._read_map_csv(map_csv) if map_csv else ({}, {})

            # collect keyframes
            keyframes = sorted(kf_dir.glob('*.jpg'))

            # choose random frames, preferring those with object json if requested
            rng = random.Random()
            frames_to_process: List[Path] = []
            if keyframes:
                if prefer_object_frames_for_overlays:
                    object_frame_candidates = []
                    non_object_candidates = []
                    for kf in keyframes:
                        stem = kf.stem
                        if (obj_dir / f"{stem}.json").exists():
                            object_frame_candidates.append(kf)
                        else:
                            non_object_candidates.append(kf)
                    take = min(max_frames_per_video, len(object_frame_candidates))
                    frames_to_process.extend(rng.sample(object_frame_candidates, take))
                    remaining = max(0, max_frames_per_video - len(frames_to_process))
                    if remaining > 0 and non_object_candidates:
                        # ensure no duplicates
                        frames_to_process.extend(rng.sample(non_object_candidates, min(remaining, len(non_object_candidates))))
                else:
                    take = min(max_frames_per_video, len(keyframes))
                    frames_to_process = rng.sample(keyframes, take)

            matched_by_n_count = 0
            matched_by_fidx_count = 0
            unmatched_count = 0

            for kf in frames_to_process:
                # Extract frame number from filename like 001.jpg → 1
                try:
                    n_from_name = int(kf.stem)
                except Exception:
                    n_from_name = None

                # Determine corresponding object file path
                obj_path = None
                if n_from_name is not None:
                    candidate = obj_dir / f"{kf.stem}.json"
                    if candidate.exists():
                        obj_path = candidate

                # Parse objects (handles OpenImages schema and generic formats)
                bboxes, labels = self._parse_objects(obj_path, kf, min_score=score_threshold) if obj_path else ([], [])

                # Map lookup
                map_row = None
                match_by_n = False
                match_by_frame_idx = False
                fps = None
                pts_time = None

                if n_from_name is not None:
                    # Try 1-based and 0-based alignments
                    candidates = [n_from_name, n_from_name - 1]
                    for c in candidates:
                        if c in by_n:
                            map_row = by_n[c]
                            match_by_n = (c == n_from_name)
                            break
                        if c in by_fidx:
                            map_row = by_fidx[c]
                            match_by_frame_idx = (c == n_from_name)
                            break

                if map_row:
                    fps = map_row.get('fps')
                    pts_time = map_row.get('pts_time')
                    if match_by_n:
                        matched_by_n_count += 1
                    elif match_by_frame_idx:
                        matched_by_fidx_count += 1
                else:
                    unmatched_count += 1

                # Determine display frame number and time
                frame_display = None
                try:
                    if map_row and map_row.get('frame_idx') is not None:
                        frame_display = int(float(map_row.get('frame_idx')))
                except Exception:
                    frame_display = None
                if frame_display is None:
                    frame_display = n_from_name
                time_display = None
                if pts_time is not None:
                    try:
                        time_display = float(pts_time)
                    except Exception:
                        time_display = None
                if time_display is None and map_row:
                    try:
                        fidx_val = map_row.get('frame_idx')
                        fps_val = map_row.get('fps')
                        if fidx_val is not None and fps_val:
                            time_display = float(fidx_val) / float(fps_val)
                    except Exception:
                        time_display = None

                # Draw overlay (only if saving per video previews)
                overlay_out = None
                error = None
                if PIL_AVAILABLE and save_overlays and save_per_video_previews:
                    self.output_root.mkdir(parents=True, exist_ok=True)
                    ov_dir = self.output_overlays / video_name
                    overlay_out = self._draw_overlay(kf, bboxes, frame_display, time_display, ov_dir / kf.name, labels=labels, video_name=video_name)
                else:
                    if not PIL_AVAILABLE:
                        error = 'Pillow not available to draw overlays. Install Pillow.'

                video_result.frame_results.append(FrameOverlayResult(
                    keyframe=str(kf),
                    objects_file=str(obj_path) if obj_path else None,
                    map_row_found=map_row is not None,
                    match_by_n=match_by_n,
                    match_by_frame_idx=match_by_frame_idx,
                    fps=fps,
                    pts_time=pts_time,
                    overlay_path=overlay_out,
                    error=error
                ))

            video_result.processed_frames = len(video_result.frame_results)
            # Second pass: collect frames that actually have signals
            annotated_collected = 0
            if PIL_AVAILABLE:
                scanned = 0
                for kf in keyframes:
                    if scanned >= max_scan_frames_for_annotation:
                        break
                    scanned += 1

                    try:
                        n_from_name = int(kf.stem)
                    except Exception:
                        n_from_name = None

                    obj_path = None
                    if n_from_name is not None:
                        candidate = obj_dir / f"{kf.stem}.json"
                        if candidate.exists():
                            obj_path = candidate

                    bboxes, labels = self._parse_objects(obj_path, kf, min_score=score_threshold) if obj_path else ([], [])

                    map_row = None
                    fps_ann = None
                    pts_ann = None
                    if n_from_name is not None:
                        for c in [n_from_name, n_from_name - 1]:
                            if c in by_n:
                                map_row = by_n[c]
                                break
                            if c in by_fidx:
                                map_row = by_fidx[c]
                                break
                    if map_row:
                        fps_ann = map_row.get('fps')
                        pts_ann = map_row.get('pts_time')

                    if bboxes or (fps_ann is not None) or (pts_ann is not None):
                        # Compute frame/time for this candidate
                        frame_disp = None
                        try:
                            if map_row and map_row.get('frame_idx') is not None:
                                frame_disp = int(float(map_row.get('frame_idx')))
                        except Exception:
                            frame_disp = None
                        if frame_disp is None:
                            frame_disp = n_from_name
                        time_disp = None
                        if pts_ann is not None:
                            try:
                                time_disp = float(pts_ann)
                            except Exception:
                                time_disp = None
                        if time_disp is None and map_row:
                            try:
                                fidx_val = map_row.get('frame_idx')
                                fps_val = map_row.get('fps')
                                if fidx_val is not None and fps_val:
                                    time_disp = float(fidx_val) / float(fps_val)
                            except Exception:
                                time_disp = None

                        # Save annotated frames only if requested per video
                        if save_overlays and save_annotated_per_video:
                            self.output_root.mkdir(parents=True, exist_ok=True)
                            ann_dir = self.output_annotated / video_name
                            self._draw_overlay(kf, bboxes, frame_disp, time_disp, ann_dir / kf.name, write_note_if_empty=False, labels=labels, video_name=video_name)
                        # Always collect for potential display
                        annotated_candidates.append((kf, bboxes, labels, frame_disp, time_disp, video_name))
                        annotated_collected += 1
                        if annotated_collected >= min_annotated_per_video:
                            break

            summary['videos'][video_name] = {
                'processed_frames': video_result.processed_frames,
                'frame_results': [r.__dict__ for r in video_result.frame_results],
                'matches': {
                    'by_n': matched_by_n_count,
                    'by_frame_idx': matched_by_fidx_count,
                    'unmatched': unmatched_count
                },
                'annotated_keyframes_saved': annotated_collected
            }

        # Display-only: show random annotated frames across all videos
        if display_only and PIL_AVAILABLE and annotated_candidates:
            rng = random.Random()
            take = min(num_random_displays, len(annotated_candidates))
            for kf, bboxes, labels, frame_disp, time_disp, video_name in rng.sample(annotated_candidates, take):
                img = self._render_overlay_image(kf, bboxes, frame_disp, time_disp, write_note_if_empty=False, labels=labels, video_name=video_name)
                if img is not None:
                    try:
                        img.show(title=f"{video_name}/{kf.name}")
                    except Exception:
                        pass

        # Save a limited number of random annotated frames as random1..N.jpg to reduce storage
        if save_overlays and PIL_AVAILABLE and annotated_candidates and num_random_saves > 0:
            rng = random.Random()
            take = min(num_random_saves, len(annotated_candidates))
            self.output_root.mkdir(parents=True, exist_ok=True)
            # Clean old per-video folders if any to save space
            if cleanup_outputs:
                for folder in [self.output_overlays, self.output_annotated]:
                    try:
                        if folder.exists():
                            shutil.rmtree(folder)
                    except Exception:
                        pass
            self.output_overlays.mkdir(parents=True, exist_ok=True)

            manifest: List[Dict[str, Any]] = []
            for idx, (kf, bboxes, labels, frame_disp, time_disp, video_name) in enumerate(rng.sample(annotated_candidates, take), start=1):
                img = self._render_overlay_image(kf, bboxes, frame_disp, time_disp, write_note_if_empty=False, labels=labels, video_name=video_name)
                if img is None:
                    continue
                out_path = self.output_overlays / f"random{idx}.jpg"
                try:
                    img.save(out_path)
                    manifest.append({
                        'output_file': str(out_path),
                        'video_name': video_name,
                        'keyframe': str(kf),
                        'frame': frame_disp,
                        'time_sec': time_disp,
                        'num_boxes': len(bboxes)
                    })
                except Exception:
                    continue

            try:
                with open(self.output_root / 'visual_annotation_results.json', 'w', encoding='utf-8') as f:
                    json.dump(manifest, f, indent=2, ensure_ascii=False)
            except Exception:
                pass

        # Save JSON summary
        out_json = self.output_root.parent / 'data_quality_evaluation_results.json'
        with open(out_json, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        # Write explanation report for frame/time calculation and L/V tracking (VN/EN)
        try:
            # compute aggregate matching counts from summary
            total_by_n = 0
            total_by_fidx = 0
            total_unmatched = 0
            total_processed_frames = 0
            for vid in summary.get('videos', {}).values():
                m = vid.get('matches', {})
                total_by_n += int(m.get('by_n', 0))
                total_by_fidx += int(m.get('by_frame_idx', 0))
                total_unmatched += int(m.get('unmatched', 0))
                total_processed_frames += int(vid.get('processed_frames', 0))

            self.output_root.mkdir(parents=True, exist_ok=True)
            explanation_path = self.output_root / 'frame_mapping_evaluation_summary.txt'
            with open(explanation_path, 'w', encoding='utf-8') as ef:
                ef.write(
                    'Frame/Time Calculation & Video Identifier Mapping (VN/EN)\n'
                    '---------------------------------------------------------\n\n'
                    'VN:\n'
                    "- Frame (frame) hiển thị lấy từ 'frame_idx' trong CSV nếu có; nếu thiếu, mới lấy từ tên file keyframe (ví dụ 001.jpg → 1).\n"
                    "- Đối sánh với CSV 'map-keyframes': ưu tiên cột n (1-based); thử 0-based (n-1); nếu vẫn không, thử 'frame_idx'.\n"
                    "- Time (time) lấy trực tiếp từ 'pts_time' nếu có; nếu không, tính time = frame_idx / fps khi cả hai trường có.\n"
                    f"- Ngưỡng lọc đối tượng (score_threshold): {score_threshold}.\n"
                    '- Cách lấy L và V: dùng tên video dạng Lxx_Vyyy (ví dụ L21_V001), hiển thị là "L21 V001".\n'
                    '- Màu bbox cố định theo nhãn để dễ phân biệt.\n\n'
                    'EN:\n'
                    "- Displayed frame number comes from 'frame_idx' in CSV when available; otherwise from keyframe filename (e.g., 001.jpg → 1).\n"
                    "- Mapping to 'map-keyframes' CSV: prefer column n (1-based); try zero-based fallback (n-1); else try frame_idx.\n"
                    "- Time is taken from 'pts_time' when present; otherwise computed as frame_idx / fps when both are available.\n"
                    f"- Detection score threshold: {score_threshold}.\n"
                    '- L/V identifier: extracted from video name Lxx_Vyyy (e.g., L21_V001) and shown as "L21 V001".\n'
                    '- Bounding-box color is stable per class label.\n\n'
                    'Aggregate matching counts:\n'
                    f"- by_n: {total_by_n}\n"
                    f"- by_frame_idx: {total_by_fidx}\n"
                    f"- unmatched: {total_unmatched}\n"
                    f"- processed_frames: {total_processed_frames}\n"
                )
        except Exception:
            pass

        return summary


