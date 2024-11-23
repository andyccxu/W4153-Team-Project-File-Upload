# File Management Microservice with AWS S3

## Overview

This microservice handles the user uploaded images and other files by storing them in AWS S3 and retrieve them later.

You should provide AWS credentials for accessing S3 service in a local `.env` file, which should look like:

```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_BUCKET_NAME=
AWS_REGION=
```

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
