import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CodeSnippetGeneratorComponent } from './code-snippet-generator.component';

describe('CodeSnippetGeneratorComponent', () => {
  let component: CodeSnippetGeneratorComponent;
  let fixture: ComponentFixture<CodeSnippetGeneratorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CodeSnippetGeneratorComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CodeSnippetGeneratorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
