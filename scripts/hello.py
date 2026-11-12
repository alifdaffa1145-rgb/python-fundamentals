#!/usr/bin/env python3
"""Test script untuk memastikan environment berfungsi."""

import sys
import platform
import pandas as pd
import numpy as np

def main():
    print(f"Python {sys.version.split()[0]} on {platform.platform()}")
    print(f"Pandas {pd.__version__}")
    print(f"NumPy {np.__version__}")
    print("✓ Environment ready!")
    
    # Quick test: baca Excel kalau ada
    import os
    excel_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_structure.xlsx')
    if os.path.exists(excel_path):
        df = pd.read_excel(excel_path)
        print(f"✓ Sample Excel loaded: {df.shape[0]} rows, {df.shape[1]} cols")
        print(df.head())
    else:
        print(f"⚠ Sample Excel not found at {excel_path}")
        print("  Letakkan file Excel struktur/BOQ di folder data/")

if __name__ == "__main__":
    main()
