#!/usr/bin/env python3
"""
Trình tạo báo cáo kiểm tra toàn diện
"""

import json
from pathlib import Path

def print_comprehensive_report(results):
    """In báo cáo kiểm tra toàn diện"""
    print("=" * 120)
    print("📊 BÁO CÁO KIỂM TRA TOÀN DIỆN DỮ LIỆU AI HCMC")
    print("=" * 120)
    print()
    
    # Thống kê tóm tắt
    print("📈 THỐNG KÊ TÓM TẮT:")
    print(f"   Tổng số file: {results['summary']['total_files']:,}")
    print(f"   Tổng số video: {results['summary']['total_videos']}")
    print(f"   File rỗng: {results['summary']['total_empty_files']}")
    print(f"   Mẫu trùng lặp: {results['summary']['total_duplicate_patterns']}")
    print(f"   File thiếu: {results['summary']['total_missing_files']}")
    print(f"   Vấn đề đa thư mục: {results['summary']['total_cross_directory_issues']}")
    print(f"   Vấn đề cấu trúc: {results['summary']['structure_issues_count']}")
    print(f"   Trạng thái tổng thể: {results['summary']['overall_status']}")
    print()
    
    # Số lượng file theo loại
    print("📁 SỐ LƯỢNG FILE THEO LOẠI:")
    for dir_type, count in results['file_counts'].items():
        print(f"   {dir_type.replace('_', ' ').title()}: {count:,}")
    print()
    
    # Kiểm tra tính nhất quán đa thư mục
    print("🔍 KIỂM TRA TÍNH NHẤT QUÁN ĐA THƯ MỤC:")
    if results['missing_files']:
        total_missing = 0
        for dir_type, videos in results['missing_files'].items():
            if videos:
                print(f"   ❌ {dir_type}: {len(videos)} video thiếu file")
                total_missing += len(videos)
        print(f"   ⚠️  Tổng số file thiếu: {total_missing}")
    else:
        print("   ✅ Tất cả video đều có file tương ứng trong tất cả các thư mục")
    print()
    
    # Kiểm tra file trùng lặp
    print("🔍 KIỂM TRA FILE TRÙNG LẶP:")
    if results['duplicate_files']:
        total_duplicates = 0
        for dir_type, duplicates in results['duplicate_files'].items():
            if duplicates:
                print(f"   ❌ {dir_type}: {len(duplicates)} video có file trùng lặp")
                total_duplicates += len(duplicates)
        print(f"   ⚠️  Tổng số vấn đề trùng lặp: {total_duplicates}")
    else:
        print("   ✅ Không tìm thấy file trùng lặp")
    print()
    
    # Kiểm tra file rỗng
    print("🔍 KIỂM TRA FILE RỖNG:")
    if results['empty_files']:
        total_empty = 0
        for dir_type, empty_list in results['empty_files'].items():
            if empty_list:
                print(f"   ❌ {dir_type}: {len(empty_list)} file rỗng")
                total_empty += len(empty_list)
        print(f"   ⚠️  Tổng số file rỗng: {total_empty}")
    else:
        print("   ✅ Không tìm thấy file rỗng")
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
    
    # Chi tiết vấn đề đa thư mục
    if results['cross_directory_issues']:
        print("⚠️  VẤN ĐỀ ĐA THƯ MỤC:")
        for issue in results['cross_directory_issues'][:10]:  # Hiển thị 10 vấn đề đầu tiên
            print(f"   - {issue}")
        if len(results['cross_directory_issues']) > 10:
            print(f"   ... và {len(results['cross_directory_issues']) - 10} vấn đề khác")
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
        print("   ✅ Tất cả video đều có file tương ứng trong tất cả các thư mục")
        print("   ✅ Không có file trùng lặp hoặc thiếu")
    else:
        print("   ⚠️  PHÁT HIỆN VẤN ĐỀ - Cần xem xét")
        if results['summary']['total_missing_files'] > 0:
            print(f"   ❌ {results['summary']['total_missing_files']} file thiếu cần chú ý")
        if results['summary']['total_duplicate_patterns'] > 0:
            print(f"   ❌ {results['summary']['total_duplicate_patterns']} file trùng lặp cần chú ý")
        if results['summary']['total_empty_files'] > 0:
            print(f"   ❌ {results['summary']['total_empty_files']} file rỗng cần chú ý")
    
    print("\n" + "=" * 120)

def save_comprehensive_results(results, output_file="reports/comprehensive_validation_results.json"):
    """Lưu kết quả toàn diện vào file JSON"""
    try:
        # Đảm bảo thư mục reports tồn tại
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"📄 Kết quả toàn diện đã lưu vào: {output_file}")
    except Exception as e:
        print(f"⚠️  Lỗi khi lưu kết quả toàn diện: {e}")

def generate_missing_files_report(results, output_file="reports/missing_files_report.md"):
    """Tạo báo cáo chi tiết về các file thiếu"""
    try:
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Báo Cáo File Thiếu - Dữ Liệu AI HCMC 2025\n\n")
            f.write(f"Được tạo: {results['validation_time']}\n")
            f.write(f"Đường dẫn dữ liệu: {results['data_path']}\n\n")
            
            if results['missing_files']:
                f.write("## Tóm Tắt File Thiếu\n\n")
                for dir_type, videos in results['missing_files'].items():
                    if videos:
                        f.write(f"### {dir_type.replace('_', ' ').title()}\n")
                        f.write(f"- **Thiếu file cho {len(videos)} video**\n\n")
                        f.write("| Video | Trạng thái |\n")
                        f.write("|-------|------------|\n")
                        for video in sorted(videos):
                            f.write(f"| {video} | ❌ Thiếu |\n")
                        f.write("\n")
            else:
                f.write("## ✅ Không Tìm Thấy File Thiếu\n\n")
                f.write("Tất cả video đều có file tương ứng trong tất cả các thư mục.\n")
        
        print(f"📄 Báo cáo file thiếu đã lưu vào: {output_file}")
    except Exception as e:
        print(f"⚠️  Lỗi khi lưu báo cáo file thiếu: {e}")
