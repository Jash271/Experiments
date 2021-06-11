from flask import Flask, request, jsonify
from dotenv import load_dotenv
import json
from requests import get, post
import time
import os

load_dotenv()
endpoint_1 = os.environ.get('endpoint')
key = os.environ.get('key')

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'Hello World'


def driver(x, url):
    body = {
        "source": url
    }
    if x == 'main':
        endpoint = endpoint_1
        apim_key = key
        post_url = endpoint + \
            "/formrecognizer/v2.1-preview.3/prebuilt/invoice/analyze?includeTextDetails=true"

        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': apim_key,
        }

        params = {
            "includeTextDetails": True
        }

        try:
            resp = post(url=post_url, data=json.dumps(body),
                        headers=headers, params=params)
            if resp.status_code != 202:
                print("POST analyze failed:\n%s" % resp.text)
                return ""

            get_url = resp.headers["operation-location"]
            n_tries = 10
            n_try = 0
            wait_sec = 6
            while n_try < n_tries:
                resp = get(url=get_url, headers={
                    "Ocp-Apim-Subscription-Key": apim_key})
                resp_json = json.loads(resp.text)

                if resp.status_code != 200:
                    print("GET Receipt results failed:\n%s" % resp_json)
                    return ""
                status = resp_json["status"]
                if status == "succeeded":
                    json_object = json.dumps(resp_json, indent=4)

                    return resp_json
                if status == "failed":
                    print("Analysis failed:\n%s" % resp_json)
                    return ""
            # Analysis still running. Wait and retry.
                time.sleep(wait_sec)
                n_try += 1
        except Exception as e:
            msg = "GET analyze results failed:\n%s" % str(e)
            print(msg)
            return ""

    elif x == 'business':
        endpoint = endpoint_1
        apim_key = key
        post_url = endpoint + \
            "/formrecognizer/v2.1-preview.3/prebuilt/businessCard/analyze?includeTextDetails=true&locale=en-IN"

        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': apim_key,
        }

        params = {
            "includeTextDetails": True
        }

        try:
            resp = post(url=post_url, data=json.dumps(body),
                        headers=headers, params=params)
            if resp.status_code != 202:
                print("POST analyze failed:\n%s" % resp.text)
                return ""

            get_url = resp.headers["operation-location"]
            n_tries = 10
            n_try = 0
            wait_sec = 6
            while n_try < n_tries:
                try:
                    resp = get(url=get_url, headers={
                        "Ocp-Apim-Subscription-Key": apim_key})
                    resp_json = json.loads(resp.text)

                    if resp.status_code != 200:
                        print("GET Receipt results failed:\n%s" % resp_json)
                        return ""
                    status = resp_json["status"]
                    if status == "succeeded":

                        try:
                            x = resp_json["analyzeResult"]["documentResults"][0]["fields"]["CompanyNames"]["valueArray"][0]["text"]
                            return x
                        except:
                            return ""

                    if status == "failed":
                        print("Analysis failed:\n%s" % resp_json)
                        return ""
            # Analysis still running. Wait and retry.
                    time.sleep(wait_sec)
                    n_try += 1
                except Exception as e:

                    return ""

        except Exception as e:
            print("POST analyze failed:\n%s" % str(e))
            return ""


def extract_relevant(data, url):
    master = {}

    x = driver("business", url)
    print(x)

    # Refer Business API

    master["VendorName"] = x
    master["Invoice_ID"] = data["analyzeResult"]["documentResults"][0]["fields"]["InvoiceId"]["text"]
    master["Invoice_Total"] = data["analyzeResult"]["documentResults"][0]["fields"]["InvoiceTotal"]["valueNumber"]
    print("1")
    l = []
    for x in data["analyzeResult"]["documentResults"][0]["fields"]["Items"]["valueArray"]:

        d = {}
        try:

            d["name"] = x["valueObject"]["Description"]["text"]
        except:
            d["name"] = ""
        try:
            d["amount"] = x["valueObject"]["Amount"]["valueNumber"]
        except:
            d["amount"] = ""
        try:
            d["quantity"] = x["valueObject"]["Quantity"]["valueNumber"]
        except:
            d["quantity"] = ""

        l.append(d)
    master["BillItems"] = l
    delta = json.dumps(master, indent=3)

    return master


@app.route('/extract_data', methods=['POST'])
def extract_data():
    url = request.form.get('url')
    print(url)
    res = driver("main", str(url))
    if (res == ""):
        print("Error")
        return jsonify({
            "Message": "Error Parsing"
        })

    final_res = extract_relevant(res, str(url))
    print(final_res)
    # Call GQL API's to Enter Json Details in DB

    return jsonify(final_res)
