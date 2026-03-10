import json
import boto3
import random
import string
import os
from urllib.parse import urlparse

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'url-shortener'))

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
}

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except Exception:
        return False

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body') or '{}')
        long_url = body.get('long_url')

        if not long_url:
            return {
                'statusCode': 400,
                'headers': HEADERS,
                'body': json.dumps({'message': 'long_url is required'})
            }

        if not is_valid_url(long_url):
            return {
                'statusCode': 400,
                'headers': HEADERS,
                'body': json.dumps({'message': 'Invalid URL. Must start with http:// or https://'})
            }

        for _ in range(5):
            short_code = generate_short_code()
            response = table.get_item(Key={'short_code': short_code})
            if 'Item' not in response:
                table.put_item(Item={
                    'short_code': short_code,
                    'long_url': long_url
                })
                return {
                    'statusCode': 200,
                    'headers': HEADERS,
                    'body': json.dumps({
                        'short_code': short_code,
                        'message': 'Short URL created successfully'
                    })
                }

        return {
            'statusCode': 500,
            'headers': HEADERS,
            'body': json.dumps({'message': 'Failed to generate unique short code, please try again'})
        }

    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': HEADERS,
            'body': json.dumps({'message': 'Invalid JSON in request body'})
        }
    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'headers': HEADERS,
            'body': json.dumps({'message': 'Internal server error'})
        }