import requests
import io
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")


def get_chart(symbol: str):

  url = "https://api.chart-img.com/v2/tradingview/advanced-chart"
  headers = {
      "x-api-key": api_key,
      "content-type": "application/json"
  }

  payload = {
      "theme": "dark",
      "interval": "1W",
      "symbol": f"NASDAQ:{symbol}",
      "override": {
          "showStudyLastValue": False
      },
      "studies": [
          {
              "name": "Volume",
              "forceOverlay": True
          },
          {
              "name": "MACD",
              "override": {
                  "Signal.linewidth": 2,
                  "Signal.color": "rgb(255,65,129)"
              }
          }
      ]
  }

  response = requests.post(url, headers=headers, json=payload)
  if response.status_code == 200:
    image_bytes = io.BytesIO(response.content)
    pil_image = Image.open(image_bytes)
    return pil_image
  else:
      raise Exception(f"Chart fetch failed: {response.status_code} - {response.text}")
