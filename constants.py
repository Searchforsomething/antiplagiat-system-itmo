OPENROUTER_MODELS = {
    "DeepSeek: R1 0528": "deepseek/deepseek-r1-0528:free",
    "TNG: DeepSeek R1T2 Chimera": "tngtech/deepseek-r1t2-chimera:free",
    "TNG: DeepSeek R1T Chimera": "tngtech/deepseek-r1t-chimera:free",
    "Arcee AI: Trinity Large Preview": "arcee-ai/trinity-large-preview:free",
    "StepFun: Step 3.5 Flash": "stepfun/step-3.5-flash:free",
    "Z.AI: GLM 4.5 Air": "z-ai/glm-4.5-air:free",
    "NVIDIA: Nemotron 3 Nano 30B A3B": "nvidia/nemotron-3-nano-30b-a3b:free",
    "NVIDIA: Nemotron Nano 9B V2": "nvidia/nemotron-nano-9b-v2:free"
}
OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'

GEMINI_MODELS = {
    "Gemini 3 Flash": "gemini-3-flash-preview",
}

GENERATION_PROMPT_ADDITION = """

Ответь только выводом кода, не добавляй никакое описание от себя. Используй формат ответа:
# <filename>
```<language>
<code>
```
# <filename>
```<language>
<code>
```
"""
