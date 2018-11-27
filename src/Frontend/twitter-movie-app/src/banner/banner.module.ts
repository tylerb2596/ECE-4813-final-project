import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { BannerComponent } from './banner.component';

@NgModule({
  declarations: [
    BannerComponent
  ],
  imports: [
    BrowserModule,
  ],
  exports:[
    BannerComponent
  ],
  providers: [],
  bootstrap: [BannerComponent]
})
export class BannerModule { }
