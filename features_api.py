import boto3
import json
import pandas as pd



def query(id):
    df = pd.read_csv('s3://mybucket/kueski/data/dataset_credit_risk.csv')
    
    df_id = df['id' == id]
    df_id = df_id.sort_values(by=["id", "loan_date"])
    df_id = df_id.reset_index(drop=True)
    
    df_id["loan_date"] = pd.to_datetime(df.loan_date)
    
    df_grouped = df_id.groupby("id")
    df_id["nb_previous_loans"] = df_grouped["loan_date"].rank(method="first") - 1

    df_id['avg_amount_loans_previous'] = (
    df_id.groupby('id')['loan_amount'].apply(lambda x: x.shift().expanding().mean())
    )

    df_id['birthday'] = pd.to_datetime(df_id['birthday'], errors='coerce')
    df_id['age'] = (pd.to_datetime('today').normalize() - df_id['birthday']).dt.days // 365

    df_id['job_start_date'] = pd.to_datetime(df_id['job_start_date'], errors='coerce')
    df_id['years_on_the_job'] = (pd.to_datetime('today').normalize() - df_id['job_start_date']).dt.days // 365

    df['flag_own_car'] = df.flag_own_car.apply(lambda x : 0 if x == 'N' else 1)


    id_dict = {
            'age': None, 
            'years_on_the_job' : None,
            'nb_previous_loans' : None,
            'avg_amount_loans_previous' : None,
            'flag_own_car' : None,
            'status' : None
            }

    if df_id.shape[0] > 0:
        
        df_id = df_id.sort_values(['nb_previous_loans'], ascending = False)
        df_id.reset_index(drop=True, inplace=True)
        
        row = df_id.iloc[0]
        
        id_dict['age'] = row['age']
        id_dict['years_on_the_job'] = row['years_on_the_job']
        id_dict[ 'avg_amount_loans_previous'] = row[ 'avg_amount_loans_previous']
        id_dict['flag_own_car,status'] = row['flag_own_car,status']
        id_dict['status'] = row['status']

    return id_dict




def lambda_handler(event, context):
     
    id = -1

    if "body" in event:
        body = json.loads(event['body'])
        id = body['id']
    else:
        id = event
    

    client = boto3.client('s3')
    resource = boto3.resource('s3')
    region = boto3.session.Session().region_name

    file_name = 'dataset_credit_risk.csv'
    bucket_name = 'mybucket'
    result = client.list_objects_v2(Bucket= bucket_name, Prefix = 'kueski/data')
    file_exists = False
    
    if 'Contents' in result:
        for object in result['Contents']:
            if file_name in object['Key']:
                file_exists = True

    if file_exists:
        #file = client.get_object(Bucket= bucket_name, Key="kueski/data/training.csv")
        return json.dumps(query(id))

    else:
        return json.dumps({
        'statusCode': 404,
        'body': 'dataset_credit_risk.csv not found'
    })
                






