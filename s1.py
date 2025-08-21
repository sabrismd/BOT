# s1.py
import requests
from urllib.parse import quote, unquote
import logging

# Static token (replace manually when expired)
ACCESS_TOKEN = "eyJraWQiOiIxNGNkZWVkOS0wZGViLTQ4ZTgtOGQ5ZS03ZGU4MzdmZWY5YTEiLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJhdWQiOiI2ODU4M2YxZTQ4MTFkYzAzOTk2MDQ3NzQiLCJpc3MiOiJodHRwczovL3d3dy5leHRyYXBlLmNvbSIsIm5hbWUiOiJNb2hhbW1lZCBTYWJyaSIsImV4cCI6MTc1ODM4MTE5NywidXNlcklkIjoiNjg1ODNmMWU0ODExZGMwMzk5NjA0Nzc0IiwiaWF0IjoxNzU1Nzg5MTk3fQ.cFf1VQZsFCLJqIqLwFECuUbNpdgu9FSl5x4YMaO48FmZMK_3YvoXWXVScX5FR4_0uV8NS72avQP93K3pQgpdPg"

CONVERTER_API_URL = "https://www.extrape.com/handler/convertText"
HEADERS = {
    "accessToken": ACCESS_TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

def convert_link(original_link):
    try:
        payload = {
            "bitlyConvert": False,
            "imageUrl": "",
            "inputText": quote(original_link, safe='')
        }

        response = requests.post(CONVERTER_API_URL, headers=HEADERS, json=payload)

        if response.status_code == 200:
            data = response.json()
            converted = unquote(data.get("convertedText", ""))
            logging.info(f"Converted: {original_link} -> {converted}")
            return converted
        else:
            logging.error(f"API Error: {response.status_code} | {response.text}")
            return None

    except Exception as e:
        logging.exception(f"Conversion failed for link: {original_link}")
        return None


