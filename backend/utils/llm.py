import traceback

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama

from utils.logger import logger
from utils.prompts import FEEDBACK_CODE_PROMPT_TEMPLATE, GENERATE_CODE_PROMPT_TEMPLATE
from fastapi import HTTPException, status


class LLMLangChain:
    code_snippet_chain = None
    feedback_code_chain = None
    code_language = "Python"
    llm = None

    def __init__(
        self,
        code_language: str = "python",
        model: str = "mistral",
        verbose: bool = True,
    ):
        self.code_language = code_language
        self.llm = Ollama(
            model=model,
        )
        self.verbose = verbose

        logger.info(
            f"Initializing LLMLangChain... with parameters: {code_language}, {model}"
        )

        # Prompt Templates for code snippets
        code_template = PromptTemplate(
            input_variables=[
                "code_prompt",
                "code_language",
            ],
            template=GENERATE_CODE_PROMPT_TEMPLATE,
        )

        # Create a LLM chain that generates the code
        self.code_snippet_chain = LLMChain(
            llm=self.llm,
            prompt=code_template,
            output_key="code",
            verbose=self.verbose,
        )

        # Auto debug chain
        feedback_code_template = PromptTemplate(
            input_variables=[
                "code_language",
                "code_snippet",
                "feedback_instructions",
            ],
            template=FEEDBACK_CODE_PROMPT_TEMPLATE,
        )

        self.feedback_code_chain = LLMChain(
            llm=self.llm,
            prompt=feedback_code_template,
            output_key="code_fix",
            verbose=self.verbose,
        )

    def generate_code(
        self,
        code_prompt: str,
        code_language: str,
    ) -> str:
        try:
            # Validate prompt and language
            if not code_prompt:
                error_message = "Error in code generation: Please enter a valid prompt."
                logger.error(error_message)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_message,
                )

            if not code_language:
                error_message = "Error in code generation: Language not specified."
                logger.error(error_message)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_message,
                )

            logger.info(
                f"Generating code for prompt: {code_prompt} in language: {code_language}"
            )

            if self.code_snippet_chain:
                logger.info("Code chain is initialized.")
                code_snippet = self.code_snippet_chain.run(
                    {
                        "code_prompt": code_prompt,
                        "code_language": code_language,
                    }
                )
                logger.info(f"Generated code: {code_snippet[:100]}...")

                extracted_code = self.__extract_code(code_snippet)
                return extracted_code

        except Exception as e:
            error_message = f"Error in code generation: {traceback.format_exc()}"
            logger.error(error_message)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_message,
            )

    def feedback_generated_code(
        self,
        code_snippet: str,
        code_language: str,
        feedback_instructions: str,
    ) -> str:
        """
        Function to modify the generated code based on the feedback.
        """
        try:
            # Check for valid code
            if not code_snippet or len(code_snippet) == 0:
                error_message = "Error in code modification: Please enter a valid code."
                logger.error(error_message)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_message,
                )

            logger.info(f"Modify code")
            if code_snippet and len(code_snippet) > 0:
                logger.info(
                    f"Modify code {code_snippet[:100]}... in language {code_language} according to feedback"
                )

                # Run the chain
                if self.feedback_code_chain:
                    logger.info("Code chain is initialized.")
                    feedback_code_snippet = self.feedback_code_chain.run(
                        {
                            "code_language": code_language,
                            "code_snippet": code_snippet,
                            "feedback_instructions": feedback_instructions,
                        }
                    )
                    logger.info(f"Generated code: {code_snippet[:100]}...")
                    extracted_code = self.__extract_code(feedback_code_snippet)
                    return extracted_code
            else:
                error_message = (
                    "Error in code fixing: Please enter a valid code and language."
                )
                logger.error(error_message)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_message,
                )
        except Exception as e:
            error_message = f"Error in code modification: {traceback.format_exc()}"
            logger.error(error_message)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_message,
            )

    def __extract_code(
        self,
        code: str,
    ) -> str:
        """
        Extracts the code from the provided string.
        If the string contains '```', it extracts the code between them.
        Otherwise, it returns the original string.
        """
        try:
            if "```" in code:
                start = code.find("```") + len("```\n")
                end = code.find("```", start)
                # Skip the first line after ```
                start = code.find("\n", start) + 1
                extracted_code = code[start:end]
                logger.info("Code extracted successfully.")
                return extracted_code
            else:
                logger.info(
                    "No special characters found in the code. Returning the original code."
                )
                return code
        except Exception as exception:
            logger.error(f"Error occurred while extracting code: {exception}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error extracting code",
            )
