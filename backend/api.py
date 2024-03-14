import traceback

import requests
import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from utils.lang_codes import get_language_codes
from utils.llm import LLMLangChain
from utils.logger import logger
from utils.models import ExecuteCode, UserFeedback, UserInput

app = FastAPI()
# origins = ['http://localhost:8000',
#            'http://127.0.0.1:8000',
#            'http://localhost:4200',]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def say_hello():
    return {"message": "Hello World"}


@app.post("/code_snippet")
async def generate_code_snippet(body: UserInput):
    try:
        llm_chain = LLMLangChain()
        generated_code_result = llm_chain.generate_code(
            code_prompt=body.code_prompt,
            code_language=body.code_language,
        )

        return {"code_snippet": generated_code_result}
    except Exception as e:
        error_message = f"Error in code generation: {traceback.format_exc()}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message,
        )


@app.post("/feedback_code_snippet")
async def generate_feedback_code_snippet(body: UserFeedback):
    try:
        llm_chain = LLMLangChain()
        feedback_generated_code_result = llm_chain.feedback_generated_code(
            code_snippet=body.code_snippet,
            code_language=body.code_language,
            feedback_instructions=body.feedback_instructions,
        )

        return {"feedback_code_snippet": feedback_generated_code_result}
    except Exception as e:
        error_message = f"Error in code generation: {traceback.format_exc()}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message,
        )


@app.post("/execute_code")
async def execute_code(body: ExecuteCode):
    _CLIENT_ID = "70df0b679a2685cee5135f492b9ecf1e"
    _CLIENT_SECRET_KEY = (
        "4bdd507fabaa3114ed5629db7b6fd0933867228a82d6d5fea8de1a6fb016ced1"
    )
    _JDOODLE_URL = "https://api.jdoodle.com/v1/execute"

    if not body.generated_code or not body.code_language:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Generated code or language is empty",
        )
    logger.info(
        f"Executing code: {body.generated_code[:50]} in language: {body.code_language}."
    )
    try:
        logger.info("Executing code using JDoodle iFrame Embedding")

        payload = {
            "clientId": _CLIENT_ID,
            "clientSecret": _CLIENT_SECRET_KEY,
            "script": body.generated_code,
            "language": get_language_codes()[body.code_language],
            "compileOnly": False,
        }
        response = requests.post(_JDOODLE_URL, json=payload)
        if response.json()["statusCode"] != 200:
            raise HTTPException(
                status_code=response.json()["statusCode"],
                detail=response.json()["error"],
            )
        else:
            return response.json()
    except Exception as e:
        logger.error(f"Error in code execution: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error executing code",
        )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
