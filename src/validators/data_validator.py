#!/usr/bin/env python3
"""
HCMC AI Data Validator - Core validation functions
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class DataValidator:
    def __init__(self, data_path):
        self.data_path = Path(data_path)
        self.results = {
            'validation_time': datetime.now().isoformat(),
            'data_path': str(self.data_path),
            'file_counts': {},
            'missing_files': {},
            'duplicate_files': {},
            'empty_files': {},
            'structure_issues': [],
            'level_distribution': {},
            'summary': {}
        }
    
    def scan_directory(self, dir_name, file_pattern="*"):
        """Scan a directory for files matching pattern"""
        dir_path = self.data_path / dir_name
        if not dir_path.exists():
            self.results['structure_issues'].append(f"Directory not found: {dir_path}")
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
            self.results['structure_issues'].append(f"Error scanning {dir_name}: {e}")
        
        return files
    
    def get_video_names_from_files(self, files):
        """Extract video names from file paths"""
        video_names = set()
        for file_path in files:
            if file_path.name.startswith('L') and '_V' in file_path.name:
                video_name = file_path.stem
                video_names.add(video_name)
        return sorted(list(video_names))
    
    def check_file_sizes(self, files):
        """Check for empty or suspiciously small files"""
        empty_files = []
        small_files = []
        
        for file_path in files:
            try:
                size = file_path.stat().st_size
                if size == 0:
                    empty_files.append(str(file_path))
                elif size < 1024:  # Less than 1KB
                    small_files.append({
                        'file': str(file_path),
                        'size': size
                    })
            except Exception as e:
                self.results['structure_issues'].append(f"Error checking size of {file_path}: {e}")
        
        return empty_files, small_files
    
    def check_duplicate_patterns(self, files):
        """Check for files with duplicate naming patterns"""
        duplicate_patterns = [
            r'\([0-9]+\)',  # (1), (2), etc.
            r'_copy',       # _copy
            r'_duplicate',  # _duplicate
            r'_backup',     # _backup
            r'_old',        # _old
            r'_new',        # _new
            r'_v[0-9]+$',   # _v1, _v2, etc. (at end of filename)
        ]
        
        duplicate_files = []
        for file_path in files:
            filename = file_path.name
            
            # Skip normal video naming patterns (L21_V001, etc.)
            if re.match(r'L\d+_V\d+', filename):
                continue
                
            for pattern in duplicate_patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    duplicate_files.append({
                        'file': str(file_path),
                        'pattern': pattern
                    })
                    break
        
        return duplicate_files
    
    def analyze_level_distribution(self, video_names):
        """Analyze video distribution across levels"""
        level_counts = defaultdict(int)
        level_videos = defaultdict(list)
        
        for video_name in video_names:
            match = re.match(r'L(\d+)_V(\d+)', video_name)
            if match:
                level = match.group(1)
                video_num = int(match.group(2))
                level_counts[level] += 1
                level_videos[level].append(video_num)
        
        # Check for gaps
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
        """Run all validation checks"""
        print("🔍 Starting HCMC AI Data validation...")
        print(f"📁 Data path: {self.data_path}")
        print()
        
        # Define directories to check
        directories = {
            'videos': ('video', '*.mp4'),
            'keyframes': ('keyframes', '*.jpg'),
            'features': ('clip-features-32', '*.npy'),
            'maps': ('map-keyframes', '*.csv'),
            'media_info': ('media-info', '*.json'),
            'objects': ('objects', '*.json')
        }
        
        all_video_names = set()
        
        # Scan each directory
        for dir_type, (dir_name, pattern) in directories.items():
            print(f"📂 Scanning {dir_name}...")
            
            files = self.scan_directory(dir_name, pattern)
            self.results['file_counts'][dir_type] = len(files)
            
            # Get video names
            video_names = self.get_video_names_from_files(files)
            all_video_names.update(video_names)
            
            # Check file sizes
            empty_files, small_files = self.check_file_sizes(files)
            self.results['empty_files'][dir_type] = empty_files
            
            # Check for duplicate patterns
            duplicate_files = self.check_duplicate_patterns(files)
            self.results['duplicate_files'][dir_type] = duplicate_files
        
        # Analyze level distribution
        level_counts, gaps = self.analyze_level_distribution(list(all_video_names))
        self.results['level_distribution'] = {
            'counts': level_counts,
            'gaps': gaps
        }
        
        # Generate summary
        self.generate_summary()
        
        return self.results
    
    def generate_summary(self):
        """Generate summary statistics"""
        total_files = sum(self.results['file_counts'].values())
        total_empty_files = sum(len(files) for files in self.results['empty_files'].values())
        total_duplicate_patterns = sum(len(files) for files in self.results['duplicate_files'].values())
        
        self.results['summary'] = {
            'total_files': total_files,
            'total_empty_files': total_empty_files,
            'total_duplicate_patterns': total_duplicate_patterns,
            'structure_issues_count': len(self.results['structure_issues']),
            'overall_status': 'PASS' if total_empty_files == 0 and total_duplicate_patterns == 0 else 'ISSUES_FOUND'
        }
