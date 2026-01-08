import pandas as pd
import os

# --- PART 1: CONFIGURATION & PATHS ---
# Get the absolute path of the script's directory to ensure relative paths work
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Define Input/Output Paths
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')

print(f"--- GLP-1 Data Pipeline Initialized ---")
print(f"Reading from: {RAW_DATA_DIR}")
print(f"Saving to:    {PROCESSED_DATA_DIR}")

# Constants
WEGOVY_LIST_PRICE = 1349
MEDICAID_STATES = [
    'California', 'Colorado', 'Connecticut', 'Hawaii', 'Massachusetts', 
    'Maryland', 'Minnesota', 'Montana', 'Nevada', 'New Mexico', 
    'New York', 'Oregon', 'Washington'
]

# File Names (Must match exactly what is in data/raw/)
FILE_OBESITY = os.path.join(RAW_DATA_DIR, "Obesity_by_state_2024.csv")
FILE_INCOME = os.path.join(RAW_DATA_DIR, "S1901_Income_Last_12_Months.csv")
FILE_EDU = os.path.join(RAW_DATA_DIR, "BRFSS_Prevalence_Data_Education.csv")
FILE_INC_BRFSS = os.path.join(RAW_DATA_DIR, "BRFSS_Prevalence_Data_Household_Income.csv")

# --- PART 2: GENERATE STATE MASTER TABLE ---
print("\n[Step 1/2] Building State Master Table...")

try:
    # 1. Load Obesity Data
    if not os.path.exists(FILE_OBESITY):
        raise FileNotFoundError(f"Missing file: {FILE_OBESITY}")
        
    df_obesity = pd.read_csv(FILE_OBESITY)
    df_master = df_obesity[['State', 'Prevalence']].rename(columns={'Prevalence': 'Obesity_Pct'})

    # 2. Load & Clean Income Data
    if not os.path.exists(FILE_INCOME):
        raise FileNotFoundError(f"Missing file: {FILE_INCOME}")
        
    df_s1901 = pd.read_csv(FILE_INCOME)
    median_income_row = df_s1901.iloc[11] # Row 11 is Median Income
    
    income_data = []
    for col in df_s1901.columns:
        if "!!Households!!Estimate" in col:
            state_name = col.split("!!")[0]
            val_str = str(median_income_row[col])
            # Clean formatting
            val_clean = val_str.replace(',', '').replace('+', '').replace('$', '').strip()
            try:
                val_float = float(val_clean)
            except ValueError:
                val_float = None
            income_data.append({'State': state_name, 'Median_Household_Income': val_float})
    
    df_income = pd.DataFrame(income_data)
    
    # 3. Merge & Calculate
    df_master = df_master.merge(df_income, on='State', how='left')
    df_master['Medicaid_Covers_GLP1'] = df_master['State'].isin(MEDICAID_STATES)
    df_master['Weeks_Income_for_Wegovy'] = WEGOVY_LIST_PRICE / (df_master['Median_Household_Income'] / 52)
    
    # Save to Processed Folder
    output_master = os.path.join(PROCESSED_DATA_DIR, "GLP1_State_Master.csv")
    df_master.to_csv(output_master, index=False)
    print(f"Success: Saved 'GLP1_State_Master.csv'")

except Exception as e:
    print(f"CRITICAL ERROR in Step 1: {e}")

# --- PART 3: GENERATE DEMOGRAPHICS TABLE ---
print("\n[Step 2/2] Building Demographics Table...")

try:
    files_to_process = [
        (FILE_EDU, "Education"),
        (FILE_INC_BRFSS, "Income")
    ]
    
    dfs_list = []
    
    for filepath, label in files_to_process:
        if os.path.exists(filepath):
            temp = pd.read_csv(filepath)
            # Filter for Obese Response
            temp = temp[temp['Response'] == 'Obese (BMI 30.0 - 99.8)']
            # Tidy Columns
            temp = temp[['Locationdesc', 'Break_Out', 'Data_value']]
            temp.columns = ['State', 'Group', 'Obesity_Rate']
            temp['Category'] = label
            dfs_list.append(temp)
        else:
            print(f"Warning: File not found: {filepath}")

    if dfs_list:
        df_demographics = pd.concat(dfs_list)
        output_demo = os.path.join(PROCESSED_DATA_DIR, "GLP1_Demographics.csv")
        df_demographics.to_csv(output_demo, index=False)
        print(f"Success: Saved 'GLP1_Demographics.csv'")
    else:
        print("Error: No demographic data processed.")

except Exception as e:
    print(f"CRITICAL ERROR in Step 2: {e}")

print("\n--- Pipeline Complete ---")