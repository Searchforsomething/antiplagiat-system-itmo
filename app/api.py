import os

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from app.main import main

load_dotenv()

app = FastAPI()

api_upload_url_template = os.getenv("API_UPLOAD_URL_TEMPLATE")

@app.post("/api/v1/templates/create")
async def generate(
    file: UploadFile = File(...),
    storage_path: str = Form(...)
):
    """
    Accept a task file + storage path,
    generate AI code archives,
    upload them,
    and return result.
    """

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    if not storage_path:
        raise HTTPException(status_code=400, detail="storagePath is required")

    try:
        contents = await file.read()
        task_text = contents.decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to read file")

    upload_url = f"{api_upload_url_template}/{storage_path}/upload"

    try:
        result = main(task_text, upload_url)

        if not result["archives"]:
            raise HTTPException(status_code=500, detail="No archives were generated")

        return JSONResponse(
            status_code=200,
            content={
                "status": "success" if result["upload_success"] else "upload_failed",
                "storagePath": storage_path,
                "upload_url": upload_url,
                "upload_status": result["upload_status"],
                "generated_archives": [str(path) for path in result["archives"]]
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Generation failed: {str(e)}"
        )
