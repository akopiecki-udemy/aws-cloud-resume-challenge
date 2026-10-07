import boto3
from moto import mock_aws
import sys, os

# Set path for local package import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path)))


# Set fake ENV variables for mocks
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"

@mock_aws
def test_empty_table():
    client = boto3.client("dynamodb", region_name='us-east-1')
    table_name = "test_table"
    from src import visitor_counter_local_v2 as vc
    client.create_table(
        AttributeDefinitions=[
            {
                "AttributeName": "visitor_count_id",
                "AttributeType": "N"
            }
        ],
        KeySchema=[
            {
                "AttributeName": "visitor_count_id",
                "KeyType": "HASH"
            }
        ],
        BillingMode="PAY_PER_REQUEST",
        TableName=table_name,
    )
    vc.Get_visitor_count(table_name)
    
