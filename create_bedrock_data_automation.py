import boto3
import json
import os

# Initialize AWS clients
bedrock_automation_client = boto3.client('bedrock-data-automation', region_name='us-west-2')
bedrock_runtime_client = boto3.client('bedrock-data-automation-runtime', region_name='us-west-2')
s3_client = boto3.client('s3')

def check_blueprint_exists(blueprint_name):
    try:
        response = bedrock_automation_client.list_blueprints()
        for blueprint in response['blueprints']:
            if blueprint['blueprintName'] == blueprint_name:
                return True
        return False
    except Exception as e:
        print(f"Error checking blueprint: {e}")
        return False

def create_blueprint(blueprint_name):
    response = bedrock_automation_client.create_blueprint(
        blueprintName=blueprint_name,
        type='DOCUMENT',
        blueprintStage='LIVE',
        schema=json.dumps({
            '\$schema': 'http://json-schema.org/draft-07/schema#',
            'description': 'This document issued by an employer to an employee contains wages received by an employee for a given period. It usually contains the breakdown of each of the income and tax deductions items.',
            'documentClass': 'Payslip',
            'type': 'object',
            'properties': {
                "PayPeriodStartDate": {
                    "type": "string",
                    "inferenceType": "generative",
                    "description": "What is the Pay Period Start Date? YYYY-MM-DD Format"
                },
                "PayPeriodEndDate": {
                    "type": "string",
                    "inferenceType": "generative",
                    "description": "What is the Pay Period End Date? YYYY-MM-DD Format"
                }
            }
        })
    )
    return response['blueprint']['blueprintArn']

def create_blueprint1(blueprint_name):
    response = bedrock_automation_client.create_blueprint(
        blueprintName=blueprint_name,
        type='DOCUMENT',
        blueprintStage='LIVE',
        schema=json.dumps({
            '$schema': 'http://json-schema.org/draft-07/schema#',
            'description': 'default',
            'documentClass': 'default',
            'type': 'object',
            'properties': {
                "PayPeriodStartDate": {
                    "type": "string",
                    "inferenceType": "generative",
                    "description": "What is the Pay Period Start Date? YYYY-MM-DD Format"
                },
                "PayPeriodEndDate": {
                    "type": "string",
                    "inferenceType": "generative",
                    "description": "What is the Pay Period End Date? YYYY-MM-DD Format"
                },
                "PayDate": {
                    "type": "string",
                    "inferenceType": "generative",
                    "description": "What is the Pay Date? YYYY-MM-DD Format"
                },
                "EmployeeName": {
                    "type": "string",
                    "inferenceType": "generative",
                    "description": "Extract the employee name"
                },
                "EmployeeAddress": {
                    "type": "string",
                    "inferenceType": "generative",
                    "description": "Extract the employee address"
                },
                "CompanyAddress": {
                    "type": "string",
                    "inferenceType": "generative",
                    "description": "Extract the company address"
                },
                "FederalFilingStatus": {
                    "type": "string",
                    "inferenceType": "extractive",
                    "description": "What is the Federal Filing Status? If available"
                },
                "StateFilingStatus": {
                    "type": "string",
                    "inferenceType": "extractive",
                    "description": "What is the State Filing Status? (If available)"
                },
                "CurrentGrossPay": {
                    "type": "number",
                    "inferenceType": "extractive",
                    "description": "What is the Current Gross Pay?"
                },
                "YTDGrossPay": {
                    "type": "number",
                    "inferenceType": "extractive",
                    "description": "What is the YTD Gross Pay?"
                },
                "CurrentNetPay": {
                    "type": "number",
                    "inferenceType": "extractive",
                    "description": "What is the Current Net Pay?"
                },
                "YTDNetPay": {
                    "type": "number",
                    "inferenceType": "extractive",
                    "description": "What is the YTD Net Pay?"
                },
                "RegularHourlyRate": {
                    "type": "number",
                    "inferenceType": "extractive",
                    "description": "What is the Regular Hourly Rate? (if available)"
                },
                "HolidayHourlyRate": {
                    "type": "number",
                    "inferenceType": "extractive",
                    "description": "What is the Holiday Hourly Rate? (if available)"
                },
                "YTDFederalTax": {
                    "type": "number",
                    "inferenceType": "extractive",
                    "description": "What is the YTD Federal Taxes amount?"
                },
                "YTDStateTax": {
                    "type": "number",
                    "inferenceType": "extractive",
                    "description": "What are the YTD State Taxes?"
                },
                "is_ytd_gross_pay_highest": {
                    "type": "boolean",
                    "inferenceType": "extractive",
                    "description": "Is the YTD Gross Pay the largest amount in the entire paystub?"
                },
                "FederalTaxes": {
                    "type": "boolean",
                    "inferenceType": "extractive",
                    "description": "Extract the federal taxes"
                },
                "StateTaxes": {
                    "type": "boolean",
                    "inferenceType": "extractive",
                    "description": "Extract the state taxes"
                },
                "CityTaxes": {
                    "type": "boolean",
                    "inferenceType": "extractive",
                    "description": "Extract the city taxes"
                },
                "EmployeeNumber": {
                    "type": "string",
                    "inferenceType": "extractive",
                    "description": "What is the employee number?"
                },
                "PayrollNumber": {
                    "type": "string",
                    "inferenceType": "extractive",
                    "description": "What is the payroll number?"
                },
                "YTDCityTax": {
                    "type": "number",
                    "inferenceType": "extractive",
                    "description": "What are the YTD City Taxes?"
                },
                "CurrentTotalDeductions": {
                    "type": "number",
                    "inferenceType": "extractive",
                    "description": "What are the current total deductions?"
                },
                "YTDTotalDeductions": {
                    "type": "number",
                    "inferenceType": "extractive",
                    "description": "What are the YTD total deductions?"
                },
                "is_gross_pay_valid": {
                    "type": "boolean",
                    "inferenceType": "generative",
                    "description": "Is the YTD gross pay the largest dollar amount value on the paystub?"
                },
                "are_field_names_sufficient": {
                    "type": "boolean",
                    "inferenceType": "generative",
                    "description": "Are field names / key values sufficient for any validation?"
                },
                "currency": {
                    "type": "string",
                    "inferenceType": "generative",
                    "description": "What currency is used in this document? CAD, USD, EUR, etc."
                }
            }
        }),
    )
    return response['blueprint']['blueprintArn']

def check_project_exists(project_name):
    next_token = None
    while True:
        if next_token:
            response = bedrock_automation_client.list_data_automation_projects(NextToken=next_token)
        else:
            response = bedrock_automation_client.list_data_automation_projects()
        
        for project in response['projects']:
            if project['projectName'] == project_name:
                return project['projectArn']
        
        next_token = response.get('nextToken')
        if not next_token:
            break
    return None

def create_project(project_name, blueprint_arn):
    response = bedrock_automation_client.create_data_automation_project(
        projectName=project_name,
        projectDescription=project_name,
        projectStage='LIVE',
        standardOutputConfiguration={
            'document': {
                'outputFormat': {
                    'textFormat': {
                        'types': ['PLAIN_TEXT']
                    },
                    'additionalFileFormat': {
                        'state': 'ENABLED',
                    }
                }
            },
        },
        customOutputConfiguration={
            'blueprints': [
            {
                'blueprintArn': blueprint_arn
            }
            ],
        },
        overrideConfiguration={
            'document': {
                'splitter': {
                    'state': 'ENABLED'
                }
            }
        },
    )
    return response['projectArn']

blueprint_name = 'custom_payslip'
project_name = 'custom_payslip_project'

# Get AWS account and region details
session = boto3.session.Session()
region = session.region_name

sts_client = boto3.client("sts")
account_id = sts_client.get_caller_identity()["Account"]

if not check_blueprint_exists(blueprint_name):
    blueprint_arn = create_blueprint1(blueprint_name)
else:
    blueprint_arn = f"arn:aws:bedrock:us-west-2:{account_id}:blueprint/{blueprint_name}"
    
project_arn = check_project_exists(project_name)
if not project_arn:
    project_arn = create_project(project_name, blueprint_arn)

# Print output as JSON
output = {
    "final_project_arn": project_arn
}
print(json.dumps(output))