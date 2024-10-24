from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import os
import json
from datetime import datetime
import uuid
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()

# Pydantic models
class UploadUrlRequest(BaseModel):
    fileName: str

class MockupRequest(BaseModel):
    templates: List[str]
    designs: List[str]
    category: str

class MockupResponse(BaseModel):
    id: str
    mockupKey: str
    templateName: str
    designName: str

# Configure AWS client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION'),
    config=Config(signature_version='s3v4')
)

@router.post("/get-upload-url")
async def get_upload_url(request: UploadUrlRequest):
    try:
        # Generate pre-signed URL for uploading to S3
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': os.getenv('S3_BUCKET'),
                'Key': f'designs/{request.fileName}',
                'ContentType': 'image/png'
            },
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return {"uploadUrl": presigned_url}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-mockup")
async def generate_mockup(request: MockupRequest):
    try:
        # This will hold our generated mockups
        mockups = []

        # For each design and template combination
        for design in request.designs:
            for template in request.templates:
                # Generate a unique ID for this mockup
                mockup_id = str(uuid.uuid4())

                # Create the mockup filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                mockup_key = f"mockups/{request.category}/{timestamp}_{mockup_id}.png"

                # In a real implementation, you would:
                # 1. Load the template image
                # 2. Load the design image from S3
                # 3. Composite them together
                # 4. Upload the result to S3

                # For now, we'll just create a mockup response
                mockup = MockupResponse(
                    id=mockup_id,
                    mockupKey=mockup_key,
                    templateName=template,
                    designName=design
                )
                mockups.append(mockup)

        return mockups
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/thumbnails/{category}")
async def get_thumbnails(category: str):
    try:
        # List objects in the S3 bucket with the given category prefix
        response = s3_client.list_objects_v2(
            Bucket=os.getenv('S3_BUCKET'),
            Prefix=f'templates/{category}/'
        )

        # Extract thumbnail filenames
        thumbnails = []
        if 'Contents' in response:
            for item in response['Contents']:
                key = item['Key']
                filename = key.split('/')[-1]
                thumbnails.append(filename)

        return thumbnails
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))