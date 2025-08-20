#!/usr/bin/env python3
"""
HCMC AI Data Comprehensive Validator - Kiểm tra đa thư mục
Kiểm tra mối quan hệ giữa video và các file tương ứng trong tất cả các thư mục
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class ComprehensiveValidator:
    def __init__(self, data_path):
        self.data_path = Path(data_path)
        self.results = {
            'validation_time': datetime.now().isoformat(),
            'data_path': str(self.data_path),
            'file_counts': {},
            'video_mapping': {},
            'missing_files': {},
            'duplicate_files': {},
            'empty_files': {},
            'cross_directory_issues': [],
            'structure_issues': [],
            'level_distribution': {},
            'summary': {}
        }
        
        # Define the expected directory structure and file patterns
        self.directories = {
            'videos': ('video', '*.mp4'),
            'keyframes': ('keyframes', '*.jpg'),
            'features': ('clip-features-32', '*.npy'),
            'maps': ('map-keyframes', '*.csv'),
            'media_info': ('media-info', '*.json'),
            'objects': ('objects', '*.json')
        }
    
    def scan_directory(self, dir_name, file_pattern="*"):
        """Quét thư mục để tìm các file khớp với mẫu"""
        dir_path = self.data_path / dir_name
        if not dir_path.exists():
            self.results['structure_issues'].append(f"Không tìm thấy thư mục: {dir_path}")
            return []
        
        files = []
        try:
            if dir_name in ["keyframes", "objects"]:
                # These are directories with subdirectories
                for subdir in dir_path.iterdir():
                    if subdir.is_dir():
                        for file_path in subdir.rglob(file_pattern):
                            if file_path.is_file():
                                files.append(file_path)
            else:
                # Flat directories
                for file_path in dir_path.rglob(file_pattern):
                    if file_path.is_file():
                        files.append(file_path)
        except Exception as e:
            self.results['structure_issues'].append(f"Lỗi khi quét {dir_name}: {e}")
        
        return files
    
    def extract_video_name(self, file_path):
        """Trích xuất tên video từ đường dẫn file"""
        filename = file_path.stem  # Remove extension
        
        # Xử lý các mẫu đặt tên file khác nhau
        if filename.startswith('L') and '_V' in filename:
            # Tên video trực tiếp (L21_V001)
            return filename
        elif '_' in filename:
            # File keyframe hoặc object (L21_V001_001)
            parts = filename.split('_')
            if len(parts) >= 2:
                return f"{parts[0]}_{parts[1]}"
        
        # Đối với keyframes và objects có tên số (001.jpg, 002.json)
        # Trích xuất tên video từ thư mục cha
        parent_dir = file_path.parent.name
        if parent_dir.startswith('L') and '_V' in parent_dir:
            return parent_dir
        
        return None
    
    def get_video_names_from_files(self, files):
        """Trích xuất tên video từ danh sách file"""
        video_names = set()
        for file_path in files:
            video_name = self.extract_video_name(file_path)
            if video_name:
                video_names.add(video_name)
        return sorted(list(video_names))
    
    def build_video_mapping(self):
        """Xây dựng bản đồ tên video đến các file của chúng trên tất cả các thư mục"""
        video_mapping = defaultdict(lambda: defaultdict(list))
        
        for dir_type, (dir_name, pattern) in self.directories.items():
            print(f"📂 Đang quét {dir_name} để lập bản đồ video...")
            files = self.scan_directory(dir_name, pattern)
            
            for file_path in files:
                video_name = self.extract_video_name(file_path)
                if video_name:
                    video_mapping[video_name][dir_type].append(str(file_path))
        
        return dict(video_mapping)
    
    def check_cross_directory_consistency(self, video_mapping):
        """Kiểm tra xem mỗi video có file tương ứng trong tất cả các thư mục không"""
        issues = []
        missing_files = defaultdict(list)
        
        # Lấy tất cả tên video duy nhất
        all_videos = set(video_mapping.keys())
        
        for video_name in all_videos:
            video_files = video_mapping[video_name]
            
            # Kiểm tra xem video có file trong tất cả các thư mục mong đợi không
            for dir_type in self.directories.keys():
                if dir_type not in video_files or not video_files[dir_type]:
                    missing_files[dir_type].append(video_name)
                    issues.append(f"Thiếu file {dir_type} cho video: {video_name}")
        
        return issues, dict(missing_files)
    
    def check_duplicate_files(self, video_mapping):
        """Kiểm tra file trùng lặp trên các thư mục"""
        duplicate_issues = []
        duplicate_files = defaultdict(list)
        
        # Các thư mục mà nhiều file cho mỗi video là bình thường
        expected_multiple = {'keyframes', 'objects'}
        
        for video_name, dir_files in video_mapping.items():
            for dir_type, files in dir_files.items():
                if len(files) > 1:
                    if dir_type in expected_multiple:
                        # Nhiều keyframes/objects cho mỗi video là bình thường
                        continue
                    else:
                        # Nhiều file trong các thư mục khác có thể là trùng lặp
                        duplicate_files[dir_type].append({
                            'video': video_name,
                            'files': files,
                            'count': len(files)
                        })
                        duplicate_issues.append(f"File {dir_type} trùng lặp cho video: {video_name} ({len(files)} files)")
        
        return duplicate_issues, dict(duplicate_files)
    
    def check_file_sizes(self, video_mapping):
        """Kiểm tra file rỗng hoặc có kích thước đáng ngờ"""
        empty_files = defaultdict(list)
        small_files = defaultdict(list)
        
        for video_name, dir_files in video_mapping.items():
            for dir_type, files in dir_files.items():
                for file_path in files:
                    try:
                        size = Path(file_path).stat().st_size
                        if size == 0:
                            empty_files[dir_type].append({
                                'video': video_name,
                                'file': file_path,
                                'size': size
                            })
                        elif size < 1024:  # Less than 1KB
                            small_files[dir_type].append({
                                'video': video_name,
                                'file': file_path,
                                'size': size
                            })
                    except Exception as e:
                        self.results['structure_issues'].append(f"Lỗi khi kiểm tra kích thước của {file_path}: {e}")
        
        return dict(empty_files), dict(small_files)
    
    def analyze_level_distribution(self, video_names):
        """Phân tích phân bố video theo các cấp độ"""
        level_counts = defaultdict(int)
        level_videos = defaultdict(list)
        
        for video_name in video_names:
            match = re.match(r'L(\d+)_V(\d+)', video_name)
            if match:
                level = match.group(1)
                video_num = int(match.group(2))
                level_counts[level] += 1
                level_videos[level].append(video_num)
        
        # Kiểm tra khoảng trống
        gaps = {}
        for level, videos in level_videos.items():
            if videos:
                videos.sort()
                expected_videos = set(range(1, max(videos) + 1))
                actual_videos = set(videos)
                missing = expected_videos - actual_videos
                if missing:
                    gaps[level] = sorted(missing)
        
        return dict(level_counts), gaps
    
    def validate_all(self):
        """Chạy tất cả các kiểm tra xác thực toàn diện"""
        print("🔍 Bắt đầu Kiểm tra Toàn diện Dữ liệu AI HCMC...")
        print(f"📁 Đường dẫn dữ liệu: {self.data_path}")
        print()
        
        # Xây dựng bản đồ video trên tất cả các thư mục
        print("🗺️ Đang xây dựng bản đồ video trên tất cả các thư mục...")
        video_mapping = self.build_video_mapping()
        self.results['video_mapping'] = video_mapping
        
        # Đếm file theo thư mục
        for dir_type in self.directories.keys():
            total_files = sum(len(files) for files in video_mapping.values() if dir_type in files)
            self.results['file_counts'][dir_type] = total_files
        
        # Kiểm tra tính nhất quán đa thư mục
        print("🔍 Đang kiểm tra tính nhất quán đa thư mục...")
        consistency_issues, missing_files = self.check_cross_directory_consistency(video_mapping)
        self.results['cross_directory_issues'] = consistency_issues
        self.results['missing_files'] = missing_files
        
        # Kiểm tra file trùng lặp
        print("🔍 Đang kiểm tra file trùng lặp...")
        duplicate_issues, duplicate_files = self.check_duplicate_files(video_mapping)
        self.results['duplicate_files'] = duplicate_files
        
        # Kiểm tra kích thước file
        print("🔍 Đang kiểm tra kích thước file...")
        empty_files, small_files = self.check_file_sizes(video_mapping)
        self.results['empty_files'] = empty_files
        
        # Phân tích phân bố cấp độ
        print("📊 Đang phân tích phân bố cấp độ...")
        level_counts, gaps = self.analyze_level_distribution(video_mapping.keys())
        self.results['level_distribution'] = {
            'counts': level_counts,
            'gaps': gaps
        }
        
        # Tạo bản tóm tắt
        self.generate_summary()
        
        return self.results
    
    def generate_summary(self):
        """Tạo thống kê tóm tắt toàn diện"""
        total_files = sum(self.results['file_counts'].values())
        total_empty_files = sum(len(files) for files in self.results['empty_files'].values())
        total_duplicate_patterns = sum(len(files) for files in self.results['duplicate_files'].values())
        total_missing_files = sum(len(videos) for videos in self.results['missing_files'].values())
        total_cross_directory_issues = len(self.results['cross_directory_issues'])
        
        self.results['summary'] = {
            'total_files': total_files,
            'total_videos': len(self.results['video_mapping']),
            'total_empty_files': total_empty_files,
            'total_duplicate_patterns': total_duplicate_patterns,
            'total_missing_files': total_missing_files,
            'total_cross_directory_issues': total_cross_directory_issues,
            'structure_issues_count': len(self.results['structure_issues']),
            'overall_status': 'PASS' if (total_empty_files == 0 and 
                                       total_duplicate_patterns == 0 and 
                                       total_missing_files == 0 and 
                                       total_cross_directory_issues == 0) else 'ISSUES_FOUND'
        }
