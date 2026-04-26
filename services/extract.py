import requests
import json
from services.logger_config import setup_logger

logger = setup_logger(__name__)

def extract_data(url):
    try:
        logger.info("Starting extraction from URL: %s", url)

        response = requests.get(url, timeout=10)
        logger.info(
            "Response received: status=%s reason=%s",
            response.status_code,
            response.reason,
        )

        response.raise_for_status()

        data = response.json()
        data_json = json.dumps(data, ensure_ascii=False, indent=2)

        logger.info("Extraction completed successfully")
        return data_json

    except requests.HTTPError:
        logger.exception("HTTP error during extraction")
        raise
    except Exception:
        logger.exception("Unexpected error during extraction")
        raise