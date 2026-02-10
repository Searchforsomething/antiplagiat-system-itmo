from llm_client import LLMClient
from llm_output_parser import parse_files


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
