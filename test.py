import requests

API= "NCBIFMP7K04TYN59" # api for  exchange rate(alphavantage)

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={}'.format(API)
r = requests.get(url)
data = r.json()

print(data)


# currency exchange rate javascript 

"""

{
    "Realtime Currency Exchange Rate": {
        "1. From_Currency Code": "USD",
        "2. From_Currency Name": "United States Dollar",
        "3. To_Currency Code": "JPY",
        "4. To_Currency Name": "Japanese Yen",
        "5. Exchange Rate": "147.94400000",
        "6. Last Refreshed": "2024-02-07 15:35:01",
        "7. Time Zone": "UTC",
        "8. Bid Price": "147.94160000",
        "9. Ask Price": "147.94410000"
    }
}


"""