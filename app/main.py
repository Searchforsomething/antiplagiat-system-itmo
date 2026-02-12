import os
import zipfile
from pathlib import Path
from typing import Dict, List

import requests

from app.llm_client import LLMClient
from app.llm_output_parser import parse_files

zip_dir = Path("../files")


def main(task: str, upload_url: str) -> dict:
    """
    Entry point:
        1. Generate AI code from multiple models
        2. Create one ZIP archive per model
        3. Store archives in ./files directory
    """
    zip_dir.mkdir(parents=True, exist_ok=True)

    print("zip dir created")

    code_files = get_ai_code(task)

    print("code files created")

    archives = create_zip_per_model(code_files, zip_dir)

    print("archive files created")

    upload_response = upload_archives(archives, upload_url)
    upload_success = upload_response is not None and upload_response.ok
    upload_status = upload_response.status_code if upload_response else None

    return {
        "archives": archives,
        "upload_success": upload_success,
        "upload_status": upload_status
    }


def upload_archives(archives: List[Path], upload_url) -> requests.Response | None:
    """
    Upload multiple ZIP archives to the API endpoint
    """
    files_payload = []

    for archive_path in archives:
        files_payload.append(
            (
                "files",
                (
                    archive_path.name,
                    open(archive_path, "rb"),
                    "application/zip"
                )
            )
        )

    try:
        response = requests.post(upload_url, files=files_payload)
        return response
    except Exception as e:
        print(f"Error uploading files: {e}")
        return None
    finally:
        for _, file_tuple in files_payload:
            file_tuple[1].close()


def get_ai_code(task: str) -> dict:
    """
    Generate source code artifacts using multiple Large Language Models (LLMs).
    Returns dict:
    {
        <model name>: [{ "filename": "...", "code": "..." }, ...],
        <model name>: [{ "filename": "...", "code": "..." }, ...],
        ...
    }
    """
    code_files = {}
    client = LLMClient(task)
    openrouter_responses = client.get_openrouter_responses()
    gemini_responses = client.get_gemini_responses()

    for responses in openrouter_responses, gemini_responses:
        for model, code in responses.items():
            code_files[model] = parse_files(code)

    return code_files

def sanitize_name(name: str) -> str:
    """
    Make a filesystem-safe name.
    """
    return (
        name.replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_")
    )


def create_zip_per_model(
    code_dict: Dict[str, List[dict]],
    output_dir: Path
) -> List[Path]:
    """
    Create a separate ZIP archive for each model.
    """
    created_archives = []

    for model_name, files in code_dict.items():
        if not files:
            continue

        safe_model = sanitize_name(model_name)
        zip_path = output_dir / f"{safe_model}.zip"

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:

            for file_obj in files:
                filename = sanitize_name(
                    file_obj.get("filename", "unknown.txt")
                )

                filename = os.path.basename(filename)

                code = file_obj.get("code", "")

                zipf.writestr(filename, code)

        created_archives.append(zip_path)

    return created_archives

#
# if __name__ == "__main__":
#     main(task=TASK)
