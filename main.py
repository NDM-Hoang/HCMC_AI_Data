#!/usr/bin/env python3
"""
HCMC AI Data 2025 - Main Entry Point
Cross-platform (Linux, Mac, Windows) validation

Usage:
    python main.py [data_path]
    
Example:
    python main.py "/path/to/Data2025"
    python main.py  # Uses default path
"""

import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.check import get_default_path, print_report, save_results
from src.validators.data_validator import DataValidator

def main():
    """Main function"""
    # Get data path from command line argument or use default
    data_path = sys.argv[1] if len(sys.argv) > 1 else get_default_path()
    
    # Check if data path exists
    if not Path(data_path).exists():
        print(f"❌ Error: Data path does not exist: {data_path}")
        print("\nPlease provide a valid path to your Data2025 directory:")
        print("python main.py /path/to/Data2025")
        sys.exit(1)
    
    # Create validator and run validation
    validator = DataValidator(data_path)
    results = validator.validate_all()
    
    # Print report
    print_report(results)
    
    # Save results to reports directory
    save_results(results, "reports/validation_results.json")
    
    # Exit with appropriate code
    if results['summary']['overall_status'] == 'PASS':
        print("🎉 Validation completed successfully!")
        sys.exit(0)
    else:
        print("⚠️  Validation completed with issues found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
