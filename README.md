# HCMC AI Data 2025 - Data Validation System

Một hệ thống kiểm tra dữ liệu toàn diện, đa nền tảng cho bộ dữ liệu HCMC AI Data 2025.

## 🚀 Khởi Động Nhanh

### Kiểm Tra Cơ Bản (Gốc):
```bash
python main.py "/path/to/Data2025"
```

### Kiểm Tra Toàn Diện (Khuyến Nghị):
```bash
python comprehensive_check.py "/path/to/Data2025"
```

### Ví Dụ Đa Nền Tảng:

#### Windows:
```bash
python comprehensive_check.py "C:\path\to\Data2025"
```

#### macOS:
```bash
python comprehensive_check.py "/Volumes/Data/HCMC_AI_Data/Data2025"
```

#### Linux:
```bash
python comprehensive_check.py "/run/media/rin/New Volume/HCMC_AI_Data/Data2025"
```

### Sử Dụng Đường Dẫn Mặc Định (Tự Động Phát Hiện):
```bash
python comprehensive_check.py
```

## 📁 File Structure

```
HCMC_AI_Data/
├── main.py                    # Basic validation entry point
├── comprehensive_check.py     # 🚀 Comprehensive validation entry point (RECOMMENDED)
├── src/
│   ├── __init__.py
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── data_validator.py           # Basic validation functions
│   │   ├── comprehensive_validator.py  # 🔍 Cross-directory validation (NEW)
│   │   ├── duplicate_file_checker.py
│   │   ├── data_validation.py
│   │   └── detailed_analysis.py
│   └── utils/
│       ├── __init__.py
│       ├── check.py                    # Basic reporting functions
│       └── comprehensive_report.py     # 📊 Enhanced reporting (NEW)
├── reports/                  # Generated reports and results
├── requirements.txt          # Dependencies
└── README.md                # This file
```

## 🔍 Validation Checks

### Basic Validation (`main.py`):
Hệ thống kiểm tra gốc thực hiện:
- **File Count Validation** - Đếm file trong mỗi thư mục
- **Empty File Detection** - Tìm file 0KB hoặc có kích thước đáng ngờ
- **Duplicate Pattern Detection** - Tìm kiếm các mẫu đặt tên như `(1)`, `_copy`, v.v.
- **Level Distribution Analysis** - Phân tích phân bố video theo các cấp độ
- **Cross-Platform Compatibility** - Hoạt động trên Windows, macOS, và Linux

### Comprehensive Validation (`comprehensive_check.py`) - **KHUYẾN NGHỊ**:
Hệ thống kiểm tra nâng cao bổ sung **cross-directory consistency checking**:

#### 1. **Cross-Directory Consistency**
- ✅ **Validates relationships** giữa video và các file tương ứng
- ✅ **Checks all 6 directories**: video, keyframes, map-keyframes, media-info, objects, clip-features-32
- ✅ **Identifies missing files** - nếu video tồn tại nhưng thiếu file tương ứng trong các thư mục khác
- ✅ **Detects orphaned files** - file không tương ứng với video nào

#### 2. **Enhanced Duplicate Detection**
- ✅ **Cross-directory duplicates** - tìm file trùng lặp trên tất cả các thư mục
- ✅ **Video-specific duplicates** - xác định nhiều file cho cùng một video trong cùng thư mục

#### 3. **Comprehensive File Analysis**
- ✅ **File size validation** - kiểm tra file rỗng hoặc bị hỏng
- ✅ **Naming consistency** - xác thực mẫu đặt tên file
- ✅ **Structure validation** - đảm bảo cấu trúc thư mục đúng

#### 4. **Detailed Reporting**
- ✅ **Missing files report** - danh sách chi tiết file thiếu theo video
- ✅ **Cross-directory issues** - các vấn đề cụ thể giữa các thư mục
- ✅ **Comprehensive statistics** - tổng file, video, file thiếu, v.v.

## 📊 Expected Data Structure

Hệ thống kiểm tra mong đợi cấu trúc thư mục này:

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
Script cung cấp cập nhật tiến trình thời gian thực và báo cáo cuối cùng toàn diện.

### JSON Results
Lưu kết quả chi tiết vào `validation_results.json` bao gồm:
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
   ❌ Lỗi: Đường dẫn dữ liệu không tồn tại: /path/to/Data2025
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

Khi kiểm tra thành công, bạn sẽ thấy:

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

Để thêm các kiểm tra xác thực mới:

1. Add new methods to the `DataValidator` class in `data_validator.py`
2. Call the new methods in the `validate_all()` function
3. Update the report functions in `check.py` to display the new results

## 📞 Support

Nếu bạn gặp bất kỳ vấn đề nào:

1. Check that all files are in the same directory
2. Verify the data path is correct
3. Ensure you have read permissions for the data directory
4. Check the console output for specific error messages

---

**Happy validating! 🚀**
