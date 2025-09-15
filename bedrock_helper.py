import boto3
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")

def get_image_description(base64_image):
    """
    Get a description of an image using Claude Sonnet 4 via Amazon Bedrock.
    
    Args:
        base64_image (str): Base64-encoded image string
    
    Returns:
        str: Description of the image
    """
    # With environment variables set, no explicit parameters needed
    bedrock_runtime = boto3.client(service_name="bedrock-runtime")
    
    # Prepare the prompt
    prompt = """
    Analyse this image and provide a detailed description of what you see. Include:
    
    1. Main subjects and objects in the image
    2. Setting or background context
    3. Actions or activities taking place
    4. Notable visual characteristics (colors, style, lighting, etc.)
    5. Any text visible in the image
    
    Be detailed but concise in your analysis.
    """
    
    # Detect image format from base64 string
    image_format = "png"  # Default format
    if base64_image.startswith("/9j/"):
        image_format = "jpeg"
    elif base64_image.startswith("iVBORw0KGgo"):
        image_format = "png"
    elif base64_image.startswith("/9j/4AAQSkZJRg"):
        image_format = "jpg"
    
    # Prepare the request payload for Claude Sonnet 4
    # Note: "anthropic_version" indicates the API version used by Bedrock to 
    # interact with Anthropic models. It is not the model version!
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": f"image/{image_format}",
                            "data": base64_image
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ]
    }
    
    # Make the API call to Bedrock
    response = bedrock_runtime.invoke_model(
        # Use the regular model id for local region inference models, but use 
        # the inference profile ID for "cross-region inference" models
        modelId="apac.anthropic.claude-sonnet-4-20250514-v1:0",  # Bedrock inference profile ID
        body=json.dumps(request_body)
    )
    
    # Parse and extract the response
    response_body = json.loads(response.get("body").read())
    # The command details depend on the model type, in this example for the Anthropic Claude models
    description = response_body.get("content", [{}])[0].get("text", "")
    
    return description
