import base64
import io
import os
import uvicorn
from bedrock_helper import get_image_description
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image

app = FastAPI(
    title="Image Analyser",
    description="An application that analyses images using Amazon Bedrock's Claude Sonnet 4 model."
)

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page"""
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "Image Analyser"}
    )

@app.post("/analyse", response_class=HTMLResponse)
async def analyse_image(request: Request, file: UploadFile = File(...)):
    """Process the uploaded image and get analysis from Amazon Bedrock Claude Sonnet 4"""
    try:
        # Read and process the image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to base64 for Bedrock
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Get image description from Claude Sonnet 4 via Bedrock
        description = get_image_description(img_str)
        
        # Return the template with results
        return templates.TemplateResponse(
            "result.html", 
            {
                "request": request, 
                "title": "Image Analysis Results",
                "description": description,
                "image_data": f"data:image/jpeg;base64,{img_str}"
            }
        )
    except Exception as e:
        error_message = str(e)
        if "AccessDeniedException" in error_message:
            error_message = "Please check your AWS credentials and Bedrock access permissions."
        
        return templates.TemplateResponse(
            "error.html", 
            {
                "request": request,
                "title": "Error",
                "error": error_message
            }
        )

@app.get("/favicon.ico")
async def favicon():
    """Serve the favicon.ico file"""
    return FileResponse("favicon.ico")

@app.get("/health", response_class=HTMLResponse)
async def health_check():
    """Health check endpoint for monitoring application status"""
    return HTMLResponse(content="OK", status_code=200)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
