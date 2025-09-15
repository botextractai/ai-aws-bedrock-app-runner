# Deploying to AWS App Runner

This markdown document provides instructions for deploying this web app to AWS App Runner.

## Prerequisites

1. AWS Account with appropriate permissions
2. Access to the Amazon Bedrock service for the Claude Sonnet 4 model
3. Your source code (this repository) must to be available from Github

## AWS App Runner Deployment

### Step 1: Create an IAM role in the AWS console

- Navigate to "IAM"
- Select "Roles"
- Click on "Create role"
- Select "Custom trust policy"
- Enter this "Custom trust policy":
  ```
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Principal": {
                  "Service": "tasks.apprunner.amazonaws.com"
              },
              "Action": "sts:AssumeRole"
          }
      ]
  }
  ```
- Click on "Next"
- Enable (check) the permission policy "AmazonBedrockLimitedAccess"
- Click on "Next"
- In "Role name", enter "apprunner-bedrock-role"
- Click on "Create role"

### Step 2: Create the AWS App Runner service in the AWS console

- Navigate to "AWS App Runner"
- Click on "Create an App Runner service"
- Select "Source code repository"
- In the "Github Connection" section, click on "Add new"
- Set up a connection to your Github repository and branch. In Github, you must grant AWS access to your repository.
- In the "Deployment settings" section, select "Automatic"
- Click on the "Next" button
- Select "Use a configuration file". This will then use the `apprunner.yaml` file for the configuration settings.
- Click on the "Next" button
- Under "Service name", enter a name like "ImageAnalyser"
- Expand the "Health check" section
- Change the protocol setting from "TCP" to "HTTP"
- Change the "Path" setting from "/" to "/health"
- Expand the "Security" section
- Under "Instance role", select the "apprunner-beckrock-role" role that you created in step 1
- Click on "Next"
- Review the settings and click on "Create & deploy"

## Monitoring and Logs

After deployment, you can monitor your application through:

1. AWS App Runner console
2. CloudWatch Logs
3. CloudWatch Metrics
