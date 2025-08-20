#!/usr/bin/env python3
"""
HCMC AI Data 2025 - Script Kiểm Tra Toàn Diện
Kiểm tra đa nền tảng với tính nhất quán đa thư mục

Cách sử dụng:
    python comprehensive_check.py [data_path]
    
Ví dụ:
    python comprehensive_check.py "/path/to/Data2025"
    python comprehensive_check.py  # Sử dụng đường dẫn mặc định
"""

import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.check import get_default_path
from src.utils.comprehensive_report import (
    print_comprehensive_report, 
    save_comprehensive_results, 
    generate_missing_files_report
)
from src.validators.comprehensive_validator import ComprehensiveValidator

def main():
    """Hàm chính cho kiểm tra toàn diện"""
    # Lấy đường dẫn dữ liệu từ tham số dòng lệnh hoặc sử dụng mặc định
    data_path = sys.argv[1] if len(sys.argv) > 1 else get_default_path()
    
    # Kiểm tra xem đường dẫn dữ liệu có tồn tại không
    if not Path(data_path).exists():
        print(f"❌ Lỗi: Đường dẫn dữ liệu không tồn tại: {data_path}")
        print("\nVui lòng cung cấp đường dẫn hợp lệ đến thư mục Data2025:")
        print("python comprehensive_check.py /path/to/Data2025")
        sys.exit(1)
    
    # Tạo trình kiểm tra toàn diện và chạy kiểm tra
    validator = ComprehensiveValidator(data_path)
    results = validator.validate_all()
    
    # In báo cáo toàn diện
    print_comprehensive_report(results)
    
    # Lưu kết quả toàn diện
    save_comprehensive_results(results)
    
    # Tạo báo cáo file thiếu
    generate_missing_files_report(results)
    
    # Thoát với mã phù hợp
    if results['summary']['overall_status'] == 'PASS':
        print("🎉 Kiểm tra toàn diện hoàn thành thành công!")
        sys.exit(0)
    else:
        print("⚠️  Kiểm tra toàn diện hoàn thành với các vấn đề được phát hiện.")
        sys.exit(1)

if __name__ == "__main__":
    main()
