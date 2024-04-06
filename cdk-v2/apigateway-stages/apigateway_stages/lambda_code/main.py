import os

def handler(event, context):
    api_url = os.environ['API_URL']
    return {
        'statusCode': 200,
        'body': f'La URL de mi API Gateway es {api_url}'
    }