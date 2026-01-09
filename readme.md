# AWS Image Processing Pipeline

## About

This project is a fully automated, serverless image processing pipeline built on AWS infrastructure. It demonstrates how to build a scalable, cost-effective solution for automatic image transformation and delivery using cloud-native services.

### What It Does

When you upload an image to the designated S3 bucket, the system automatically:
- Detects the upload event in real-time
- Generates optimized thumbnails (200x200 pixels)
- Stores processed images separately for efficient access
- Records metadata for tracking and auditing
- Delivers images through a global CDN for fast access worldwide

### Key Features

- **Serverless Architecture**: No servers to manage - automatically scales with demand
- **Event-Driven Processing**: Images are processed immediately upon upload
- **Automated Workflow**: End-to-end automation from upload to delivery
- **Metadata Tracking**: Complete audit trail of all processed images in DynamoDB
- **CDN Integration**: Fast global content delivery via CloudFront
- **Secure Access**: Implements best practices for S3 security with Origin Access Identity
- **Cost-Effective**: Pay only for what you use with AWS serverless pricing

### Use Cases

- **Web Applications**: Automatically generate thumbnails for user-uploaded profile pictures or gallery images
- **E-commerce**: Process product images at scale for catalog listings
- **Content Management**: Automate image optimization for blogs and media sites
- **Mobile Apps**: Backend processing for photo-sharing applications
- **Learning**: Understand serverless architecture and AWS service integration

### Technologies Used

- **AWS Lambda**: Serverless compute for image processing
- **Amazon S3**: Object storage for original and processed images
- **Amazon DynamoDB**: NoSQL database for metadata storage
- **Amazon CloudFront**: CDN for global content delivery
- **Python 3.9**: Lambda function runtime
- **Pillow (PIL)**: Python imaging library for thumbnail generation

---

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