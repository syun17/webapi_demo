import requests
from datetime import datetime


def get_weather():
    TARGETURL = "https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json"

    r = requests.get(TARGETURL)
    root = r.json()
    # Extract temperature and humidity from the API response
    # This is a simplified example; you'll need to adjust the keys based on the actual API structure
    wethers = root[0]["timeSeries"][0]["areas"][0]["weathers"]

    time_defins=root[0]["timeSeries"][0]["timeDefines"]
    time_defins
    for item1,item2 in zip(time_defins,wethers):
        dt = datetime.fromisoformat(item1)
        print(dt.strftime("%Y/%m/%d(%a)"),item2)
    return 