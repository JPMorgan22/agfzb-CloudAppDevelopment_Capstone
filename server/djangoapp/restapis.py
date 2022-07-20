import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests
import os

client = Cloudant.iam(
    account_name="949fe2a8-5bb8-45a9-abfe-4ab7769e65b4-bluemix",
    api_key="RtXYQUFmw3Plhy7LAVoKPC_XtHZrfr4mlG23JBkTiPGY",
    connect=True,
)

dealership_db = client["dealerships"]
review_db     = client["reviews"]

dealership_db.create_query_index(fields=['state'])

def getDealershipByState(state):

    dealerships = []

    try:
        selector = {'state': {'$eq': state}}
        docs = dealership_db.get_query_result(selector)
        for doc in docs:
            dealerships.append(doc)

    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dealerships": dealerships}

def getAllDealerships():

    dealerships = []

    try:
        for document in dealership_db:
            dealerships.append(document)

    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dealerships": dealerships}

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



