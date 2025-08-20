#!/usr/bin/env python3
"""
Detailed HCMC AI Data Analysis Script
This script provides comprehensive analysis of the data structure and content.
"""

import os
import json
from pathlib import Path
from collections import defaultdict, Counter
import re

class DetailedDataAnalyzer:
    def __init__(self, data_path="/run/media/rin/New Volume/HCMC_AI_Data/Data2025"):
        self.data_path = Path(data_path)
        
    def analyze_video_distribution(self):
        """Analyze video distribution across levels"""
        video_dir = self.data_path / "video"
        if not video_dir.exists():
            return {}
        
        level_counts = defaultdict(int)
        video_list = defaultdict(list)
        
        for video_file in video_dir.glob("*.mp4"):
            video_name = video_file.stem
            match = re.match(r'L(\d+)_V(\d+)', video_name)
            if match:
                level = match.group(1)
                video_num = int(match.group(2))
                level_counts[level] += 1
                video_list[level].append(video_num)
        
        # Check for gaps in video numbering
        gaps = {}
        for level, videos in video_list.items():
            videos.sort()
            expected_videos = set(range(1, max(videos) + 1))
            actual_videos = set(videos)
            missing = expected_videos - actual_videos
            if missing:
                gaps[level] = sorted(missing)
        
        return {
            'level_counts': dict(level_counts),
            'video_list': {k: sorted(v) for k, v in video_list.items()},
            'gaps': gaps
        }
    
    def analyze_keyframe_distribution(self):
        """Analyze keyframe distribution"""
        keyframes_dir = self.data_path / "keyframes"
        if not keyframes_dir.exists():
            return {}
        
        keyframe_counts = {}
        total_keyframes = 0
        
        for video_dir in keyframes_dir.iterdir():
            if video_dir.is_dir() and video_dir.name.startswith('L'):
                jpg_files = list(video_dir.glob("*.jpg"))
                keyframe_count = len(jpg_files)
                keyframe_counts[video_dir.name] = keyframe_count
                total_keyframes += keyframe_count
        
        return {
            'keyframe_counts': keyframe_counts,
            'total_keyframes': total_keyframes,
            'average_keyframes_per_video': total_keyframes / len(keyframe_counts) if keyframe_counts else 0
        }
    
    def analyze_feature_files(self):
        """Analyze feature files"""
        features_dir = self.data_path / "clip-features-32"
        if not features_dir.exists():
            return {}
        
        feature_files = list(features_dir.glob("*.npy"))
        return {
            'total_features': len(feature_files),
            'feature_files': [f.stem for f in feature_files]
        }
    
    def analyze_map_files(self):
        """Analyze map files and their content"""
        maps_dir = self.data_path / "map-keyframes"
        if not maps_dir.exists():
            return {}
        
        map_files = list(maps_dir.glob("*.csv"))
        map_analysis = {}
        
        # Sample a few files to understand the structure
        sample_files = map_files[:5] if len(map_files) >= 5 else map_files
        
        for csv_file in sample_files:
            try:
                with open(csv_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        header = lines[0].strip().split(',')
                        map_analysis[csv_file.stem] = {
                            'header': header,
                            'line_count': len(lines) - 1  # Exclude header
                        }
            except Exception as e:
                map_analysis[csv_file.stem] = {'error': str(e)}
        
        return {
            'total_maps': len(map_files),
            'sample_analysis': map_analysis
        }
    
    def analyze_media_info(self):
        """Analyze media info files"""
        media_info_dir = self.data_path / "media-info"
        if not media_info_dir.exists():
            return {}
        
        json_files = list(media_info_dir.glob("*.json"))
        media_analysis = {}
        
        # Sample a few files to understand the structure
        sample_files = json_files[:3] if len(json_files) >= 3 else json_files
        
        for json_file in sample_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    media_analysis[json_file.stem] = {
                        'keys': list(data.keys()) if isinstance(data, dict) else 'not_dict',
                        'data_type': type(data).__name__
                    }
            except Exception as e:
                media_analysis[json_file.stem] = {'error': str(e)}
        
        return {
            'total_media_info': len(json_files),
            'sample_analysis': media_analysis
        }
    
    def analyze_objects(self):
        """Analyze object files"""
        objects_dir = self.data_path / "objects"
        if not objects_dir.exists():
            return {}
        
        object_analysis = {}
        total_object_files = 0
        
        for video_dir in objects_dir.iterdir():
            if video_dir.is_dir() and video_dir.name.startswith('L'):
                json_files = list(video_dir.glob("*.json"))
                object_analysis[video_dir.name] = {
                    'object_files': len(json_files),
                    'file_numbers': [f.stem for f in json_files]
                }
                total_object_files += len(json_files)
        
        return {
            'total_object_files': total_object_files,
            'object_analysis': object_analysis
        }
    
    def check_data_consistency(self):
        """Check consistency across all data types"""
        video_dir = self.data_path / "video"
        keyframes_dir = self.data_path / "keyframes"
        features_dir = self.data_path / "clip-features-32"
        maps_dir = self.data_path / "map-keyframes"
        media_info_dir = self.data_path / "media-info"
        objects_dir = self.data_path / "objects"
        
        # Get all video names from each directory
        videos = {f.stem for f in video_dir.glob("*.mp4")} if video_dir.exists() else set()
        keyframes = {d.name for d in keyframes_dir.iterdir() if d.is_dir() and d.name.startswith('L')} if keyframes_dir.exists() else set()
        features = {f.stem for f in features_dir.glob("*.npy")} if features_dir.exists() else set()
        maps = {f.stem for f in maps_dir.glob("*.csv")} if maps_dir.exists() else set()
        media_info = {f.stem for f in media_info_dir.glob("*.json")} if media_info_dir.exists() else set()
        objects = {d.name for d in objects_dir.iterdir() if d.is_dir() and d.name.startswith('L')} if objects_dir.exists() else set()
        
        all_sets = [videos, keyframes, features, maps, media_info, objects]
        all_videos = set.union(*all_sets)
        
        consistency_report = {
            'total_unique_videos': len(all_videos),
            'videos_in_all_directories': len(set.intersection(*all_sets)),
            'missing_from_videos': list(all_videos - videos),
            'missing_from_keyframes': list(all_videos - keyframes),
            'missing_from_features': list(all_videos - features),
            'missing_from_maps': list(all_videos - maps),
            'missing_from_media_info': list(all_videos - media_info),
            'missing_from_objects': list(all_videos - objects)
        }
        
        return consistency_report
    
    def generate_comprehensive_report(self):
        """Generate comprehensive analysis report"""
        print("🔍 Starting detailed HCMC AI Data analysis...")
        print(f"📁 Data path: {self.data_path}")
        print()
        
        # Run all analyses
        video_analysis = self.analyze_video_distribution()
        keyframe_analysis = self.analyze_keyframe_distribution()
        feature_analysis = self.analyze_feature_files()
        map_analysis = self.analyze_map_files()
        media_analysis = self.analyze_media_info()
        object_analysis = self.analyze_objects()
        consistency = self.check_data_consistency()
        
        # Print comprehensive report
        print("=" * 100)
        print("📊 DETAILED HCMC AI DATA ANALYSIS REPORT")
        print("=" * 100)
        print()
        
        # Video distribution analysis
        print("🎬 VIDEO DISTRIBUTION ANALYSIS:")
        if video_analysis.get('level_counts'):
            for level in sorted(video_analysis['level_counts'].keys()):
                count = video_analysis['level_counts'][level]
                print(f"   L{level}: {count} videos")
            
            if video_analysis.get('gaps'):
                print("\n   ⚠️  GAPS IN VIDEO NUMBERING:")
                for level, gaps in video_analysis['gaps'].items():
                    print(f"     L{level}: Missing videos {gaps}")
        print()
        
        # Keyframe analysis
        print("🖼️  KEYFRAME ANALYSIS:")
        if keyframe_analysis:
            print(f"   Total keyframes: {keyframe_analysis['total_keyframes']:,}")
            print(f"   Average keyframes per video: {keyframe_analysis['average_keyframes_per_video']:.1f}")
            
            # Find videos with unusual keyframe counts
            counts = list(keyframe_analysis['keyframe_counts'].values())
            if counts:
                min_count = min(counts)
                max_count = max(counts)
                print(f"   Min keyframes per video: {min_count}")
                print(f"   Max keyframes per video: {max_count}")
        print()
        
        # Feature analysis
        print("🔧 FEATURE ANALYSIS:")
        if feature_analysis:
            print(f"   Total feature files: {feature_analysis['total_features']}")
        print()
        
        # Map analysis
        print("🗺️  MAP ANALYSIS:")
        if map_analysis:
            print(f"   Total map files: {map_analysis['total_maps']}")
            if map_analysis.get('sample_analysis'):
                print("   Sample file structure:")
                for video, info in list(map_analysis['sample_analysis'].items())[:3]:
                    if 'header' in info:
                        print(f"     {video}: {info['header']} ({info['line_count']} lines)")
        print()
        
        # Media info analysis
        print("📋 MEDIA INFO ANALYSIS:")
        if media_analysis:
            print(f"   Total media info files: {media_analysis['total_media_info']}")
            if media_analysis.get('sample_analysis'):
                print("   Sample file structure:")
                for video, info in list(media_analysis['sample_analysis'].items())[:3]:
                    if 'keys' in info:
                        print(f"     {video}: {info['keys']}")
        print()
        
        # Object analysis
        print("🎯 OBJECT ANALYSIS:")
        if object_analysis:
            print(f"   Total object files: {object_analysis['total_object_files']}")
            if object_analysis.get('object_analysis'):
                # Show sample object file counts
                sample_videos = list(object_analysis['object_analysis'].items())[:5]
                for video, info in sample_videos:
                    print(f"     {video}: {info['object_files']} object files")
        print()
        
        # Consistency check
        print("🔍 DATA CONSISTENCY CHECK:")
        print(f"   Total unique videos across all data types: {consistency['total_unique_videos']}")
        print(f"   Videos present in ALL directories: {consistency['videos_in_all_directories']}")
        
        missing_counts = {
            'Videos': len(consistency['missing_from_videos']),
            'Keyframes': len(consistency['missing_from_keyframes']),
            'Features': len(consistency['missing_from_features']),
            'Maps': len(consistency['missing_from_maps']),
            'Media Info': len(consistency['missing_from_media_info']),
            'Objects': len(consistency['missing_from_objects'])
        }
        
        print("\n   Missing files by type:")
        for data_type, count in missing_counts.items():
            status = "✅ Complete" if count == 0 else f"❌ Missing {count}"
            print(f"     {data_type}: {status}")
        
        print("\n" + "=" * 100)
        
        # Save detailed results
        detailed_results = {
            'video_analysis': video_analysis,
            'keyframe_analysis': keyframe_analysis,
            'feature_analysis': feature_analysis,
            'map_analysis': map_analysis,
            'media_analysis': media_analysis,
            'object_analysis': object_analysis,
            'consistency': consistency
        }
        
        with open('detailed_analysis_results.json', 'w', encoding='utf-8') as f:
            json.dump(detailed_results, f, indent=2, ensure_ascii=False)
        
        print("📄 Detailed analysis results saved to: detailed_analysis_results.json")

def main():
    analyzer = DetailedDataAnalyzer()
    analyzer.generate_comprehensive_report()

if __name__ == "__main__":
    main()
