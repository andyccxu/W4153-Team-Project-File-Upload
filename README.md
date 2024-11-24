# File Storage Microservice with AWS S3

## Overview

This microservice handles the user uploaded images and other files by storing them in AWS S3 and retrieve them later.

You should provide AWS credentials for accessing S3 service in a local `.env` file, which should look like:

```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_BUCKET_NAME=
AWS_REGION=
```

## Deployment

We deployed this service using Google Cloud VM + Docker container.

Build the docker image locally and push it to Google Artifact Registry. Alternatively, we can use Google Cloud Build to build the image remotely.

In the root directory of the project, write a Dockerfile and run
```
gcloud builds submit --region=us-east4 --tag us-east4-docker.pkg.dev/YOUR_PROJECT_ID/YOUR_REPO_NAME/YOUR_IMAGE_NAME
```

Then, ssh to the VM, manually copy over the .env file with AWS credentials, and run

```
docker run -d -p 8080:8080 --env-file .env us-east4-docker.pkg.dev/YOUR_PROJECT_ID/YOUR_REPO_NAME/YOUR_IMAGE_NAME
```

In this way, the .env file with secrets will not be added to the docker image.



## API Endpoints

### GET /get_image

This endpoint allows users to retrieve an image from the S3 bucket by providing its object name.

Parameters:
- `object_name`

Returns: image content in bytes stream

Test the endpoint using curl:

```
curl -o test.heic "http://127.0.0.1:8080/get_image?object_name=2153816011290181632.heic"
```


### POST /upload_image

This endpoint allows users to upload an image to the S3 bucket. It returns the object name (Key) stored in AWS S3.

Body parameters:
- `image`: 

Response:
- `object_name`
