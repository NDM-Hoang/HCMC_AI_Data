#!/usr/bin/env python3
"""
Unified Data Check & Evaluation Runner

Usage:
  python check_evaluate.py "/path/to/Data2025"

This script performs:
  1) Structural validation (counts, empty files, duplicates, distribution)
  2) Data quality evaluation (media-info fields, object overlays, map-keyframe timing)

Outputs:
  - reports/validation_results.json
  - reports/data_quality_evaluation/overlays/random1.jpg .. random5.jpg
  - reports/data_quality_evaluation_results.json
"""

import sys
from pathlib import Path

from src.utils.check import get_default_path, print_report, save_results
from src.validators.data_validator import DataValidator
from src.validators.data_quality_evaluator import DataQualityEvaluator


def main():
    data_path = sys.argv[1] if len(sys.argv) > 1 else get_default_path()
    if not Path(data_path).exists():
        print(f"❌ Lỗi: Đường dẫn dữ liệu không tồn tại: {data_path}")
        print("\nVui lòng cung cấp đường dẫn hợp lệ đến thư mục Data2025:")
        print("python check_evaluate.py /path/to/Data2025")
        sys.exit(1)

    # Phase 1: Structural validation
    print("\n===== PHASE 1: STRUCTURAL VALIDATION =====")
    validator = DataValidator(data_path)
    results = validator.validate_all()
    print_report(results)
    save_results(results)

    # Phase 2: Quality evaluation with compact storage (save 5 random annotated images)
    print("\n===== PHASE 2: DATA QUALITY EVALUATION =====")
    evaluator = DataQualityEvaluator(data_path)
    evaluator.evaluate(
        max_frames_per_video=3,
        score_threshold=0.3,
        display_only=False,
        save_overlays=True,
        cleanup_outputs=True,
        save_per_video_previews=False,
        save_annotated_per_video=False,
        num_random_saves=5
    )
    print("\n✅ Hoàn thành. Ảnh minh hoạ được lưu tại reports/data_quality_evaluation/overlays/random1..random5.jpg")


if __name__ == "__main__":
    main()


