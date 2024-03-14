import { Routes } from '@angular/router';
import { CodeSnippetGeneratorComponent } from './components/code-snippet-generator/code-snippet-generator.component';

export const routes: Routes = [{
  path: '',component:CodeSnippetGeneratorComponent
},{
  path:'**',redirectTo:'/',pathMatch:"full"
}];
