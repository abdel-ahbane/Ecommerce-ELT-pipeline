import pandas as pd
import os
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def clean_data(df):
    #using list comprehension to fix columns names ad assign it to original df.columns
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    # convert order_date, payment_date, signup_date to date .to_datetime()
    for col in ["order_date", "payment_date", "signup_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    return df


raw_files_path = "../data/raw"
cleaned_files_path = "../data/cleaned"

os.makedirs(cleaned_files_path, exist_ok=True)
raw_files = os.listdir(raw_files_path)

for file in raw_files:
    if file.endswith(".csv"):
        raw_file_path = os.path.join(raw_files_path, file)

        logging.info(f"Processing {raw_file_path}")
        raw_df = pd.read_csv(raw_file_path)
        logging.info(raw_df.head(3))

        cleaned_df = clean_data(raw_df)
        logging.info(cleaned_df.head(3))

        cleaned_file_path = os.path.join(cleaned_files_path, file)
        cleaned_df.to_csv(cleaned_file_path, index=False)
        logging.info(f"Cleaned {file} has been saved to {cleaned_file_path}")



