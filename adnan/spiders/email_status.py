import scrapy
import pandas as pd
from urllib.parse import urlencode



import json
class EmailStatusSpider(scrapy.Spider):
    name = "email_status"

    def start_requests(self):
        file_path = r"C:\Users\Lenovo\Downloads\10000emailsV2.csv"
        status=1
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            Id = row['Id']
            First_Name = row['First_Name']
            Last_Name = row['Last_Name']
            Email = row['Email']
            registered = row['registered']
            recheck = row['recheck']



            url = "https://registerdisney.go.com/jgc/v8/client/TPR-DVC.WEB-PROD/guest-flow?langPref=en-US&feature=no-password-reuse"

            payload = json.dumps({
                "email": Email
            })
            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9,ur;q=0.8',
                'authorization': 'APIKEY hGPASjkP4n4pnhWXCXnPlgLqn7NVrs+RHPpXHvTSbhMKBJRKdb7LEH1w4kuGQ5i5DzVQ2fyqZqQCq4Nk9ejlkQ==',
                'cache-control': 'no-cache',
                'content-type': 'application/json',
                'conversation-id': '18ef0bdb-9e32-4437-9887-14112065571a',
                'correlation-id': '1b7f42a6-8d59-44c8-95f9-5483c1f589d9',
                'expires': '-1',
                'oneid-reporting': 'eyJjb252ZXJzYXRpb25JZCI6IjE4ZWYwYmRiLTllMzItNDQzNy05ODg3LTE0MTEyMDY1NTcxYSJ9',
                'origin': 'https://cdn.registerdisney.go.com',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://cdn.registerdisney.go.com/',
                'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site'
                # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
            }

            # response = requests.request("POST", url, headers=headers, data=payload)
            yield scrapy.Request(
                url=url,
                method='POST',
                headers=headers,
                body=payload,
                meta={
                    'Id': Id,
                    'First_Name': First_Name,
                    'Last_Name': Last_Name,
                    'Email': Email,
                    'registered': registered

                },
                callback=self.parse
            )
            # print(response.text)



    def parse(self, response):

        try:
            Id=response.meta['Id']
            First_Name=response.meta['First_Name']
            Last_Name=response.meta['Last_Name']
            Email=response.meta['Email']
            registered=response.meta['registered']

            json_data = json.loads(response.text)
            guestFlow=json_data.get('data').get('guestFlow')

            yield {
                'Id': Id,
                'First_Name': First_Name,
                'Last_Name': Last_Name,
                'Email': Email,
                'registered': registered,
                'guestFlow':guestFlow
            }

            # print(json_data)

        except json.JSONDecodeError:
            # Handle JSON decoding error
            self.logger.error("Failed to decode JSON response: %s", response.text)

