from flask_cors import CORS
import os
import uuid
import boto3
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, ClientError
import io

# Load AWS credentials from .env file
load_dotenv()

app = Flask(__name__)
CORS(app,
     origins=["http://localhost:5173",
              "https://ui-app-745799261495.us-east4.run.app"],
     supports_credentials=True)

# AWS S3 setup
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)
BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')


def upload_to_s3(file_obj, bucket_name, object_name=None):
    """Upload a file to an S3 bucket and return the URL."""
    if object_name is None:
        filename = secure_filename(file_obj.filename)[:20]
        object_name = filename + "_" + str(uuid.uuid4())[:50]

    # Upload the file to S3
    try:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
        s3.upload_fileobj(file_obj, bucket_name, object_name)
        return object_name
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None


# /upload endpoint
@app.route('/upload_image', methods=['POST', 'OPTIONS'])
def upload_image():
    if request.method == 'OPTIONS':
        # Handle preflight request
        return jsonify({'message': 'Preflight check successful'}), 200
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']

    # Upload to S3
    image_key = upload_to_s3(image_file, BUCKET_NAME)

    if image_key:
        return jsonify({'image_key': image_key}), 200
    else:
        return jsonify({'error': 'Failed to upload image'}), 500


@app.route('/get_image', methods=['GET', 'OPTIONS'])
def get_image():
    if request.method == 'OPTIONS':
        # Handle preflight request
        return jsonify({'message': 'Preflight check successful'}), 200
    # Get the object name from query parameters
    object_name = request.args.get('object_name')

    if not object_name:
        return jsonify({'error': 'Object name is required'}), 400

    try:
        # Retrieve the object from S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key=object_name)
        print(response)
        image_data = response['Body'].read()

        # Create a BytesIO stream to return the image as a file
        return send_file(io.BytesIO(image_data),
                         mimetype=response['ContentType'],
                         as_attachment=False)

    except NoCredentialsError:
        return jsonify({'error': 'AWS credentials not available'}), 403
    except ClientError as e:
        # Handle specific errors, such as "NoSuchKey"
        return jsonify({'error': str(e)}), e.response['ResponseMetadata']['HTTPStatusCode']


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002)
