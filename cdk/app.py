from aws_cdk import App
from app_stack import AppStack

app = App()

# Fetch parameters from CLI context
s3_bucket_name = app.node.try_get_context("s3BucketName")
payslip_data_automation_arn = app.node.try_get_context("payslipDataAutomationArn")

AppStack(
    app, 
    "AppStack1"
)
app.synth()