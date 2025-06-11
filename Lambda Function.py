import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Your Table Name')

def lambda_handler(event, context):
    print("📥 Incoming event:", json.dumps(event))

    try:
        # langsung akses key
        device_id = event['device_id']
        lux = int(event['lux'])
        timestamp = event['timestamp']

        # insert ke DynamoDB
        response = table.put_item(
            Item={
                'device_id': device_id,
                'timestamp': timestamp,
                'lux': lux
            }
        )

        print(f"✅ Data saved: {device_id}, lux: {lux}, time: {timestamp}")
        return {
            'statusCode': 200,
            'body': json.dumps('IoT data saved to DynamoDB')
        }

    except Exception as e:
        print(f"❌ Error saving to DynamoDB: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
