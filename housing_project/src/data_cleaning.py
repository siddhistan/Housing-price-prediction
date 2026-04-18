import pandas as pd
import os

# 1. Setup Paths
# We use paths relative to the project root where you run the command
raw_data_path = 'housing_project/data/raw/train.csv'
processed_folder = 'housing_project/data/processed'
output_path = os.path.join(processed_folder, 'cleaned_train.csv')

def clean_data():
    # Load original data
    print("Loading raw data...")
    df = pd.read_csv(raw_data_path)

    # --- DROP COLUMNS ---
    # Dropping high-null columns identified in exploration
    cols_to_drop = ['PoolQC', 'MiscFeature', 'Alley', 'Fence']
    df_cleaned = df.drop(columns=cols_to_drop)

    # --- FLAG CATEGORICAL ---
    # NaNs in these columns actually mean 'None' (e.g., No Garage)
    none_cols = ['FireplaceQu', 'GarageType', 'GarageFinish', 'GarageQual', 
                 'GarageCond', 'BsmtQual', 'BsmtCond']
    for col in none_cols:
        df_cleaned[col] = df_cleaned[col].fillna('None')

    # --- IMPUTE NUMERICAL ---
    # Filling LotFrontage with median
    median_val = df_cleaned['LotFrontage'].median()
    df_cleaned['LotFrontage'] = df_cleaned['LotFrontage'].fillna(median_val)

    # --- REMOVE OUTLIERS ---
    # Keeping GrLivArea under 4000 to prevent skewed results
    df_final = df_cleaned[df_cleaned['GrLivArea'] < 4000]

    # Save the result
    os.makedirs(processed_folder, exist_ok=True)
    df_final.to_csv(output_path, index=False)
    print(f"Cleaning complete! Saved {len(df_final)} rows to {output_path}")

if __name__ == "__main__":
    clean_data()