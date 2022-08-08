import requests
import json
import random
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests
import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions

authenticator = IAMAuthenticator('eiErHXVKabJ_ouMD8V24T7_w-czR0wvoDwujPTLCY3Hy')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator)

natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/b36b026b-0758-43bf-b2d5-48e48096132b')

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
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
        # If any error occurs
        print("Network exception occurred")
    # status_code = response.status_code
    # print("With status {} ".format(status_code))
    # json_data = json.loads(response.text)
    # return json_data
    status_code = response.status_code
    print("With status {} ".format(status_code))
    print(response.headers['content-type'])
    print(response.content)
    json_data = json.loads(response.text)
    return json_data

def getDealershipByState(state):

    dealerships = []

    try:
        selector = {'state': {'$eq': state}}
        docs = dealership_db.get_query_result(selector)
        for document in docs:
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
        for document in docs:
            sentiment = analyze_review_sentiments(document["review"])
            review_obj = DealerReview(dealership=document["dealership"], purchase=document["purchase"], 
                                name=document["name"], id=document["id"] if 'id' in document else random.randint(10, 999), 
                                review=document["review"], 
                                purchase_date=document["purchase_date"] if (document["purchase"] == True) else None,
                                car_make=document["car_make"] if (document["purchase"] == True) else None,
                                car_model=document["car_model"] if (document["purchase"] == True) else None, 
                                car_year=document["car_year"] if (document["purchase"] == True) else None,
                                sentiment=sentiment)
            reviews.append(review_obj)

    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    print("HERES WHAT WE GOT:" + str(reviews))
    return {"reviews": reviews}


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    if(text is None):
        return "No review"

    response = natural_language_understanding.analyze(
                text=text,
                features=Features(
                sentiment=SentimentOptions(document=True))).get_result()
    return response["sentiment"]["document"]["label"]

def addReviewToCloudant(review):

    my_document = review_db.create_document(review)
    if my_document.exists():
        print('SUCCESS!!')
    else:
        print("Error creating document")




