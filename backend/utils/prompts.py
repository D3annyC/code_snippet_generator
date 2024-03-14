_GUIDELINES = """
        Guidelines:
        - Ensure the method is modular in its approach.
        - Optimize the code to ensure it runs efficiently.
        - Ensure the code is robust against potential issues.
        - Follow standard naming conventions.
        - Make sure the output is printed on the screen.
        - Make sure the program doesn't ask for any input from the user.
        - Make sure the output contains only the code and nothing else.
        - Ensure that the code should be followed inline format.
        - Ensure that the code should be followed JDoodle API format.
        - Ensure DO NOT use f-string interpolation in the output that if code language is Python.
        """

GENERATE_CODE_PROMPT_TEMPLATE = f"""
        Ensure the task "{{code_prompt}}" is a validated code generation prompt, if not, please generate code in {{code_language}} to print message to ask user enter a correct code prompt.
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
        Ensure the Feedback "{{feedback_instructions}}" is a validated Feedback, if not, please generate code in {{code_language}} to print message to ask user enter a correct Feedback.
        {{feedback_instructions}}
        """
