import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { ContentComponent } from './content.component';
import { MatTable, MatTableModule } from '@angular/material';

@NgModule({
  declarations: [
    ContentComponent
  ],
  imports: [
    BrowserModule,
    MatTableModule
  ],
  exports:[
    ContentComponent
  ],
  providers: [],
  bootstrap: [ContentComponent]
})
export class ContentModule { }
