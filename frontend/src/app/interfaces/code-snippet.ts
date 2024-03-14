export interface CodeSnippet {
  code_language: string;
  code_prompt: string;
}

export interface CodeExecute {
  code_language: string;
  generated_code: string;
}

export interface Feedback {
  code_snippet: string;
  code_language: string;
  feedback_instructions: string;
}
