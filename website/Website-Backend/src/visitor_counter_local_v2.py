import json
import boto3
import os
import time
from dotenv import load_dotenv

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
TABLE_NAME = "non-existent-table"

client = boto3.client("dynamodb", region_name='us-east-1',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def lambda_handler(event, context):
    return Get_Visitor_Count()

def Get_Visitor_Count(table):
    response = client.scan(TableName=table)
    try:
        response = client.scan(TableName=TABLE_NAME)
        if "Items" in response:   
            count = response["Items"][0]["visitor_count"]["N"]
            # Convert string to int for increment operation
            count = int(count)
            # Increment count by 1
            count += 1
    # Error handling for being passed an empty or non-existent key
    except (IndexError, KeyError):
        count = 0
    except client.exceptions.ResourceNotFoundException:
        client.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    "AttributeName": "visitor_count_id",
                    "KeyType": "HASH"
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "visitor_count_id",
                    "AttributeType": "N"
                }
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
            TableName=TABLE_NAME,

        )
        count = 0

        time.sleep(30)

    def get_key_schema():
        #describe table and get partition key and pk type
        describe_response = client.describe_table(TableName=TABLE_NAME)
        pk_name = describe_response["Table"]["AttributeDefinitions"][0]["AttributeName"]
        pk_type = describe_response["Table"]["AttributeDefinitions"][0]["AttributeType"]

        # Primary key determines pk value
        if pk_type == "B":
            pk_value = 'MQ=='
            key = {
                f'{pk_name}': {
                    f'{pk_type}': f'{pk_value}',
                }
            }
        elif pk_type == 'S' or pk_type == 'N':
            pk_value = "1"
            key = {
                f'{pk_name}': {
                    f'{pk_type}': f'{pk_value}',
                }
            }
        return key

    client.update_item(
        # Unique identifier of the record
        Key=get_key_schema(),
        # Substitution token for the atrribute name
        ExpressionAttributeNames={
            "#VC": "visitor_count",
        },
        ExpressionAttributeValues={
            ":count": {
                # N is attribute of type number
                "N": str(count),
            },
        },
        returnValues="ALL_NEW",
        TableName=TABLE_NAME,
        # An expression that defines one or more attributes to be updated, the action to be performed on them, and new values for them.
        # SET - Adds one or more attributes and values to an item. If any of these attributes already exist, they are replaced by the new values.
        UpdateExpression="SET #VC = :count",
    )

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'visitorcount': count})
    }

print(Get_Visitor_Count(TABLE_NAME))