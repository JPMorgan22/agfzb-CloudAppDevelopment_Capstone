import requests
import json
from .models import CarDealer
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
review_db = client["reviews"]

dealership_db.create_query_index(fields=['state'])
review_db.create_query_index(fields=['dealership'])

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

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

# if url is passed, use cf api to create request, else use python-cloudant sdk
def getAllDealerships(url=None):

    dealerships = []
    if url is None:
        try:
            for document in dealership_db:
                if 'short_name' in document:
                    dealer_obj = CarDealer(address=document["address"], city=document["city"], 
                        full_name=document["full_name"], id=document["id"], 
                        lat=document["lat"], long=document["long"],
                        short_name=document["short_name"],
                        st=document["st"], zip=document["zip"])
                    dealerships.append(dealer_obj)

        except CloudantException as ce:
            print("unable to connect")
            return {"error": ce}
        except (requests.exceptions.RequestException, ConnectionResetError) as err:
            print("connection error")
            return {"error": err}

        return {"dealerships": dealerships}
    else:
        json_result = get_request(url)
        if json_result:
            # Get the row list in JSON as dealers
            dealers = json_result["rows"]
            # For each dealer object
            for dealer in dealers:
                # Get its content in `doc` object
                dealer_doc = dealer["doc"]
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
                dealerships.append(dealer_obj)

        return {"dealerships":dealerships}

def getReviewByDealership(dealer_id):

    reviews = []

    try:
        selector = {'dealership': {'$eq': int(dealer_id)}}
        docs = review_db.get_query_result(selector)
        for doc in docs:
            reviews.append(doc)

    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    print("HERES WHAT WE GOT:" + str(reviews))
    return {"reviews": reviews}

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



