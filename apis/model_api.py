import requests
import pandas as pd
from joblib import load     
import boto3

def lambda_handler(event, context):

    s3_client = boto3.client("s3")
    bucket_name = 'mybucket'
    features_api_url = 'https://7io81nandb.execute-api.us-east-1.amazonaws.com/beta/example'
    object_key = "/kueski/models/model.joblib"
    file_content = s3_client.get_object( Bucket= bucket_name, Key=object_key)["Body"].read()
    model = load(file_content)
    features = requests.post(features_api_url, event)
    features = [features['age'], features['years_on_the_job'], features['nb_previous_loans'], features['avg_amount_loans_previous'], features['flag_own_car'], features['status']]

    return model.predict(features)