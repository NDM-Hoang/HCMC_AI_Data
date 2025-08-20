#!/usr/bin/env python3
"""
HCMC AI Data 2025 - Main Validation Script
Cross-platform (Linux, Mac, Windows) validation

Usage:
    python check.py [data_path]
    
Example:
    python check.py "/path/to/Data2025"
    python check.py  # Uses default path
"""

import sys
import json
from pathlib import Path
from ..validators.data_validator import DataValidator

def get_default_path():
    """Get default data path based on operating system"""
    if sys.platform.startswith('win'):
        return "C:/HCMC_AI_Data/Data2025"
    elif sys.platform.startswith('darwin'):
        return "/Volumes/Data/HCMC_AI_Data/Data2025"
    else:
        return "/run/media/rin/New Volume/HCMC_AI_Data/Data2025"

def print_report(results):
    """Print comprehensive validation report"""
    print("=" * 100)
    print("📊 HCMC AI DATA VALIDATION REPORT")
    print("=" * 100)
    print()
    
    # Summary statistics
    print("📈 SUMMARY STATISTICS:")
    print(f"   Total files: {results['summary']['total_files']:,}")
    print(f"   Empty files: {results['summary']['total_empty_files']}")
    print(f"   Duplicate patterns: {results['summary']['total_duplicate_patterns']}")
    print(f"   Structure issues: {results['summary']['structure_issues_count']}")
    print(f"   Overall status: {results['summary']['overall_status']}")
    print()
    
    # File counts by type
    print("📁 FILE COUNTS BY TYPE:")
    for dir_type, count in results['file_counts'].items():
        print(f"   {dir_type.replace('_', ' ').title()}: {count:,}")
    print()
    
    # Level distribution
    print("📊 LEVEL DISTRIBUTION:")
    for level in sorted(results['level_distribution']['counts'].keys()):
        count = results['level_distribution']['counts'][level]
        print(f"   L{level}: {count} videos")
    
    if results['level_distribution']['gaps']:
        print("\n   ⚠️  GAPS IN VIDEO NUMBERING:")
        for level, gaps in results['level_distribution']['gaps'].items():
            print(f"     L{level}: Missing videos {gaps}")
    print()
    
    # Empty files check
    print("🔍 EMPTY FILES CHECK:")
    total_empty = 0
    for dir_type, empty_files in results['empty_files'].items():
        if empty_files:
            print(f"   ❌ {dir_type}: {len(empty_files)} empty files")
            total_empty += len(empty_files)
        else:
            print(f"   ✅ {dir_type}: No empty files")
    
    if total_empty == 0:
        print("   🎉 EXCELLENT: No empty files found!")
    print()
    
    # Duplicate files check
    print("🔍 DUPLICATE FILES CHECK:")
    total_duplicates = 0
    for dir_type, duplicate_files in results['duplicate_files'].items():
        if duplicate_files:
            print(f"   ❌ {dir_type}: {len(duplicate_files)} duplicate patterns")
            total_duplicates += len(duplicate_files)
        else:
            print(f"   ✅ {dir_type}: No duplicates")
    
    if total_duplicates == 0:
        print("   🎉 EXCELLENT: No duplicate files found!")
    print()
    
    # Structure issues
    if results['structure_issues']:
        print("⚠️  STRUCTURE ISSUES:")
        for issue in results['structure_issues']:
            print(f"   - {issue}")
        print()
    
    # Final assessment
    print("🎯 FINAL ASSESSMENT:")
    if results['summary']['overall_status'] == 'PASS':
        print("   ✅ DATASET IS COMPLETE AND READY FOR USE!")
        print("   🎉 All validation checks passed successfully!")
    else:
        print("   ⚠️  ISSUES FOUND - Review recommended")
    
    print("\n" + "=" * 100)

def save_results(results, output_file="validation_results.json"):
    """Save detailed results to JSON file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"📄 Detailed results saved to: {output_file}")
    except Exception as e:
        print(f"⚠️  Error saving results: {e}")

def main():
    """Main function"""
    # Get data path from command line argument or use default
    data_path = sys.argv[1] if len(sys.argv) > 1 else get_default_path()
    
    # Check if data path exists
    if not Path(data_path).exists():
        print(f"❌ Error: Data path does not exist: {data_path}")
        print("\nPlease provide a valid path to your Data2025 directory:")
        print("python check.py /path/to/Data2025")
        sys.exit(1)
    
    # Create validator and run validation
    validator = DataValidator(data_path)
    results = validator.validate_all()
    
    # Print report
    print_report(results)
    
    # Save results
    save_results(results)
    
    # Exit with appropriate code
    if results['summary']['overall_status'] == 'PASS':
        print("🎉 Validation completed successfully!")
        sys.exit(0)
    else:
        print("⚠️  Validation completed with issues found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
