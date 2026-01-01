import streamlit as st
import boto3
import json
import time
import pandas as pd
from PIL import Image
import PyPDF2
from io import BytesIO
import os

# Initialize AWS clients
bedrock_automation_client = boto3.client('bedrock-data-automation', region_name='us-west-2')
bedrock_runtime_client = boto3.client('bedrock-data-automation-runtime', region_name='us-west-2')
s3_client = boto3.client('s3')

# bucket_name = 'bedrock-bda-us-west-2-683ac04f-fdec-4d70-8794-07acbf8b4d58'
bucket_name = os.environ.get('S3_BUCKET_NAME')
Payslip_Data_Automation_ARN = os.environ.get('PAYSLIP_DATA_AUTOMATION_ARN')

def upload_file_to_s3(file, filename):
    try:
        s3_key = f'input_data/{filename}'
        # Read the file content into bytes
        file_bytes = BytesIO(file.getvalue())
        # Upload to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=file_bytes.getvalue(),
            ContentType=file.type
        )
        # Verify the file exists in S3
        try:
            s3_client.head_object(Bucket=bucket_name, Key=s3_key)
        except Exception as e:
            st.error(f"File upload verification failed: {e}")
            return None
            
        return f"s3://{bucket_name}/{s3_key}"
    except Exception as e:
        st.error(f"Error uploading to S3: {e}")
        return None

def invoke_data_automation(input_s3_uri, output_s3_uri, document_type):
    try:
        # Verify S3 access before invoking
        input_key = input_s3_uri.split(f"{bucket_name}/")[1]
        try:
            s3_client.head_object(Bucket=bucket_name, Key=input_key)
        except Exception as e:
            st.error(f"Cannot access input file in S3: {e}")
            return None

        response = bedrock_runtime_client.invoke_data_automation_async(
            inputConfiguration={'s3Uri': input_s3_uri},
            outputConfiguration={'s3Uri': output_s3_uri},
            dataAutomationConfiguration={
                'dataAutomationArn': DATA_AUTOMATION_ARNS[document_type],
                'stage': 'LIVE'
            }
        )
        return response['invocationArn']
    except Exception as e:
        st.error(f"Error invoking data automation: {e}")
        return None

def check_invocation_status(invocation_arn):
    return bedrock_runtime_client.get_data_automation_status(invocationArn=invocation_arn)

def display_inference_result(custom_output_path):
    try:
        object_key = custom_output_path[len(f"s3://{bucket_name}/"):]
        result = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        content = json.loads(result['Body'].read())
        inference_result = content.get('inference_result', {})
        
        # Create DataFrame only with non-null values and sort by Field
        filtered_results = {k: v for k, v in inference_result.items() if v is not None and v != ''}
        if filtered_results:
            df = pd.DataFrame(list(filtered_results.items()), columns=['Field', 'Value'])
            df = df.sort_values('Field').reset_index(drop=True)  # Sort by Field name and reset index
            
            # Add numbered index starting from 1
            df.index = range(1, len(df) + 1)
            
            # Display the DataFrame with the custom index
            st.table(df)
        else:
            st.warning("No valid results found in the document.")
                
    except Exception as e:
        st.error(f"Error fetching output: {e}")

def display_file_content(uploaded_file):
    if uploaded_file.type == "image/png":
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_container_width=True)
    elif uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page_num in range(len(pdf_reader.pages)):
            st.write(f"Page {page_num + 1}")
            st.write(pdf_reader.pages[page_num].extract_text())

# Streamlit UI
st.title("Turn Raw Documents into Actionable Data")

# Use session state to track changes in document type
if 'previous_selection' not in st.session_state:
    st.session_state.previous_selection = None

# Add select box for document type
document_type = st.selectbox(
    "Select Document Type",
    ("Payslip")
)

# Check if document type has changed
if st.session_state.previous_selection != document_type:
    # Reset all session state variables
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.previous_selection = document_type
    # Rerun the app to clear all widgets
    st.rerun()

# Define ARNs based on document type
DATA_AUTOMATION_ARNS = {
    # "Payslip": "arn:aws:bedrock:us-west-2:680038756295:data-automation-project/fa1b4fa8ffc8"
    "Payslip": Payslip_Data_Automation_ARN
}

uploaded_file = st.file_uploader("Upload PDF or PNG file", type=["pdf", "png"], key="file_uploader")

if uploaded_file is not None:
    # Display the uploaded file content
    display_file_content(uploaded_file)
    
    # Process the file
    with st.spinner('Extracting data from document...'):
        file_s3_uri = upload_file_to_s3(uploaded_file, uploaded_file.name)
        if file_s3_uri:
            invocation_arn = invoke_data_automation(file_s3_uri, f"{file_s3_uri}/output", document_type)
            if invocation_arn:
                status = 'Pending'
                while status != 'Success':
                    response = check_invocation_status(invocation_arn)
                    status = response['status']
                    
                    if status == 'Success':
                        try:
                            output_s3_uri = response['outputConfiguration']['s3Uri']
                            result = s3_client.get_object(
                                Bucket=bucket_name, 
                                Key=output_s3_uri[len(f"s3://{bucket_name}/"):]
                            )
                            job_metadata_json = json.loads(result['Body'].read())
                            
                            output_metadata = job_metadata_json.get("output_metadata", [])
                            if output_metadata and output_metadata[0]['segment_metadata']:
                                custom_output_path = output_metadata[0]['segment_metadata'][0]['custom_output_path']
                                st.write("### Structured Data Extracted from Document:")
                                display_inference_result(custom_output_path)
                            else:
                                st.error("Custom output path not found in job metadata.")
                        except Exception as e:
                            st.error(f"Error processing results: {e}")
                        break
                    time.sleep(5)