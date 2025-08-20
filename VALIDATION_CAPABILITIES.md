# HCMC AI Data Validation Capabilities

## 🔍 Validation Overview

The HCMC AI Data validation system now provides **two levels of validation** to ensure your dataset is complete and consistent.

## 📊 Basic Validation (`main.py`)

The original validation system provides fundamental checks:

### ✅ What It Checks:
- **File Counts**: Counts files in each directory
- **Empty Files**: Finds 0KB or suspiciously small files (<1KB)
- **Duplicate Patterns**: Searches for naming patterns like `(1)`, `_copy`, `_duplicate`
- **Level Distribution**: Analyzes video distribution across levels (L21-L30)
- **Structure Issues**: Validates directory structure

### ⚠️ Limitations:
- **No cross-directory validation** - doesn't check relationships between directories
- **No missing file detection** - doesn't verify if videos have corresponding files in all directories
- **Basic duplicate detection** - only checks naming patterns, not actual file relationships

## 🚀 Comprehensive Validation (`comprehensive_check.py`) - **RECOMMENDED / KHUYẾN NGHỊ**

The enhanced validation system provides **complete cross-directory consistency checking**:

### ✅ What It Checks:

#### 1. **Cross-Directory Consistency**
- **Video-to-File Mapping**: Maps each video to its corresponding files across all 6 directories
- **Missing File Detection**: Identifies videos that lack corresponding files in other directories
- **Orphaned File Detection**: Finds files that don't correspond to any video
- **Complete Coverage**: Ensures every video has files in all expected directories

#### 2. **Enhanced Duplicate Detection**
- **Cross-Directory Duplicates**: Finds duplicate files across all directories
- **Video-Specific Duplicates**: Identifies multiple files for the same video in the same directory
- **Relationship Validation**: Ensures proper one-to-many relationships (video → multiple keyframes/objects)

#### 3. **Comprehensive File Analysis**
- **File Size Validation**: Checks for empty or corrupted files
- **Naming Consistency**: Validates file naming patterns across directories
- **Structure Validation**: Ensures proper directory structure and organization

#### 4. **Detailed Reporting**
- **Missing Files Report**: Detailed list of missing files per video
- **Cross-Directory Issues**: Specific issues between directories
- **Comprehensive Statistics**: Total files, videos, missing files, etc.

## 📁 Directory Structure Validation

The comprehensive validator checks these 6 directories:

```
Data2025/
├── video/                    # 873 .mp4 files
├── keyframes/               # 873 directories with .jpg files
├── clip-features-32/        # 873 .npy files
├── map-keyframes/           # 873 .csv files
├── media-info/              # 873 .json files
└── objects/                 # 873 directories with .json files
```

### 🔍 Cross-Directory Validation Logic:

For each video (e.g., `L21_V001`), the validator checks:

1. **Video File**: `video/L21_V001.mp4` exists
2. **Keyframes**: `keyframes/L21_V001/L21_V001_001.jpg`, `L21_V001_002.jpg`, etc. exist
3. **Features**: `clip-features-32/L21_V001.npy` exists
4. **Maps**: `map-keyframes/L21_V001.csv` exists
5. **Media Info**: `media-info/L21_V001.json` exists
6. **Objects**: `objects/L21_V001/L21_V001_001.json`, `L21_V001_002.json`, etc. exist

## 📊 Expected Results

### Perfect Dataset Should Show:
- **Total files**: ~358,134 files
- **Total videos**: 873 videos
- **Videos**: 873 .mp4 files
- **Keyframes**: 177,321 .jpg files
- **Features**: 873 .npy files
- **Maps**: 873 .csv files
- **Media Info**: 873 .json files
- **Objects**: 177,321 .json files
- **Missing files**: 0
- **Duplicate files**: 0
- **Empty files**: 0
- **Cross-directory issues**: 0
- **Overall status**: PASS

## 🎯 Usage Recommendations

### Use Basic Validation When:
- You want a quick overview of file counts
- You're checking for obvious issues (empty files, duplicate patterns)
- You need basic level distribution analysis

### Use Comprehensive Validation When:
- You need to ensure complete dataset integrity
- You want to verify cross-directory consistency
- You're preparing data for production use
- You need detailed missing file reports
- You want to validate the complete dataset structure

## 📈 Validation Reports

### Basic Validation Output:
- Console report with file counts and basic issues
- `validation_results.json` with detailed data

### Comprehensive Validation Output:
- Enhanced console report with cross-directory analysis
- `comprehensive_validation_results.json` with complete mapping
- `missing_files_report.md` with detailed missing file list
- Cross-directory consistency analysis
- Video-to-file relationship mapping

## 🔧 Technical Implementation

### Basic Validator (`DataValidator`):
- Scans directories independently
- Counts files per directory
- Checks individual file properties
- No cross-directory relationships

### Comprehensive Validator (`ComprehensiveValidator`):
- Builds complete video-to-file mapping
- Validates relationships across all directories
- Detects missing and orphaned files
- Provides detailed cross-directory analysis
- Generates comprehensive reports

## ✅ Validation Status Codes

### PASS:
- All files present and accounted for
- No missing files across directories
- No duplicate files
- No empty or corrupted files
- Complete cross-directory consistency

### ISSUES_FOUND:
- Missing files in one or more directories
- Duplicate files detected
- Empty or corrupted files found
- Cross-directory consistency issues
- Structure problems detected

## 🚀 Getting Started

### Quick Start:
```bash
# Basic validation
python main.py "/path/to/Data2025"

# Comprehensive validation (RECOMMENDED)
python comprehensive_check.py "/path/to/Data2025"
```

### Cross-Platform:
```bash
# Windows
python comprehensive_check.py "C:\path\to\Data2025"

# macOS
python comprehensive_check.py "/Volumes/Data/HCMC_AI_Data/Data2025"

# Linux
python comprehensive_check.py "/run/media/rin/New Volume/HCMC_AI_Data/Data2025"
```

The comprehensive validation ensures your dataset is **complete, consistent, and ready for production use**! 🎉

---

## 🖼️ Quality Evaluation (VN/EN)

### Unified Runner
```bash
python check_evaluate.py "/path/to/Data2025"
```

### What it does / Tính năng
- EN: Validates media-info fields; overlays object boxes with labels on keyframes; maps `n/frame_idx` to CSV and overlays `fps` + `pts_time`.
- VN: Kiểm tra `media-info` bắt buộc; vẽ bbox + nhãn đối tượng lên keyframe; đối sánh `n/frame_idx` với CSV và ghi `fps` + `pts_time`.

### Output
- Saves 5 random annotated images: `reports/data_quality_evaluation/overlays/random1..random5.jpg`.
- JSON summary: `reports/data_quality_evaluation_results.json`.
