from pydantic import BaseModel


class UserInput(BaseModel):
    code_language: str
    code_prompt: str


class UserFeedback(BaseModel):
    code_language: str
    code_snippet: str
    feedback_instructions: str


class ExecuteCode(BaseModel):
    code_language: str
    generated_code: str
