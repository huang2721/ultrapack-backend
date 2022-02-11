import boto3
import os
import simplejson as json
from boto3.dynamodb.conditions import Key

from common.utils.logger import get_logger

logger = get_logger('root')


def lambda_handler(message, context):
    if ('pathParameters' not in message or
            message['httpMethod'] != 'GET'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    # Set AWS resoureces
    table_name = os.environ.get('TABLE', 'packing-list-table')
    region = os.environ.get('REGION', 'us-east-1')
    aws_environment = os.environ.get('AWSENV', 'AWS')
    if aws_environment == 'AWS_SAM_LOCAL':
        packing_list_table = boto3.resource(
            'dynamodb',
            endpoint_url='http://dynamodb:8000'
        )
    else:
        packing_list_table = boto3.resource(
            'dynamodb',
            region_name=region
        )
    table = packing_list_table.Table(table_name)

    # Parse response body
    try:
        user_id = message['pathParameters']['user_id']
    except KeyError as err:
        logger.error(f'Error when parsing path parameters: {err}')

    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    print(response)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Items'])
    }
