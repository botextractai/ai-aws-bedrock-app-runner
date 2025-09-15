# Image Analyser web app

This example is a FastAPI application that analyses images using Amazon Bedrock's Claude Sonnet 4 model.

You can run this web app in two different ways:

1. **Local execution:** Follow the instructions below.
2. **AWS App Runner deployment:** This application is configured for deployment to AWS App Runner. For detailed AWS App Runner deployment instructions, see [APPRUNNER_DEPLOYMENT.md](APPRUNNER_DEPLOYMENT.md).

## What is AWS App Runner?

AWS App Runner is a fully managed service that lets you deploy and run web applications and APIs directly from your source code (from a Github repository) or a container image, without having to set up or manage servers or infrastructure (such as virtual machines or Docker). With AWS App Runner, you automatically get HTTPS, load balancing, health checks, and scaling up or down based on traffic.

AWS App Runner is a "source-code-in, running-web-service-out" platform that is comparable to platforms like Heroku, Render, or Google App Engine.

In this example, AWS App Runner pulls the program code (this repository) from Github and automatically builds a Docker container image (using its built-in build system, based on buildpacks). It then runs this image in a managed container environment, handles scaling, health checks, and updates, and exposes the application to the public internet. AWS App Runner automatically creates a new internal image for each deployment that it manages for you.

## Web app features

- Upload an image via the web interface
- Get AI-powered analysis of image content
- View detailed descriptions of what's in the image

## How this web app works

The application:

1. Accepts image uploads from users. The `data` folder contains 2 example images for you to analyse.
2. Converts the image to base64 format
3. Sends the image to Amazon Bedrock's Claude Sonnet 4 model
4. Displays the AI's analysis of the image content

![alt text](https://github.com/user-attachments/assets/0e449831-dfea-4314-b95f-200c6a4e8784 "Image Analysis Results")

## Requirements

- Python 3.11+
- AWS account with Amazon Bedrock access
- Access to the Claude Sonnet 4 model in Amazon Bedrock

## Required environment variable settings for this example

1. You need your AWS Access Key ID for this example.
2. You also need your AWS Secret Access Key for this example.
3. You must ensure that you have access to the Claude Sonnet 4 model in Amazon Bedrock in your AWS Default Region. Please ensure your AWS credentials have appropriate permissions for Amazon Bedrock and for the Claude Sonnet 4 model.
4. Enter the previous 3 values in the `.env.example` file and rename this file to just `.env` (remove the ".example" ending).

## Running this web app locally (without AWS App Runner)

```
uvicorn main:app --reload
```

Or run directly:

```
python main.py
```

The application will be available at http://localhost:8000
