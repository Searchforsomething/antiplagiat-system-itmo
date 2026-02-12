from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from app.main import main
from app.constants import API_UPLOAD_URL_TEMPLATE

load_dotenv()

app = FastAPI()


@app.post("/api/v1/create")
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

    # Формируем URL загрузки
    # Пример: http://localhost:8080/api/upload/works/lab_1
    upload_url = f"{API_UPLOAD_URL_TEMPLATE}/{storage_path}"

    try:
        archives = main(task_text, upload_url)

        if not archives:
            raise HTTPException(
                status_code=500,
                detail="No archives were generated"
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "storagePath": storage_path,
                "upload_url": upload_url,
                "generated_archives": [str(path) for path in archives]
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Generation failed: {str(e)}"
        )
