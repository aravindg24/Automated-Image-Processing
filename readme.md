# AWS Image Processing Pipeline

This project implements a serverless image processing pipeline using AWS services including S3, Lambda, DynamoDB, and CloudFront. The system automatically processes uploaded images, creates thumbnails, and delivers them through a CDN.

## Architecture Overview

1. **Upload Bucket**: Images are uploaded to an S3 bucket (`image-proc-uploads-my-tp-proj`)
2. **Lambda Processing**: S3 events trigger a Lambda function (`ImageProcessor`) 
3. **Processing**: The Lambda function creates thumbnails using the PIL library
4. **Storage**: Processed images are stored in a separate S3 bucket (`image-proc-processed-my-tp-proj`)
5. **Metadata Storage**: Image metadata is stored in DynamoDB (`ImageMetaDAta`)
6. **Content Delivery**: CloudFront distributes the processed images with proper caching

## Project Components

### S3 Buckets
- Upload bucket: `image-proc-uploads-my-tp-proj`
- Processed image bucket: `image-proc-processed-my-tp-proj`

### Lambda Function
The Lambda function is triggered when images are uploaded to the S3 bucket and processes images with the following extensions:
- `.jpg`
- `.jpeg`
- `.png`

### CloudFront Distribution
A CloudFront distribution serves the processed images with:
- HTTPS redirection
- Proper caching configuration
- Origin Access Identity (OAI) for S3 bucket security

### IAM Configuration
- Lambda trust policy: Allows Lambda service to assume the role
- Lambda permissions policy: Grants access to S3 buckets, DynamoDB, and CloudWatch Logs

### S3 Event Notifications
The notification configuration triggers the Lambda function when images are uploaded.

### S3 Bucket Policy
The bucket policy restricts access to the processed image bucket, allowing only CloudFront to access the objects.

### Deployment
This project includes several configuration files:

bucket-policy.json: S3 bucket policy for CloudFront access
cloudfront-config.json: CloudFront distribution configuration
lambda-image-policy.json: IAM policy for Lambda execution role
lambda-trust-policy.json: Trust policy for Lambda role
notification.json: S3 event notification configuration

### Prerequisites
AWS CLI v2
AWS Account with permissions to create the required resources
Python 3.9+ (Lambda function uses Python 3.9)