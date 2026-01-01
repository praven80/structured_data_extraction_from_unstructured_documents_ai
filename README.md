# Document Data Extraction Platform

An automated document processing platform built with AWS Bedrock Data Automation and Streamlit, designed to extract structured data from various documents.

You can view a short demo video in the "Demo" folder.

## Features

- PDF and PNG document upload support
- Automated data extraction
- Real-time processing status
- Structured data presentation
- S3 integration for document storage
- Customizable extraction schema
- Interactive web interface

## Architecture

### Components
- Frontend: Streamlit web application
- Backend: AWS Bedrock Data Automation
- Storage: Amazon S3
- Infrastructure: AWS ECS (Fargate)

### AWS Services Used
- AWS Bedrock Data Automation
- Amazon S3
- Amazon ECS
- AWS IAM
- Application Load Balancer
- CloudWatch Logs

## Prerequisites

- AWS Account with access to:
  - AWS Bedrock
  - Amazon ECS
  - Amazon S3
  - AWS IAM
- Python 3.9+
- Docker
- AWS CDK

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd document-extraction
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install AWS CDK (if not already installed):
```bash
npm install -g aws-cdk
```

## Deployment

1. Configure AWS credentials:
```bash
aws configure
```

2. Bootstrap CDK (first time only):
```bash
cdk bootstrap
```

3. Deploy the stack:
```bash
cdk deploy
```

## Environment Variables

Required environment variables:
```bash
S3_BUCKET_NAME=<your-s3-bucket>
PAYSLIP_DATA_AUTOMATION_ARN=<bedrock-automation-arn>
```

## Usage

1. Access the application through the ALB DNS
2. Select document type (currently supports Payslip)
3. Upload PDF or PNG file
4. View extracted structured data

## Infrastructure

The application is deployed with:
- VPC with public/private subnets
- ECS Fargate cluster
- Application Load Balancer
- S3 bucket for document storage
- IAM roles and policies

## Docker Support

Build the container:
```bash
docker build -t doc-extraction .
```

Run locally:
```bash
docker run -p 8501:8501 doc-extraction
```

## Development

### Local Development
```bash
streamlit run app.py
```

### Adding New Document Types
1. Create new blueprint in `create_bedrock_data_automation.py`
2. Define schema for new document type
3. Update Streamlit interface

## Security

- Private subnets for container deployment
- Security groups for network access control
- VPC isolation