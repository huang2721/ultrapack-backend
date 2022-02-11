import uuid
from datetime import datetime
import simplejson as json
import boto3
import os
from common.utils.logger import get_logger
logger = get_logger('root')


def lambda_handler(message, context):
    if ('body' not in message or message['httpMethod'] != 'POST'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    # Set AWS resoureces
    table_name = 'packing-list-table'
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

    # Load message body
    body = json.loads(message['body'])
    # Build list

    # try:
    #     list = body['packing_list']
    #     items = []
    #     for i in list['items']:
    #         item = Item()
    #         item.name = i['name']
    #         item.description = i['description']
    #         item.weight = i['weight']
    #         item.unit = i['unit']
    #         item.price = i['price']
    #         item.worn = i['worn']
    #         item.consumable = i['consumable']
    #         item.quantity = i['quantity']
    #         item.image_link = i['image_link']
    #         item.category = i['category']
    #         items.append(item)
    #     id = body['list_id']
    #     list_id = str(uuid.uuid4()) if id == "" else id
    #     pack_list = PackList(
    #         user_id=body['user_id'],
    #         list_id=list_id,
    #         name=list['name'],
    #         description=list['description'],
    #         last_edit_date=str(datetime.timestamp(datetime.now())),
    #         items=items
    #     )

    # packing_list = PackingList()
    # list_id = body['list_id']
    # packing_list.id = str(uuid.uuid4()) if list_id is None else list_id
    # packing_list.user_id = body['user_id']
    # packing_list.name = list['name']
    # packing_list.description = list['description']
    # packing_list.last_edit_date = str(datetime.timestamp(datetime.now()))
    try:
        list = body['packing_list']
        # Fill items list with each item
        items = []
        for i in list['items']:
            item = {
                'name': i['name'],
                'description': i['description'],
                'weight': i['weight'],
                'unit': i['unit'],
                'price': i['price'],
                'worn': i['worn'],
                'consumable': i['consumable'],
                'quantity': i['quantity'],
                'image_link': i['image_link'],
                'category': i['category']
            }
            items.append(item)
        # Create list_id if it doesn't exist already
        id = body['list_id']
        list_id = str(uuid.uuid4()) if id == "" else id
        # Create params to be sent in request body
        params = {
            'user_id': body['user_id'],
            'list_id': list_id,
            'name': list['name'],
            'description': list['description'],
            'last_edit_date': str(datetime.timestamp(datetime.now())),
            'items': items
        }
    except KeyError as err:
        logger.error(f'Error from parsing response body: {err}')

    # Write to table
    response = table.put_item(
        TableName=table_name,
        Item=params
    )

    # response = pack_list.save()

    logger.info(response)

    return {
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({'msg': 'Table created!'})
    }
