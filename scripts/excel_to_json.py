#!/usr/bin/env python3
"""Konversi Excel struktur/BOQ ke JSON untuk analisis lebih lanjut.

Usage:
    python scripts/excel_to_json.py data/sample_structure.xlsx
    python scripts/excel_to_json.py data/sample_structure.xlsx -o output/structure.json
"""

import argparse
import json
import sys
from pathlib import Path
import pandas as pd


def read_excel_smart(filepath: Path) -> dict[str, pd.DataFrame]:
    """Baca semua sheet di Excel, return dict {sheet_name: DataFrame}."""
    try:
        excel_file = pd.ExcelFile(filepath)
        sheets = {}
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            # Bersihkan: drop row/col kosong total
            df = df.dropna(how='all').dropna(axis=1, how='all')
            df.columns = df.columns.astype(str).str.strip()
            sheets[sheet_name] = df
            print(f"  Sheet '{sheet_name}': {df.shape[0]} rows × {df.shape[1]} cols")
        return sheets
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        sys.exit(1)


def sheets_to_json(sheets: dict[str, pd.DataFrame], output_path: Path) -> None:
    """Convert sheets dict to JSON dengan metadata."""
    output = {}
    for name, df in sheets.items():
        # Convert DataFrame ke list of records (dict per row)
        records = df.to_dict(orient='records')
        # Handle NaN -> None untuk JSON serializable
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
        
        output[name] = {
            'metadata': {
                'rows': len(df),
                'columns': list(df.columns),
                'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
            },
            'data': records,
        }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"✓ JSON saved to {output_path}")
    print(f"  Total sheets: {len(output)}")
    total_rows = sum(len(s['data']) for s in output.values())
    print(f"  Total data rows: {total_rows}")


def print_summary(sheets: dict[str, pd.DataFrame]) -> None:
    """Print ringkasan data untuk quick inspection."""
    print("\n=== RINGKASAN DATA ===")
    for name, df in sheets.items():
        print(f"\n--- Sheet: {name} ---")
        print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} cols")
        print(f"  Columns: {list(df.columns)}")
        print(f"  Dtypes:\n{df.dtypes}")
        print(f"  Sample (first 3 rows):")
        print(df.head(3).to_string(index=False))
        
        # Kalau ada kolom numerik, hitung statistik dasar
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            print(f"  Numeric stats:")
            print(df[numeric_cols].describe().to_string())


def main():
    parser = argparse.ArgumentParser(description="Excel → JSON converter untuk data teknik sipil")
    parser.add_argument('input', type=Path, help='Path ke file Excel (.xlsx/.xls)')
    parser.add_argument('-o', '--output', type=Path, help='Output JSON path (default: same name .json)')
    parser.add_argument('--summary-only', action='store_true', help='Hanya print summary, jangan write JSON')
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File tidak ditemukan: {input_path}")
        sys.exit(1)
    
    print(f"Reading: {input_path}")
    sheets = read_excel_smart(input_path)
    
    print_summary(sheets)
    
    if not args.summary_only:
        output_path = args.output or input_path.with_suffix('.json')
        sheets_to_json(sheets, output_path)
        print(f"\nNext steps:")
        print(f"  1. Buka {output_path} untuk inspect JSON")
        print(f"  2. Gunakan di notebook untuk analisis/visualisasi")
        print(f"  3. Commit perubahan: git add . && git commit -m 'Add Excel data + conversion script'")


if __name__ == "__main__":
    main()
