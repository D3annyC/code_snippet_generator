import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { DEV_API } from '../../config';
import { CodeExecute, CodeSnippet, Feedback } from '../interfaces/code-snippet';

@Injectable({
  providedIn: 'root',
})
export class CodeSnippetService {
  private _http: HttpClient = inject(HttpClient);

  generateCodeSnippet(client: CodeSnippet): Observable<CodeSnippet> {
    return this._http.post<CodeSnippet>(DEV_API + '/code_snippet', client);
  }

  codeExecution(client: CodeExecute): Observable<CodeExecute> {
    return this._http.post<CodeExecute>(DEV_API + '/execute_code', client);
  }

  feedbackCode(client: Feedback): Observable<Feedback> {
    return this._http.post<Feedback>(
      DEV_API + '/feedback_code_snippet',
      client
    );
  }
}
