import boto3
from datetime import datetime
from services.logger_config import setup_logger


logger = setup_logger(__name__)

def load_data(bucket_name, file_name, data_json):

    try:
        s3 = boto3.client('s3')

        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=data_json,
            ContentType="application/json"
        )

        date = datetime.now().date()

        logger.info("File successfully uploaded on %s: %s", date, file_name)

    except Exception as e:
        logger.exception("Error uploading file to S3: %s", e)
        raise