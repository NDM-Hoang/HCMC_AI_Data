#!/usr/bin/env python3
"""
Duplicate File Checker for HCMC AI Data
This script checks for duplicate files with patterns like (1), _copy, etc.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

class DuplicateFileChecker:
    def __init__(self, data_path="/run/media/rin/New Volume/HCMC_AI_Data/Data2025"):
        self.data_path = Path(data_path)
        self.duplicate_patterns = [
            r'\([0-9]+\)',  # (1), (2), etc.
            r'_copy',       # _copy
            r'_copy_',      # _copy_
            r'_duplicate',  # _duplicate
            r'_backup',     # _backup
            r'_old',        # _old
            r'_new',        # _new
            r'_v[0-9]+',    # _v1, _v2, etc.
            r'_copy\([0-9]+\)',  # _copy(1), _copy(2), etc.
            r'_backup\([0-9]+\)', # _backup(1), etc.
        ]
        
    def check_for_duplicate_patterns(self):
        """Check for files with duplicate patterns in their names"""
        print("🔍 Checking for duplicate files with patterns like (1), _copy, etc...")
        print(f"📁 Data path: {self.data_path}")
        print()
        
        duplicate_files = defaultdict(list)
        total_files_checked = 0
        
        # Check all directories
        directories = [
            "video",
            "keyframes", 
            "clip-features-32",
            "map-keyframes",
            "media-info",
            "objects"
        ]
        
        for dir_name in directories:
            dir_path = self.data_path / dir_name
            if not dir_path.exists():
                print(f"⚠️  Directory not found: {dir_path}")
                continue
                
            print(f"📂 Checking directory: {dir_name}")
            
            if dir_name == "keyframes" or dir_name == "objects":
                # These are directories, check subdirectories
                for subdir in dir_path.iterdir():
                    if subdir.is_dir():
                        # Check files in subdirectories
                        for file_path in subdir.rglob("*"):
                            if file_path.is_file():
                                total_files_checked += 1
                                self._check_file_for_duplicates(file_path, duplicate_files, dir_name)
            else:
                # These are flat directories with files
                for file_path in dir_path.rglob("*"):
                    if file_path.is_file():
                        total_files_checked += 1
                        self._check_file_for_duplicates(file_path, duplicate_files, dir_name)
        
        return duplicate_files, total_files_checked
    
    def _check_file_for_duplicates(self, file_path, duplicate_files, dir_name):
        """Check if a file has duplicate patterns in its name"""
        filename = file_path.name
        stem = file_path.stem
        extension = file_path.suffix
        
        # Check for duplicate patterns
        for pattern in self.duplicate_patterns:
            if re.search(pattern, filename, re.IGNORECASE):
                duplicate_files[dir_name].append({
                    'file_path': str(file_path),
                    'filename': filename,
                    'pattern_found': pattern,
                    'size': file_path.stat().st_size if file_path.exists() else 0
                })
                break
    
    def check_for_actual_duplicates(self):
        """Check for files with identical content (same hash)"""
        print("\n🔍 Checking for files with identical content...")
        
        import hashlib
        
        file_hashes = defaultdict(list)
        total_files_checked = 0
        
        # Check all directories
        directories = [
            "video",
            "keyframes", 
            "clip-features-32",
            "map-keyframes",
            "media-info",
            "objects"
        ]
        
        for dir_name in directories:
            dir_path = self.data_path / dir_name
            if not dir_path.exists():
                continue
                
            print(f"📂 Checking content in: {dir_name}")
            
            if dir_name == "keyframes" or dir_name == "objects":
                # These are directories, check subdirectories
                for subdir in dir_path.iterdir():
                    if subdir.is_dir():
                        for file_path in subdir.rglob("*"):
                            if file_path.is_file():
                                total_files_checked += 1
                                self._hash_file(file_path, file_hashes, dir_name)
            else:
                # These are flat directories with files
                for file_path in dir_path.rglob("*"):
                    if file_path.is_file():
                        total_files_checked += 1
                        self._hash_file(file_path, file_hashes, dir_name)
        
        # Find duplicates
        content_duplicates = {}
        for dir_name, hashes in file_hashes.items():
            dir_duplicates = {}
            for file_hash, files in hashes.items():
                if len(files) > 1:
                    dir_duplicates[file_hash] = files
            if dir_duplicates:
                content_duplicates[dir_name] = dir_duplicates
        
        return content_duplicates, total_files_checked
    
    def _hash_file(self, file_path, file_hashes, dir_name):
        """Calculate hash of a file"""
        try:
            import hashlib
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            file_hash = hash_md5.hexdigest()
            file_hashes[dir_name].append((file_hash, str(file_path)))
        except Exception as e:
            print(f"⚠️  Error hashing {file_path}: {e}")
    
    def generate_report(self):
        """Generate comprehensive duplicate file report"""
        print("=" * 80)
        print("🔍 DUPLICATE FILE ANALYSIS REPORT")
        print("=" * 80)
        print()
        
        # Check for duplicate patterns
        pattern_duplicates, total_checked = self.check_for_duplicate_patterns()
        
        # Check for content duplicates
        content_duplicates, total_content_checked = self.check_for_actual_duplicates()
        
        print("\n" + "=" * 80)
        print("📊 DUPLICATE FILE SUMMARY")
        print("=" * 80)
        print()
        
        # Pattern duplicates summary
        print("🔍 FILES WITH DUPLICATE PATTERNS IN NAMES:")
        total_pattern_duplicates = 0
        for dir_name, duplicates in pattern_duplicates.items():
            if duplicates:
                print(f"   📁 {dir_name}: {len(duplicates)} files")
                total_pattern_duplicates += len(duplicates)
                for dup in duplicates[:5]:  # Show first 5
                    print(f"     - {dup['filename']} (pattern: {dup['pattern_found']})")
                if len(duplicates) > 5:
                    print(f"     ... and {len(duplicates) - 5} more")
            else:
                print(f"   📁 {dir_name}: ✅ No duplicate patterns found")
        
        if total_pattern_duplicates == 0:
            print("   ✅ NO FILES WITH DUPLICATE PATTERNS FOUND")
        
        print()
        
        # Content duplicates summary
        print("🔍 FILES WITH IDENTICAL CONTENT:")
        total_content_duplicates = 0
        for dir_name, duplicates in content_duplicates.items():
            if duplicates:
                print(f"   📁 {dir_name}: {len(duplicates)} duplicate groups")
                total_content_duplicates += len(duplicates)
                for hash_val, files in list(duplicates.items())[:3]:  # Show first 3 groups
                    print(f"     Hash {hash_val[:8]}...: {len(files)} files")
                    for file_path in files[:3]:  # Show first 3 files in group
                        print(f"       - {Path(file_path).name}")
                    if len(files) > 3:
                        print(f"       ... and {len(files) - 3} more")
            else:
                print(f"   📁 {dir_name}: ✅ No content duplicates found")
        
        if total_content_duplicates == 0:
            print("   ✅ NO FILES WITH IDENTICAL CONTENT FOUND")
        
        print()
        
        # Overall summary
        print("📈 OVERALL SUMMARY:")
        print(f"   Files checked for patterns: {total_checked:,}")
        print(f"   Files checked for content: {total_content_checked:,}")
        print(f"   Files with duplicate patterns: {total_pattern_duplicates}")
        print(f"   Groups with identical content: {total_content_duplicates}")
        
        if total_pattern_duplicates == 0 and total_content_duplicates == 0:
            print("   🎉 EXCELLENT: No duplicate files found!")
        else:
            print("   ⚠️  Duplicate files detected - review recommended")
        
        print("\n" + "=" * 80)
        
        # Save detailed results
        results = {
            'pattern_duplicates': dict(pattern_duplicates),
            'content_duplicates': content_duplicates,
            'summary': {
                'total_files_checked': total_checked,
                'total_content_checked': total_content_checked,
                'total_pattern_duplicates': total_pattern_duplicates,
                'total_content_duplicates': total_content_duplicates
            }
        }
        
        with open('duplicate_file_results.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print("📄 Detailed results saved to: duplicate_file_results.json")

def main():
    checker = DuplicateFileChecker()
    checker.generate_report()

if __name__ == "__main__":
    main()
