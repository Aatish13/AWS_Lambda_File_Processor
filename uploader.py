import json
import boto3
session = boto3.Session(region_name="REGION_NAME",
                        aws_access_key_id="AWS_ACCESS_KEY_ID",
                        aws_secret_access_key="AWS_SECRET_ACCESS_KEY")

# upload student_data.json to dynamoDB
def load_json_to_dynamodb():
    dynamodb = session.resource('dynamodb')

    table = dynamodb.Table('student')

    with open('./student_data.json', 'r') as myfile:
        data=myfile.read()

    # parse file
    obj = json.loads(data)

    for o in obj:
        table.put_item(Item=o)
    return "Success"


if __name__ == "__main__":
    load_json_to_dynamodb()