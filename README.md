# python-fundamentals

Dasar-dasar Python untuk ingeniero sipil yang beralih ke BIM/Construction Tech.

## Progress
- [x] Minggu 1-2: Python fundamentals + environment setup
- [ ] Minggu 3-4: Data analysis & visualization (pandas, plotly)
- [ ] Minggu 5-6: Git & GitHub workflow profesional
- [ ] Minggu 7-8: Revit API + PyRevit
- [ ] Minggu 9-10: Dynamo + Python Node
- [ ] Minggu 11-12: Portfolio polish + job ready

## Structure
```
python-fundamentals/
├── .gitignore
├── README.md
├── requirements.txt
├── pyproject.toml
├── scripts/
│   ├── excel_to_json.py      # Mini project: Excel → JSON
│   ├── hello.py              # Test script
│   └── utils/
│       └── __init__.py
├── notebooks/
│   └── exploration.ipynb
└── data/                     # (gitignored) - place Excel files here
    └── sample_structure.xlsx
```

## Quick Start
```bash
# Install dependencies
uv pip install -r requirements.txt
# or
pip install -r requirements.txt

# Run test script
python scripts/hello.py

# Run mini project
python scripts/excel_to_json.py data/sample_structure.xlsx
```

## Learning Log
| Minggu | Topik | Status | Catatan |
|--------|-------|--------|---------|
| 1-2 | Python fundamentals | 🔄 In progress | Setup env, basic syntax, file I/O |
