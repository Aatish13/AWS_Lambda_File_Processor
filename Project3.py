import boto3
import time
import json
import threading
from boto3.dynamodb.conditions import Key

INPUT_BUCKET_NAME = "cse546project3input"
OUTPUT_BUCKET_NAME = "cse546project3output"
REGION_NAME = 'us-east-1'


session = boto3.Session(region_name=REGION_NAME,
                        aws_access_key_id=AWS_ACCESS_KEY_ID, 
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Get S3 client from boto3
s3 = session.client('s3')

# Get S3 client from boto3
lambda_client = session.client('lambda')

#Function for trigerring the AWS lambda function
def trigger_lambda(file_name):
    event = { "Records": [{"s3": {"bucket": {"name": INPUT_BUCKET_NAME},
                                  "object": {"key": file_name}}}]}
    response = lambda_client.invoke(
    FunctionName='face_detection',
    InvocationType='Event',
    LogType='Tail',
    ClientContext='string',
    Payload=json.dumps(event),
    )

# Function for monitoring S3 output bucket
def monitor_S3_output_bucket():
    stored_file_details = {}
    count = 0
    while True:
        contents = s3.list_objects(Bucket=OUTPUT_BUCKET_NAME).get('Contents', [])
        file_details = [[obj['Key'],obj['LastModified']] for obj in contents]
        
        for key in file_details:
            if stored_file_details.get(key[0])!=key[1]:
                stored_file_details[key[0]] = key[1]
                response = s3.get_object(Bucket=OUTPUT_BUCKET_NAME, Key = key[0])
                data = response['Body'].read()
                count+=1
                print("Count:",count," - ",key[0], " ", data.decode().strip())

        time.sleep(15)

#Function for monitoring S3 input bucket
def monitor_S3_input_bucket():
    stored_file_details = {}

    while True:
        contents = s3.list_objects(Bucket=INPUT_BUCKET_NAME).get('Contents', [])
        file_details = [[obj['Key'],obj['LastModified']] for obj in contents]
        for key in file_details:
            if stored_file_details.get(key[0]) != key[1]:
                stored_file_details[key[0]] = key[1]
                trigger_lambda(key[0])
        time.sleep(15)


input_process = threading.Thread(target=monitor_S3_input_bucket)
output_process = threading.Thread(target=monitor_S3_output_bucket)

input_process.start()
output_process.start()
