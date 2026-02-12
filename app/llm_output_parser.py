import re
from typing import List, Dict

FILE_BLOCK_RE = re.compile(
    r"""
    ^\#\s+(?P<filename>[^\n]+)\n
    ```[^\n]*\n
    (?P<fenced_code>.*?)
    ```
    """,
    re.MULTILINE | re.DOTALL | re.VERBOSE,
)


def parse_files(text: str) -> List[Dict[str, str]]:
    """
    Parse LLM response, returns list of dictionaries containing filename and code:
    [{ "filename": "...", "code": "..." }, ...]
    """
    result = []
    for match in FILE_BLOCK_RE.finditer(text):
        filename = match.group("filename").strip()

        code = match.group("fenced_code")
        if code is None:
            code = match.group("plain_code")

        result.append({
            "filename": filename,
            "code": code.rstrip("\n"),
        })

    return result
