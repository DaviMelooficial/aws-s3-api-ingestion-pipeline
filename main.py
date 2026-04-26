from services.extract import extract_data
from services.load import load_data
from services.logger_config import setup_logger
from datetime import datetime
from dotenv import load_dotenv
import os

logger = setup_logger(__name__)

def main():
    try:
        load_dotenv()
        now = datetime.now()
        bucket_name = os.getenv('S3_BUCKET_NAME')
        url = "https://jsonplaceholder.typicode.com/posts"

        file_name = f'marketing_data/raw/jsonplaceholder/year={now.year}/month={now.month:02d}/data_{now.strftime("%Y%m%d_%H%M%S")}.json'

        logger.info("Pipeline started")

        data_json = extract_data(url)
        load_data(bucket_name, file_name, data_json)

        logger.info("Pipeline finished successfully")
    except Exception:
        logger.exception("Pipeline execution failed")
        raise

if __name__ == "__main__":
    main()