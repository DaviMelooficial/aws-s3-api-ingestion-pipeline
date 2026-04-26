from services.extract import extract_data
from services.load import load_data
from datetime import datetime

def main():

    url = "https://jsonplaceholder.typicode.com/posts"
    bucket_name = 'davi-data-pipeline-raw'

    now = datetime.now()
    file_name = f'marketing_data/raw/jsonplaceholder/year={now.year}/month={now.month:02d}/data_{now.strftime("%Y%m%d_%H%M%S")}.json'

    data_json = extract_data(url)

    load_data(bucket_name, file_name, data_json)

if __name__ == "__main__":
    main()