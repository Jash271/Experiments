import json
import os
import sys
import requests
import time


from decouple import config

# Add your Computer Vision subscription key and endpoint to your environment variables.
from dotenv import load_dotenv

load_dotenv()

endpoint = config('COMPUTER_VISION_ENDPOINT')

subscription_key = config('COMPUTER_VISION_SUBSCRIPTION_KEY')
text_recognition_url = endpoint + "/vision/v3.1/read/analyze"

# Set image_url to the URL of an image that you want to recognize.
image_url = 'https://firebasestorage.googleapis.com/v0/b/codeit-d447b.appspot.com/o/WhatsApp%20Image%202021-06-15%20at%207.52.03%20PM.jpeg?alt=media&token=d9fb9e6e-f4d6-4cce-9013-02595b1177cc'

headers = {'Ocp-Apim-Subscription-Key': subscription_key}
data = {'url': image_url}
print("1")
response = requests.post(
    text_recognition_url, headers=headers, json=data)
response.raise_for_status()

# Extracting text requires two API calls: One call to submit the
# image for processing, the other to retrieve the text found in the image.

# Holds the URI used to retrieve the recognized text.
operation_url = response.headers["Operation-Location"]
print("2")
# The recognized text isn't immediately available, so poll to wait for completion.


def recognize_lines(data):
    l = []
    items = data["analyzeResult"]["readResults"][0]["lines"]
    for x in items:
        l.append(x["text"])
    return l


analysis = {}
poll = True
while (poll):
    response_final = requests.get(
        response.headers["Operation-Location"], headers=headers)
    analysis = response_final.json()

    with open("data_1.json", "w") as outfile:
        outfile.write(json.dumps(analysis, indent=4))

    if ("analyzeResult" in analysis):
        poll = False
    if ("status" in analysis and analysis['status'] == 'failed'):
        poll = False

k = recognize_lines(analysis)
print(k)
print("Done")
