import boto3
import json
from datetime import datetime

def load_data(bucket_name, file_name, data_json):

    try:
        s3 = boto3.client('s3')

        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=data_json
        )

        date = datetime.now().date()

        print(f"Archive {date} loaded!")

    except Exception as e:
        print(f"Error loading archive: {e}")
        