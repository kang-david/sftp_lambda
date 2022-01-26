import json
from . import run

def lambda_handler(event, context):
    run.operation()
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }