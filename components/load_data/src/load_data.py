import pandas as pd
import argparse
from google.cloud import storage
def load_data(input_path):
    data = pd.read_excel(input_path)

    storage_client = storage.Client()
    bucket = storage_client.bucket("gs://first_pipeline")
    bucket.blob('data/data.xlsx').upload_from_filename(input_path)
    print(data.head())
    print("DATA IS UPLOADED TO GOOGLE STORAGE")
    return 
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description= "Input your desired data to be passed")
    parser.add_argument('--DataPath', type = str,
    help = 'Enter the data you want to upload here')
    args = parser.parse_args()
    load_data(args.DataPath)