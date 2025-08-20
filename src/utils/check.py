#!/usr/bin/env python3
"""
HCMC AI Data 2025 - Script Kiểm Tra Chính
Kiểm tra đa nền tảng (Linux, Mac, Windows)

Cách sử dụng:
    python check.py [data_path]
    
Ví dụ:
    python check.py "/path/to/Data2025"
    python check.py  # Sử dụng đường dẫn mặc định
"""

import sys
import json
from pathlib import Path
from ..validators.data_validator import DataValidator
from ..validators.data_quality_evaluator import DataQualityEvaluator

def get_default_path():
    """Lấy đường dẫn dữ liệu mặc định dựa trên hệ điều hành"""
    if sys.platform.startswith('win'):
        return "C:/HCMC_AI_Data/Data2025"
    elif sys.platform.startswith('darwin'):
        return "/Volumes/Data/HCMC_AI_Data/Data2025"
    else:
        return "/run/media/rin/New Volume/HCMC_AI_Data/Data2025"

def print_report(results):
    """In báo cáo kiểm tra toàn diện"""
    print("=" * 100)
    print("📊 BÁO CÁO KIỂM TRA DỮ LIỆU AI HCMC")
    print("=" * 100)
    print()
    
    # Thống kê tóm tắt
    print("📈 THỐNG KÊ TÓM TẮT:")
    print(f"   Tổng số file: {results['summary']['total_files']:,}")
    print(f"   File rỗng: {results['summary']['total_empty_files']}")
    print(f"   Mẫu trùng lặp: {results['summary']['total_duplicate_patterns']}")
    print(f"   Vấn đề cấu trúc: {results['summary']['structure_issues_count']}")
    print(f"   Trạng thái tổng thể: {results['summary']['overall_status']}")
    print()
    
    # Số lượng file theo loại
    print("📁 SỐ LƯỢNG FILE THEO LOẠI:")
    for dir_type, count in results['file_counts'].items():
        print(f"   {dir_type.replace('_', ' ').title()}: {count:,}")
    print()
    
    # Phân bố cấp độ
    print("📊 PHÂN BỐ CẤP ĐỘ:")
    for level in sorted(results['level_distribution']['counts'].keys()):
        count = results['level_distribution']['counts'][level]
        print(f"   L{level}: {count} video")
    
    if results['level_distribution']['gaps']:
        print("\n   ⚠️  KHOẢNG TRỐNG TRONG ĐÁNH SỐ VIDEO:")
        for level, gaps in results['level_distribution']['gaps'].items():
            print(f"     L{level}: Thiếu video {gaps}")
    print()
    
    # Kiểm tra file rỗng
    print("🔍 KIỂM TRA FILE RỖNG:")
    total_empty = 0
    for dir_type, empty_files in results['empty_files'].items():
        if empty_files:
            print(f"   ❌ {dir_type}: {len(empty_files)} file rỗng")
            total_empty += len(empty_files)
        else:
            print(f"   ✅ {dir_type}: Không có file rỗng")
    
    if total_empty == 0:
        print("   🎉 TUYỆT VỜI: Không tìm thấy file rỗng!")
    print()
    
    # Kiểm tra file trùng lặp
    print("🔍 KIỂM TRA FILE TRÙNG LẶP:")
    total_duplicates = 0
    for dir_type, duplicate_files in results['duplicate_files'].items():
        if duplicate_files:
            print(f"   ❌ {dir_type}: {len(duplicate_files)} mẫu trùng lặp")
            total_duplicates += len(duplicate_files)
        else:
            print(f"   ✅ {dir_type}: Không có trùng lặp")
    
    if total_duplicates == 0:
        print("   🎉 TUYỆT VỜI: Không tìm thấy file trùng lặp!")
    print()
    
    # Vấn đề cấu trúc
    if results['structure_issues']:
        print("⚠️  VẤN ĐỀ CẤU TRÚC:")
        for issue in results['structure_issues']:
            print(f"   - {issue}")
        print()
    
    # Đánh giá cuối cùng
    print("🎯 ĐÁNH GIÁ CUỐI CÙNG:")
    if results['summary']['overall_status'] == 'PASS':
        print("   ✅ BỘ DỮ LIỆU HOÀN CHỈNH VÀ SẴN SÀNG SỬ DỤNG!")
        print("   🎉 Tất cả các kiểm tra xác thực đã thành công!")
    else:
        print("   ⚠️  PHÁT HIỆN VẤN ĐỀ - Cần xem xét")
    
    print("\n" + "=" * 100)

def save_results(results, output_file="validation_results.json"):
    """Lưu kết quả chi tiết vào file JSON"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"📄 Kết quả chi tiết đã lưu vào: {output_file}")
    except Exception as e:
        print(f"⚠️  Lỗi khi lưu kết quả: {e}")

def main():
    """Hàm chính"""
    # Lấy đường dẫn dữ liệu từ tham số dòng lệnh hoặc sử dụng mặc định
    data_path = sys.argv[1] if len(sys.argv) > 1 else get_default_path()
    
    # Kiểm tra xem đường dẫn dữ liệu có tồn tại không
    if not Path(data_path).exists():
        print(f"❌ Lỗi: Đường dẫn dữ liệu không tồn tại: {data_path}")
        print("\nVui lòng cung cấp đường dẫn hợp lệ đến thư mục Data2025:")
        print("python check.py /path/to/Data2025")
        sys.exit(1)
    
    # Tạo trình kiểm tra và chạy kiểm tra
    validator = DataValidator(data_path)
    results = validator.validate_all()
    
    # In báo cáo
    print_report(results)
    
    # Lưu kết quả
    save_results(results)

    # Giai đoạn 2: Đánh giá chất lượng (media-info, overlay objects lên keyframes)
    print("\n🔎 Đang đánh giá chất lượng dữ liệu (media-info, keyframes, objects, maps)...")
    try:
        evaluator = DataQualityEvaluator(data_path)
        # Hiển thị ngẫu nhiên 5 ảnh đã có annotation trên toàn bộ dataset, không lưu ảnh để tiết kiệm dung lượng
        eval_results = evaluator.evaluate(
            max_frames_per_video=3,
            score_threshold=0.3,
            display_only=False,
            save_overlays=True,
            cleanup_outputs=True,
            save_per_video_previews=False,
            save_annotated_per_video=False,
            num_random_saves=5
        )
        print("✅ Hoàn thành đánh giá chất lượng. Đã lưu 5 ảnh ngẫu nhiên (random1..random5.jpg) trong reports/data_quality_evaluation/overlays/.")
    except Exception as e:
        print(f"⚠️  Lỗi khi đánh giá chất lượng dữ liệu: {e}")
    
    # Thoát với mã phù hợp
    if results['summary']['overall_status'] == 'PASS':
        print("🎉 Kiểm tra hoàn thành thành công!")
        sys.exit(0)
    else:
        print("⚠️  Kiểm tra hoàn thành với các vấn đề được phát hiện.")
        sys.exit(1)

if __name__ == "__main__":
    main()
