import boto3
import simplejson as json
import os
from moto import mock_dynamodb2
from unittest.mock import patch
from src.read_lists import app
from contextlib import contextmanager

table_name = 'packing-list-table'

event_data = 'events/read_lists_event.json'
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
            'user_id': {'S': 'user_id'},
            'list_id': {'S': 'list_id'},
            'name': {'S': 'List_Name'},
            'description': {'S': 'List Description...'},
            'last_edit_date': {'S': '01/01/1010'},
            'items': {
                'L': [
                    {
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
                ]
            }
        }
    )


@patch.dict(os.environ, {
    'TABLE': 'packing-list-table',
    'REGION': 'us-east-1',
    'AWSENV': 'MOCK'
})
def test_read_lists_200():
    with do_test_setup():
        response = app.lambda_handler(event, '')

        payload = [
            {
                'user_id': 'user_id',
                'list_id': 'list_id',
                'name': 'List_Name',
                'description': 'List Description...',
                'last_edit_date': '01/01/1010',
                'items': [{
                    'name': 'Item_name',
                    'description': 'Item Description',
                    'weight': 100,
                    'unit': 'Ounces',
                    'price': 'List_Name',
                    'worn': True,
                    'consumable': False,
                    'quantity': 1,
                    'image_link': 'link_to_image.link',
                    'category': 'my_category'
                }]
            }
        ]

        data = json.loads(response['body'])

        assert event['httpMethod'] == 'GET'
        assert data == payload


@patch.dict(os.environ, {
    'TABLE': 'packing-list-table',
    'REGION': 'us-east-1',
    'AWSENV': 'MOCK'
})
def test_list_activities_400():
    with do_test_setup():
        response = app.lambda_handler({}, '')

        payload = {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

        assert response == payload
