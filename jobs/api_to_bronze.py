import requests
import boto3
import json

class BreweryDataPipeline:
    def __init__(self, bucket_name, prefix="breweries/", page_size=200):
        self.api_url = "https://api.openbrewerydb.org/v1/breweries"
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.page_size = page_size
        self.s3_client = boto3.client("s3")

    def fetch_page(self, page):
        params = {"per_page": self.page_size, "page": page}
        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            return response.json()
        print(f"Failed to fetch page {page}: {response.status_code}")
        return None

    def save_to_s3(self, data, page):
        if not data:
            print(f"No data to save for page {page}.")
            return

        file_key = f"{self.prefix}breweries_page_{page}.json"
        json_data = json.dumps(data, indent=4)

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=json_data,
                ContentType="application/json"
            )
            print(f"Page {page} saved to S3: {file_key}")
        except Exception as e:
            print(f"Error saving page {page} to S3: {e}")

    def run_pipeline(self, max_pages=50):
        for page in range(1, max_pages + 1):
            print(f"Processing page {page}...")
            data = self.fetch_page(page)
            self.save_to_s3(data, page)

if __name__ == "__main__":
    bucket_name = "your-s3-bucket-name"
    pipeline = BreweryDataPipeline(bucket_name)
    pipeline.run_pipeline(max_pages=50)