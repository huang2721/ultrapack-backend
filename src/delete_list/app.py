import boto3
import os
import simplejson as json

from common.utils.logger import get_logger

logger = get_logger('root')


def lambda_handler(message, context):
    if ('pathParameters' not in message or
            message['httpMethod'] != 'DELETE'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }
    # Set AWS resources
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
        list_id = message['pathParameters']['list_id']
        user_id = message['pathParameters']['user_id']
    except KeyError as err:
        logger.error(f'Error when parsing path parameters: {err}')

    params = {
        'list_id': list_id,
        'user_id': user_id
    }

    response = table.delete_item(
        Key=params
    )
    logger.info(response)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({'msg': 'List deleted'})
    }
