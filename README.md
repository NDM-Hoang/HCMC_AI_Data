# HCMC AI Data 2025 - Data Validation System

A comprehensive, cross-platform data validation system for the HCMC AI Data 2025 dataset.

## 🚀 Quick Start

### For Windows Users:
```bash
python main.py "C:\path\to\Data2025"
```

### For macOS Users:
```bash
python main.py "/Volumes/Data/HCMC_AI_Data/Data2025"
```

### For Linux Users:
```bash
python main.py "/run/media/rin/New Volume/HCMC_AI_Data/Data2025"
```

### Using Default Path (Auto-detected):
```bash
python main.py
```

## 📁 File Structure

```
HCMC_AI_Data/
├── main.py                 # Main entry point
├── src/
│   ├── __init__.py
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── data_validator.py      # Core validation functions
│   │   ├── duplicate_file_checker.py
│   │   ├── data_validation.py
│   │   └── detailed_analysis.py
│   └── utils/
│       ├── __init__.py
│       └── check.py              # Utility functions
├── reports/               # Generated reports and results
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## 🔍 What the Validation Checks

The system performs comprehensive validation including:

### 1. **File Count Validation**
- Counts all files in each directory
- Verifies expected file counts
- Checks for missing files

### 2. **Empty File Detection**
- Finds files with 0KB size
- Identifies suspiciously small files (<1KB)
- Reports corrupted or incomplete files

### 3. **Duplicate File Detection**
- Searches for files with patterns like `(1)`, `(2)`, `_copy`, `_duplicate`
- Identifies backup files and version duplicates
- Reports any duplicate naming patterns

### 4. **Data Structure Analysis**
- Analyzes video distribution across levels (L21-L30)
- Identifies gaps in video numbering
- Validates directory structure

### 5. **Cross-Platform Compatibility**
- Works on Windows, macOS, and Linux
- Auto-detects operating system
- Uses appropriate default paths

## 📊 Expected Data Structure

The validation expects this directory structure:

```
Data2025/
├── video/                    # 873 .mp4 files
├── keyframes/               # 873 directories with .jpg files
├── clip-features-32/        # 873 .npy files
├── map-keyframes/           # 873 .csv files
├── media-info/              # 873 .json files
└── objects/                 # 873 directories with .json files
```

## 🎯 Expected Results

### Perfect Dataset Should Show:
- **Total files**: ~178,194 files
- **Videos**: 873 .mp4 files
- **Keyframes**: 177,321 .jpg files
- **Features**: 873 .npy files
- **Maps**: 873 .csv files
- **Media Info**: 873 .json files
- **Objects**: 177,321 .json files
- **Empty files**: 0
- **Duplicate patterns**: 0
- **Overall status**: PASS

## 📋 Output Files

### Console Output
The script provides real-time progress updates and a comprehensive final report.

### JSON Results
Saves detailed results to `validation_results.json` including:
- File counts by type
- Empty file lists
- Duplicate file patterns
- Level distribution analysis
- Structure issues
- Summary statistics

## 🔧 Troubleshooting

### Common Issues:

1. **Path not found error**
   ```
   ❌ Error: Data path does not exist: /path/to/Data2025
   ```
   **Solution**: Provide the correct path to your Data2025 directory

2. **Permission denied**
   ```
   Error scanning video: Permission denied
   ```
   **Solution**: Ensure you have read permissions for the data directory

3. **Import error**
   ```
   ModuleNotFoundError: No module named 'data_validator'
   ```
   **Solution**: Ensure `data_validator.py` is in the same directory as `check.py`

## 🎉 Success Indicators

When validation passes successfully, you'll see:

```
🎯 FINAL ASSESSMENT:
   ✅ DATASET IS COMPLETE AND READY FOR USE!
   🎉 All validation checks passed successfully!

🎉 Validation completed successfully!
```

## 📈 Sample Output

```
📊 HCMC AI DATA VALIDATION REPORT
====================================================================================================

📈 SUMMARY STATISTICS:
   Total files: 178,194
   Empty files: 0
   Duplicate patterns: 0
   Structure issues: 0
   Overall status: PASS

📁 FILE COUNTS BY TYPE:
   Videos: 873
   Keyframes: 177,321
   Features: 873
   Maps: 873
   Media Info: 873
   Objects: 177,321

📊 LEVEL DISTRIBUTION:
   L21: 29 videos
   L22: 31 videos
   L23: 25 videos
   L24: 43 videos
   L25: 88 videos
   L26: 498 videos
   L27: 16 videos
   L28: 24 videos
   L29: 23 videos
   L30: 96 videos

🔍 EMPTY FILES CHECK:
   ✅ videos: No empty files
   ✅ keyframes: No empty files
   ✅ features: No empty files
   ✅ maps: No empty files
   ✅ media_info: No empty files
   ✅ objects: No empty files
   🎉 EXCELLENT: No empty files found!

🔍 DUPLICATE FILES CHECK:
   ✅ videos: No duplicates
   ✅ keyframes: No duplicates
   ✅ features: No duplicates
   ✅ maps: No duplicates
   ✅ media_info: No duplicates
   ✅ objects: No duplicates
   🎉 EXCELLENT: No duplicate files found!

🎯 FINAL ASSESSMENT:
   ✅ DATASET IS COMPLETE AND READY FOR USE!
   🎉 All validation checks passed successfully!
```

## 🤝 Contributing

To add new validation checks:

1. Add new methods to the `DataValidator` class in `data_validator.py`
2. Call the new methods in the `validate_all()` function
3. Update the report functions in `check.py` to display the new results

## 📞 Support

If you encounter any issues:

1. Check that all files are in the same directory
2. Verify the data path is correct
3. Ensure you have read permissions for the data directory
4. Check the console output for specific error messages

---

**Happy validating! 🚀**
