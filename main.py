#!/usr/bin/env python3
"""
HCMC AI Data 2025 - Điểm Vào Chính
Kiểm tra đa nền tảng (Linux, Mac, Windows)

Cách sử dụng:
    python main.py [data_path]
    
Ví dụ:
    python main.py "/path/to/Data2025"
    python main.py  # Sử dụng đường dẫn mặc định
"""

import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.check import get_default_path, print_report, save_results
from src.validators.data_validator import DataValidator

def main():
    """Hàm chính"""
    # Lấy đường dẫn dữ liệu từ tham số dòng lệnh hoặc sử dụng mặc định
    data_path = sys.argv[1] if len(sys.argv) > 1 else get_default_path()
    
    # Kiểm tra xem đường dẫn dữ liệu có tồn tại không
    if not Path(data_path).exists():
        print(f"❌ Lỗi: Đường dẫn dữ liệu không tồn tại: {data_path}")
        print("\nVui lòng cung cấp đường dẫn hợp lệ đến thư mục Data2025:")
        print("python main.py /path/to/Data2025")
        sys.exit(1)
    
    # Tạo trình kiểm tra và chạy kiểm tra
    validator = DataValidator(data_path)
    results = validator.validate_all()
    
    # In báo cáo
    print_report(results)
    
    # Lưu kết quả vào thư mục reports
    save_results(results, "reports/validation_results.json")
    
    # Thoát với mã phù hợp
    if results['summary']['overall_status'] == 'PASS':
        print("🎉 Kiểm tra hoàn thành thành công!")
        sys.exit(0)
    else:
        print("⚠️  Kiểm tra hoàn thành với các vấn đề được phát hiện.")
        sys.exit(1)

if __name__ == "__main__":
    main()
