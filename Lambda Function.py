import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']  # Tambahkan ini juga di environment variable
def lambda_handler(event, context):
    print("Received event:", event)

    device_id = event.get('device_id')
    timestamp = event.get('timestamp')
    lux = event.get('lux')

    if device_id and timestamp and lux is not None:
        # Simpan ke DynamoDB
        table.put_item(
            Item={
                'device_id': device_id,
                'timestamp': timestamp,
                'lux': lux
            }
        )

        # Simpan ke latest.json di S3
        latest_data = {
            'device_id': device_id,
            'timestamp': timestamp,
            'lux': lux
        }

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key='latest.json',
            Body=json.dumps(latest_data),
            ContentType='application/json',
            # ACL='public-read'  # opsional, jika ingin bisa diakses publik
        )

        return {
            'statusCode': 200,
            'body': 'Data inserted and latest.json updated successfully'
        }
    else:
        return {
            'statusCode': 400,
            'body': 'Missing data in the event'
        }