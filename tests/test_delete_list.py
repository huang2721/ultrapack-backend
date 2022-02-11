import boto3
import simplejson as json
import os
from moto import mock_dynamodb2
from unittest.mock import patch
from src.delete_list import app
from contextlib import contextmanager

table_name = 'packing-list-table'

event_data = 'events/delete_list_event.json'
with open(event_data, 'r') as f:
    event = json.load(f)


@contextmanager
def do_test_setup():
    with mock_dynamodb2():
        set_up_dynamodb()
        put_item_dynamodb()
        yield


def set_up_dynamodb():
    conn = boto3.client(
       'dynamodb',
        region_name='us-east-1',
        aws_access_key_id='mock',
        aws_secret_access_key='mock',
    )  
    conn.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'user_id', 'KeyType': 'HASH'},
            {'AttributeName': 'list_id', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'user_id', 'AttributeType': 'S'},
            {'AttributeName': 'list_id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        },
    )


def put_item_dynamodb():
    conn = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id='mock',
        aws_secret_access_key='mock',
    )

    conn.put_item(
        TableName=table_name,
        Item={
            'user_id': {'S': '12345'},
            'list_id': {'S': '54321'},
            'name': {'S': 'List_Name'},
            'description': {'S': 'List Description...'},
            'last_edit_date': {'S': '01/01/1010'},
            'items': {
                'M': {
                    'name': {'S': 'Item_name'},
                    'description': {'S': 'Item Description'},
                    'weight': {'N': '100'},
                    'unit': {'S': 'Ounces'},
                    'price': {'S': 'List_Name'},
                    'worn': {'BOOL': True},
                    'consumable': {'BOOL': False},
                    'quantity': {'N': '1'},
                    'image_link': {'S': 'link_to_image.link'},
                    'category': {'S': 'my_category'}
                }
            }
        }
    )


@patch.dict(os.environ, {
    'TABLE': 'packing-list-table',
    'REGION': 'us-east-1',
    'AWSENV': 'MOCK'
})
def test_delete_list_200():
    with do_test_setup():
        response = app.lambda_handler(event, '')

        payload = {
            'msg': 'List deleted'
        }

        data = json.loads(response['body'])

        packing_list_table = boto3.resource(
            'dynamodb',
            region_name='us-east-1',
            aws_access_key_id='mock',
            aws_secret_access_key='mock',
        )

        table = packing_list_table.Table(table_name)

        response = table.scan()

        assert event['httpMethod'] == 'DELETE'
        assert data == payload
        assert response['Items'] == []


@patch.dict(os.environ, {
    'TABLE': 'packing-list-table',
    'REGION': 'us-east-1',
    'AWSENV': 'MOCK'
})
def test_delete_list_400():
    with do_test_setup():
        response = app.lambda_handler({}, '')

        payload = {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

        assert response == payload
