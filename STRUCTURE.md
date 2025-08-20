# HCMC AI Data - Project Structure

## 📁 New Organized Structure / Cấu trúc dự án

```
HCMC_AI_Data/
├── main.py                    # 🚀 Basic validation entry point
├── comprehensive_check.py     # 🔍 Comprehensive validation entry point (RECOMMENDED)
├── check_evaluate.py          # ✅ Unified check + quality evaluation runner (NEW)
├── src/                       # 📦 Source code package
│   ├── __init__.py
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── data_validator.py           # Basic validation functions
│   │   ├── comprehensive_validator.py  # Cross-directory validation
│   │   ├── data_quality_evaluator.py   # 🖼️ Quality evaluator (media-info, objects ↔ keyframes, maps)
│   │   ├── duplicate_file_checker.py
│   │   ├── data_validation.py
│   │   └── detailed_analysis.py
│   └── utils/
│       ├── __init__.py
│       ├── check.py                    # Reporting utilities
│       └── comprehensive_report.py     # Enhanced reporting
├── reports/                  # 📊 Generated reports and results
│   ├── validation_results.json
│   ├── data_quality_evaluation_results.json
│   └── data_quality_evaluation/
│       └── overlays/
│           ├── random1.jpg .. random5.jpg
├── requirements.txt          # 📋 Dependencies
├── README.md                 # 📖 Main documentation
└── STRUCTURE.md              # 📋 This file
```

## 🚀 Run / Chạy

- Unified (VN/EN): `python check_evaluate.py "/path/to/Data2025"`
- Basic: `python main.py "/path/to/Data2025"`
- Comprehensive: `python comprehensive_check.py "/path/to/Data2025"`

## 🔄 Migration Summary

### What Changed:
1. **Moved all validation modules** to `src/validators/`
2. **Moved utility functions** to `src/utils/`
3. **Created proper Python packages** with `__init__.py` files
4. **Organized reports** into `reports/` directory
5. **Created new entry point** `main.py` instead of `check.py`
6. **Updated imports** to use relative imports within packages

### Benefits:
- ✅ **Better organization** - Clear separation of concerns
- ✅ **Modular design** - Easy to maintain and extend
- ✅ **Professional structure** - Follows Python best practices
- ✅ **Clean imports** - Proper package structure
- ✅ **Scalable** - Easy to add new modules

## 📦 Package Structure

### Validators Package (`src/validators/`)
- **DataValidator**: Basic validation functions
- **ComprehensiveValidator**: Cross-directory validation (NEW)
- **DuplicateFileChecker**: Duplicate file detection
- **HCMCDataValidator**: Comprehensive data validation
- **DetailedDataAnalyzer**: Detailed analysis functions

### Utils Package (`src/utils/`)
- **check.py**: Basic reporting functions
- **comprehensive_report.py**: Enhanced reporting for cross-directory validation (NEW)
- **print_report()**: Generate formatted reports
- **print_comprehensive_report()**: Generate comprehensive reports
- **save_results()**: Save results to files
- **get_default_path()**: Cross-platform path detection

## 🔧 Import Examples

```python
# Import specific validator
from src.validators.data_validator import DataValidator

# Import utility functions
from src.utils.check import print_report, save_results

# Import all validators
from src.validators import DataValidator, DuplicateFileChecker
```

## ✅ Verification

The new structure has been tested and verified:
- ✅ All imports work correctly
- ✅ Main entry point functions properly
- ✅ Package structure is valid
- ✅ No broken dependencies
- ✅ Clean organization maintained

## 🎯 Next Steps

The project is now ready for:
- Adding new validation modules
- Extending functionality
- Better testing structure
- Documentation improvements
