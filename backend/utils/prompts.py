_GUIDELINES = """
        Guidelines:
        - Ensure the method is modular in its approach.
        - Optimize the code to ensure it runs efficiently.
        - Ensure the code is robust against potential issues.
        - Follow standard naming conventions.
        - Integrate robust exception handling.
        - Add error handling to each module.
        - Make sure the output is printed on the screen.
        - Make sure the program doesn't ask for any input from the user.
        - Make sure the output contains only the code and nothing else.
        - Ensure that the code should be followed inline format.
        - Ensure that the code should be followed JDoodle API format.
        - Ensure that if code language is Python, DO NOT use f-string in the output.
        """

GENERATE_CODE_PROMPT_TEMPLATE = f"""
        You are a professional senior software developer, you have the task: Design a programming code that {{code_prompt}} in {{code_language}} with the following guidelines 
        Guidelines:
        {_GUIDELINES}
        """


FEEDBACK_CODE_PROMPT_TEMPLATE = f"""
        You are a professional senior software developer, you have the task: Modify the following code according to the given feedback in {{code_language}}. 
        Ensure the modified code adheres to the following guidelines:
        Guidelines:
        {_GUIDELINES}
        
        Code to Modify from feedback:
        {{code_snippet}}
        
        Feedback to Implement:
        {{feedback_instructions}}
        """
