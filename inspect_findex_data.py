import pandas as pd

file_path = 'data/Findex/findex_microdata_2025_labelled_update112425.dta'

try:
    # Read a small subset of columns to speed things up, or just read the whole thing if needed
    # We need economycode, account, wgt, female
    df = pd.read_stata(file_path)
    
    print("--- Data Info ---")
    print(df[['economycode', 'account', 'female']].dtypes)
    
    print("\n--- Unique Economy Codes ---")
    print(df['economycode'].unique())
    
    print("\n--- Account Column Values ---")
    print(df['account'].unique())
    print(df['account'].value_counts(dropna=False))
    
    # Check what happens when we filter for IND and BGD
    target_economies = ['IND', 'BGD']
    df_filtered = df[df['economycode'].isin(target_economies)]
    
    print(f"\n--- Filtered Data (IND, BGD) ---")
    print(f"Shape: {df_filtered.shape}")
    print("Account value counts in filtered data:")
    print(df_filtered['account'].value_counts(dropna=False))
    
    # Check female column
    print("\n--- Female Column Values ---")
    print(df['female'].unique())
    
except Exception as e:
    print(f"Error: {e}")
