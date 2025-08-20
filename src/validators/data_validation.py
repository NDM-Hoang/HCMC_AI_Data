#!/usr/bin/env python3
"""
HCMC AI Data Validation Script
This script validates the data structure and checks for missing files.
"""

import os
import json
from pathlib import Path
import zipfile
from collections import defaultdict, Counter
import re

class HCMCDataValidator:
    def __init__(self, data_path="/run/media/rin/New Volume/HCMC_AI_Data/Data2025"):
        self.data_path = Path(data_path)
        self.results = {
            'expected_videos': [],
            'found_videos': [],
            'expected_keyframes': [],
            'found_keyframes': [],
            'expected_features': [],
            'found_features': [],
            'expected_maps': [],
            'found_maps': [],
            'expected_media_info': [],
            'found_media_info': [],
            'expected_objects': [],
            'found_objects': [],
            'missing_files': [],
            'structure_issues': []
        }
        
    def generate_expected_video_names(self):
        """Generate expected video names based on actual data"""
        # Instead of assuming 96 videos per level, we'll use the actual found videos
        # This will be updated after scanning the actual data
        return []
    
    def scan_video_directory(self):
        """Scan the video directory for actual video files"""
        video_dir = self.data_path / "video"
        if not video_dir.exists():
            self.results['structure_issues'].append(f"Video directory not found: {video_dir}")
            return []
        
        found_videos = []
        for video_file in video_dir.glob("*.mp4"):
            found_videos.append(video_file.stem)  # Remove .mp4 extension
        
        return sorted(found_videos)
    
    def scan_keyframes_directory(self):
        """Scan the keyframes directory for actual keyframe files"""
        keyframes_dir = self.data_path / "keyframes"
        if not keyframes_dir.exists():
            self.results['structure_issues'].append(f"Keyframes directory not found: {keyframes_dir}")
            return []
        
        found_keyframes = []
        for video_dir in keyframes_dir.iterdir():
            if video_dir.is_dir() and video_dir.name.startswith('L'):
                found_keyframes.append(video_dir.name)
        
        return sorted(found_keyframes)
    
    def scan_features_directory(self):
        """Scan the clip-features directory for .npy files"""
        features_dir = self.data_path / "clip-features-32"
        if not features_dir.exists():
            self.results['structure_issues'].append(f"Features directory not found: {features_dir}")
            return []
        
        found_features = []
        for npy_file in features_dir.glob("*.npy"):
            found_features.append(npy_file.stem)  # Remove .npy extension
        
        return sorted(found_features)
    
    def scan_maps_directory(self):
        """Scan the map-keyframes directory for .csv files"""
        maps_dir = self.data_path / "map-keyframes"
        if not maps_dir.exists():
            self.results['structure_issues'].append(f"Maps directory not found: {maps_dir}")
            return []
        
        found_maps = []
        for csv_file in maps_dir.glob("*.csv"):
            found_maps.append(csv_file.stem)  # Remove .csv extension
        
        return sorted(found_maps)
    
    def scan_media_info_directory(self):
        """Scan the media-info directory for .json files"""
        media_info_dir = self.data_path / "media-info"
        if not media_info_dir.exists():
            self.results['structure_issues'].append(f"Media info directory not found: {media_info_dir}")
            return []
        
        found_media_info = []
        for json_file in media_info_dir.glob("*.json"):
            found_media_info.append(json_file.stem)  # Remove .json extension
        
        return sorted(found_media_info)
    
    def scan_objects_directory(self):
        """Scan the objects directory for video folders"""
        objects_dir = self.data_path / "objects"
        if not objects_dir.exists():
            self.results['structure_issues'].append(f"Objects directory not found: {objects_dir}")
            return []
        
        found_objects = []
        for video_dir in objects_dir.iterdir():
            if video_dir.is_dir() and video_dir.name.startswith('L'):
                found_objects.append(video_dir.name)
        
        return sorted(found_objects)
    
    def count_keyframe_files(self):
        """Count total keyframe files across all directories"""
        keyframes_dir = self.data_path / "keyframes"
        if not keyframes_dir.exists():
            return 0
        
        total_count = 0
        for video_dir in keyframes_dir.iterdir():
            if video_dir.is_dir() and video_dir.name.startswith('L'):
                jpg_count = len(list(video_dir.glob("*.jpg")))
                total_count += jpg_count
        
        return total_count
    
    def count_video_files(self):
        """Count total video files"""
        video_dir = self.data_path / "video"
        if not video_dir.exists():
            return 0
        
        return len(list(video_dir.glob("*.mp4")))
    
    def validate_data_structure(self):
        """Main validation function"""
        print("🔍 Starting HCMC AI Data validation...")
        print(f"📁 Data path: {self.data_path}")
        print()
        
        # Scan actual directories first
        self.results['found_videos'] = self.scan_video_directory()
        self.results['found_keyframes'] = self.scan_keyframes_directory()
        self.results['found_features'] = self.scan_features_directory()
        self.results['found_maps'] = self.scan_maps_directory()
        self.results['found_media_info'] = self.scan_media_info_directory()
        self.results['found_objects'] = self.scan_objects_directory()
        
        # Use found videos as the expected set
        self.results['expected_videos'] = self.results['found_videos']
        
        # Count files
        total_keyframes = self.count_keyframe_files()
        total_videos = self.count_video_files()
        
        # Find missing files by comparing across directories
        all_video_sets = [
            set(self.results['found_videos']),
            set(self.results['found_keyframes']),
            set(self.results['found_features']),
            set(self.results['found_maps']),
            set(self.results['found_media_info']),
            set(self.results['found_objects'])
        ]
        
        # Find videos that are missing from any directory
        all_videos = set.union(*all_video_sets)
        self.results['missing_files'] = {
            'videos': list(all_videos - set(self.results['found_videos'])),
            'keyframes': list(all_videos - set(self.results['found_keyframes'])),
            'features': list(all_videos - set(self.results['found_features'])),
            'maps': list(all_videos - set(self.results['found_maps'])),
            'media_info': list(all_videos - set(self.results['found_media_info'])),
            'objects': list(all_videos - set(self.results['found_objects']))
        }
        
        return {
            'total_videos': total_videos,
            'total_keyframes': total_keyframes,
            'expected_video_count': len(all_videos),
            'results': self.results
        }
    
    def print_report(self, validation_results):
        """Print comprehensive validation report"""
        print("=" * 80)
        print("📊 HCMC AI DATA VALIDATION REPORT")
        print("=" * 80)
        print()
        
        # Summary statistics
        print("📈 SUMMARY STATISTICS:")
        print(f"   Expected videos: {validation_results['expected_video_count']}")
        print(f"   Found videos: {validation_results['total_videos']}")
        print(f"   Found keyframes: {validation_results['total_keyframes']}")
        print()
        
        # File counts by type
        print("📁 FILE COUNTS BY TYPE:")
        print(f"   Videos (.mp4): {len(self.results['found_videos'])}")
        print(f"   Keyframe directories: {len(self.results['found_keyframes'])}")
        print(f"   Feature files (.npy): {len(self.results['found_features'])}")
        print(f"   Map files (.csv): {len(self.results['found_maps'])}")
        print(f"   Media info files (.json): {len(self.results['found_media_info'])}")
        print(f"   Object directories: {len(self.results['found_objects'])}")
        print()
        
        # Missing files analysis
        print("❌ MISSING FILES ANALYSIS:")
        for file_type, missing in self.results['missing_files'].items():
            if missing:
                print(f"   {file_type.upper()}: {len(missing)} missing files")
                if len(missing) <= 10:  # Show first 10 missing files
                    for missing_file in missing[:10]:
                        print(f"     - {missing_file}")
                else:
                    print(f"     - First 10: {', '.join(missing[:10])}")
                    print(f"     - ... and {len(missing) - 10} more")
            else:
                print(f"   {file_type.upper()}: ✅ All files present")
        print()
        
        # Structure issues
        if self.results['structure_issues']:
            print("⚠️  STRUCTURE ISSUES:")
            for issue in self.results['structure_issues']:
                print(f"   - {issue}")
            print()
        
        # Consistency check
        print("🔍 CONSISTENCY CHECK:")
        all_sets = [
            set(self.results['found_videos']),
            set(self.results['found_keyframes']),
            set(self.results['found_features']),
            set(self.results['found_maps']),
            set(self.results['found_media_info']),
            set(self.results['found_objects'])
        ]
        
        common_videos = set.intersection(*all_sets)
        print(f"   Videos present in ALL directories: {len(common_videos)}")
        
        if len(common_videos) != len(self.results['expected_videos']):
            print(f"   ⚠️  Expected {len(self.results['expected_videos'])} videos, found {len(common_videos)} in all directories")
        
        # Level distribution analysis
        print("\n📊 LEVEL DISTRIBUTION ANALYSIS:")
        level_counts = defaultdict(int)
        for video in self.results['found_videos']:
            match = re.match(r'L(\d+)_V\d+', video)
            if match:
                level_counts[match.group(1)] += 1
        
        for level in sorted(level_counts.keys()):
            print(f"   L{level}: {level_counts[level]} videos")
        
        print("\n" + "=" * 80)

def main():
    validator = HCMCDataValidator()
    results = validator.validate_data_structure()
    validator.print_report(results)
    
    # Save detailed results to JSON
    output_file = "data_validation_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Detailed results saved to: {output_file}")

if __name__ == "__main__":
    main()
