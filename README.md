# HCMC AI Data 2025 - Hệ Thống Kiểm Tra Dữ Liệu

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

## 🔍 Các Kiểm Tra Xác Thực

### Kiểm Tra Cơ Bản (`main.py`):
Hệ thống kiểm tra gốc thực hiện:
- **Kiểm Tra Số Lượng File** - Đếm file trong mỗi thư mục
- **Phát Hiện File Rỗng** - Tìm file 0KB hoặc có kích thước đáng ngờ
- **Phát Hiện Mẫu Trùng Lặp** - Tìm kiếm các mẫu đặt tên như `(1)`, `_copy`, v.v.
- **Phân Tích Phân Bố Cấp Độ** - Phân tích phân bố video theo các cấp độ
- **Tương Thích Đa Nền Tảng** - Hoạt động trên Windows, macOS, và Linux

### Kiểm Tra Toàn Diện (`comprehensive_check.py`) - **KHUYẾN NGHỊ**:
Hệ thống kiểm tra nâng cao bổ sung **kiểm tra tính nhất quán đa thư mục**:

#### 1. **Tính Nhất Quán Đa Thư Mục**
- ✅ **Xác thực mối quan hệ** giữa video và các file tương ứng
- ✅ **Kiểm tra tất cả 6 thư mục**: video, keyframes, map-keyframes, media-info, objects, clip-features-32
- ✅ **Xác định file thiếu** - nếu video tồn tại nhưng thiếu file tương ứng trong các thư mục khác
- ✅ **Phát hiện file mồ côi** - file không tương ứng với video nào

#### 2. **Phát Hiện Trùng Lặp Nâng Cao**
- ✅ **Trùng lặp đa thư mục** - tìm file trùng lặp trên tất cả các thư mục
- ✅ **Trùng lặp theo video** - xác định nhiều file cho cùng một video trong cùng thư mục

#### 3. **Phân Tích File Toàn Diện**
- ✅ **Xác thực kích thước file** - kiểm tra file rỗng hoặc bị hỏng
- ✅ **Tính nhất quán đặt tên** - xác thực mẫu đặt tên file
- ✅ **Xác thực cấu trúc** - đảm bảo cấu trúc thư mục đúng

#### 4. **Báo Cáo Chi Tiết**
- ✅ **Báo cáo file thiếu** - danh sách chi tiết file thiếu theo video
- ✅ **Vấn đề đa thư mục** - các vấn đề cụ thể giữa các thư mục
- ✅ **Thống kê toàn diện** - tổng file, video, file thiếu, v.v.

## 📊 Cấu Trúc Dữ Liệu Mong Đợi

Hệ thống kiểm tra mong đợi cấu trúc thư mục này:

```
Data2025/
├── video/                    # 873 file .mp4
├── keyframes/               # 873 thư mục với file .jpg
├── clip-features-32/        # 873 file .npy
├── map-keyframes/           # 873 file .csv
├── media-info/              # 873 file .json
└── objects/                 # 873 thư mục với file .json
```

## 🎯 Kết Quả Mong Đợi

### Bộ Dữ Liệu Hoàn Hảo Sẽ Hiển Thị:
- **Tổng số file**: ~178,194 file
- **Videos**: 873 file .mp4
- **Keyframes**: 177,321 file .jpg
- **Features**: 873 file .npy
- **Maps**: 873 file .csv
- **Media Info**: 873 file .json
- **Objects**: 177,321 file .json
- **File rỗng**: 0
- **Mẫu trùng lặp**: 0
- **Trạng thái tổng thể**: PASS

## 📋 File Đầu Ra

### Đầu Ra Console
Script cung cấp cập nhật tiến trình thời gian thực và báo cáo cuối cùng toàn diện.

### Kết Quả JSON
Lưu kết quả chi tiết vào `validation_results.json` bao gồm:
- Số lượng file theo loại
- Danh sách file rỗng
- Mẫu file trùng lặp
- Phân tích phân bố cấp độ
- Vấn đề cấu trúc
- Thống kê tóm tắt

## 🔧 Xử Lý Sự Cố

### Các Vấn Đề Thường Gặp:

1. **Lỗi không tìm thấy đường dẫn**
   ```
   ❌ Lỗi: Đường dẫn dữ liệu không tồn tại: /path/to/Data2025
   ```
   **Giải pháp**: Cung cấp đường dẫn chính xác đến thư mục Data2025

2. **Từ chối quyền truy cập**
   ```
   Lỗi quét video: Từ chối quyền truy cập
   ```
   **Giải pháp**: Đảm bảo bạn có quyền đọc thư mục dữ liệu

3. **Lỗi import**
   ```
   ModuleNotFoundError: No module named 'data_validator'
   ```
   **Giải pháp**: Đảm bảo `data_validator.py` nằm trong cùng thư mục với `check.py`

## 🎉 Chỉ Báo Thành Công

Khi kiểm tra thành công, bạn sẽ thấy:

```
🎯 ĐÁNH GIÁ CUỐI CÙNG:
   ✅ BỘ DỮ LIỆU HOÀN CHỈNH VÀ SẴN SÀNG SỬ DỤNG!
   🎉 Tất cả các kiểm tra xác thực đã thành công!

🎉 Kiểm tra hoàn thành thành công!
```

## 📈 Ví Dụ Đầu Ra

```
📊 BÁO CÁO KIỂM TRA DỮ LIỆU AI HCMC
====================================================================================================

📈 THỐNG KÊ TÓM TẮT:
   Tổng số file: 178,194
   File rỗng: 0
   Mẫu trùng lặp: 0
   Vấn đề cấu trúc: 0
   Trạng thái tổng thể: PASS

📁 SỐ LƯỢNG FILE THEO LOẠI:
   Videos: 873
   Keyframes: 177,321
   Features: 873
   Maps: 873
   Media Info: 873
   Objects: 177,321

📊 PHÂN BỐ CẤP ĐỘ:
   L21: 29 video
   L22: 31 video
   L23: 25 video
   L24: 43 video
   L25: 88 video
   L26: 498 video
   L27: 16 video
   L28: 24 video
   L29: 23 video
   L30: 96 video

🔍 KIỂM TRA FILE RỖNG:
   ✅ videos: Không có file rỗng
   ✅ keyframes: Không có file rỗng
   ✅ features: Không có file rỗng
   ✅ maps: Không có file rỗng
   ✅ media_info: Không có file rỗng
   ✅ objects: Không có file rỗng
   🎉 TUYỆT VỜI: Không tìm thấy file rỗng!

🔍 KIỂM TRA FILE TRÙNG LẶP:
   ✅ videos: Không có trùng lặp
   ✅ keyframes: Không có trùng lặp
   ✅ features: Không có trùng lặp
   ✅ maps: Không có trùng lặp
   ✅ media_info: Không có trùng lặp
   ✅ objects: Không có trùng lặp
   🎉 TUYỆT VỜI: Không tìm thấy file trùng lặp!

🎯 ĐÁNH GIÁ CUỐI CÙNG:
   ✅ BỘ DỮ LIỆU HOÀN CHỈNH VÀ SẴN SÀNG SỬ DỤNG!
   🎉 Tất cả các kiểm tra xác thực đã thành công!
```

## 🤝 Đóng Góp

Để thêm các kiểm tra xác thực mới:

1. Thêm phương thức mới vào lớp `DataValidator` trong `data_validator.py`
2. Gọi các phương thức mới trong hàm `validate_all()`
3. Cập nhật các hàm báo cáo trong `check.py` để hiển thị kết quả mới

## 📞 Hỗ Trợ

Nếu bạn gặp bất kỳ vấn đề nào:

1. Kiểm tra rằng tất cả file đều nằm trong cùng thư mục
2. Xác minh đường dẫn dữ liệu là chính xác
3. Đảm bảo bạn có quyền đọc thư mục dữ liệu
4. Kiểm tra đầu ra console để biết thông báo lỗi cụ thể

---

**Chúc bạn kiểm tra thành công! 🚀**
