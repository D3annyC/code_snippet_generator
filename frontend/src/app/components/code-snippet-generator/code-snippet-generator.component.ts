import { Component, OnInit, inject, signal } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { HighlightModule } from 'ngx-highlightjs';
import { CodeSnippetService } from '../../services/code-snippet.service';

@Component({
  selector: 'app-code-snippet-generator',
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, HighlightModule],
  templateUrl: './code-snippet-generator.component.html',
  styleUrl: './code-snippet-generator.component.scss',
})
export class CodeSnippetGeneratorComponent implements OnInit {
  private _fb = inject(FormBuilder);
  private _codeSnippetService = inject(CodeSnippetService);

  generateCodeSnippetForm: FormGroup;
  feedbackForm: FormGroup;

  isGenerateCode: boolean = false;
  isExecutingCode: boolean = false;
  hiddenGenerateCode: boolean = false;
  hiddenFeedbackCode: boolean = true;
  disableGenerateCode: boolean = false;
  disableExecuteCode: boolean = false;
  disableFeedbackCode: boolean = false;

  generated_code = signal<string | undefined | null>(null);
  code_language = signal<string | undefined | null>(null);
  executed_result = signal<string | undefined | null>(null);
  feedback_instructions = signal<string | undefined | null>(null);

  constructor() {
    this.generateCodeSnippetForm = this._fb.group({
      code_prompt: new FormControl('', Validators.required),
      code_language: new FormControl('Python', Validators.required),
    });

    this.feedbackForm = this._fb.group({
      feedback_instructions: new FormControl('', Validators.required),
    });
  }

  ngOnInit(): void {}

  generateCode() {
    this.isGenerateCode = true;
    this.disableGenerateCode = true;

    if (this.generateCodeSnippetForm.valid) {
      this._codeSnippetService
        .generateCodeSnippet(this.generateCodeSnippetForm.value)
        .subscribe({
          next: (response: any) => {
            this.code_language.set(
              this.generateCodeSnippetForm.value['code_language']
            );
            this.generated_code.set(response['code_snippet']);

            this.hiddenGenerateCode = true;
            this.hiddenFeedbackCode = false;
            this.isGenerateCode = false;
          },
        });
    }
  }

  executeCode() {
    this.isExecutingCode = true;
    this.disableExecuteCode = true;
    this.executed_result.set(null);

    this._codeSnippetService
      .codeExecution({
        generated_code: this.generated_code() ?? '',
        code_language: this.code_language() ?? '',
      })
      .subscribe({
        next: (response: any) => {
          this.executed_result.set(response['output']);

          this.isExecutingCode = false;
          this.disableExecuteCode = false;
        },
      });
  }

  feedbackCode() {
    const payload = {
      code_snippet: this.generated_code() ?? '',
      code_language: this.code_language() ?? '',
      feedback_instructions: this.feedbackForm.value['feedback_instructions'],
    };

    this.isGenerateCode = true;
    this.generated_code.set(null);
    this.executed_result.set(null);
    this.disableFeedbackCode = true;

    console.log(payload);
    this._codeSnippetService.feedbackCode(payload).subscribe({
      next: (response: any) => {
        this.generated_code.set(response['feedback_code_snippet']);

        this.isGenerateCode = false;
        this.disableFeedbackCode = false;
      },
    });
  }

  reset() {
    this.hiddenGenerateCode = false;
    this.hiddenFeedbackCode = true;
    this.disableGenerateCode = false;

    this.generated_code.set(null);
    this.code_language.set(null);
    this.executed_result.set(null);
    this.feedback_instructions.set(null);

    this.generateCodeSnippetForm.reset();
    this.feedbackForm.reset();
  }
}
