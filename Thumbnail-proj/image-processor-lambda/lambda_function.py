import boto3
import os
from urllib.parse import unquote_plus
from PIL import Image

# Initialize AWS clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Get environment variables
DEST_BUCKET_NAME = os.environ['DEST_BUCKET_NAME']
DDB_TABLE_NAME = os.environ['DDB_TABLE_NAME']
THUMBNAIL_SIZE = (200, 200)

def lambda_handler(event, context):
    """
    This function is triggered by an S3 event. It resizes the uploaded image
    to a thumbnail and stores it in another S3 bucket. It also logs metadata
    to a DynamoDB table.
    """
    try:
        # 1. Get the bucket and key from the S3 event
        record = event['Records'][0]
        source_bucket = record['s3']['bucket']['name']
        source_key = unquote_plus(record['s3']['object']['key']) # Handles spaces, etc.
        
        print(f"Processing image '{source_key}' from bucket '{source_bucket}'.")

        # 2. Download the original image from S3 to the /tmp/ directory
        # Lambda provides /tmp/ as temporary storage
        download_path = f'/tmp/{os.path.basename(source_key)}'
        s3_client.download_file(source_bucket, source_key, download_path)
        
        # 3. Resize the image using Pillow
        thumbnail_path = f'/tmp/thumbnail-{os.path.basename(source_key)}'
        with Image.open(download_path) as image:
            image.thumbnail(THUMBNAIL_SIZE)
            image.save(thumbnail_path)
            
        # 4. Upload the thumbnail to the destination S3 bucket
        processed_key = f"thumbnails/{os.path.basename(source_key)}"
        s3_client.upload_file(thumbnail_path, DEST_BUCKET_NAME, processed_key)
        
        print(f"Successfully created thumbnail and uploaded to '{DEST_BUCKET_NAME}/{processed_key}'.")

        # 5. Store metadata in DynamoDB
        table = dynamodb.Table(DDB_TABLE_NAME)
        table.put_item(
            Item={
                'imageId': source_key,
                'processedBucket': DEST_BUCKET_NAME,
                'processedKey': processed_key,
                'uploadTimestamp': record['eventTime']
            }
        )
        print(f"Successfully logged metadata to DynamoDB table '{DDB_TABLE_NAME}'.")

        return {
            'statusCode': 200,
            'body': 'Image processed successfully!'
        }

    except Exception as e:
        print(f"Error processing image: {e}")
        # Optionally, you could add logic to log the failure to DynamoDB
        raise e