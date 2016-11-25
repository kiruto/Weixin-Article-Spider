import './rxjs-extensions';

import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { HttpModule } from '@angular/http';
import { AppComponent }  from './app.component';
import { ArticlesComponent } from './articles.component';
import { SpiderComponent } from './spider.component';
import {FormsModule} from "@angular/forms";
import {ArticleService} from "./article.service";
import {AppRoutingModule} from "./app-routing.module";
import {SettingsComponent} from "./settings.component";
import {LogsComponent} from "./logs.component";
import {StatusComponent} from "./status.component";
import {TimingRequestService} from "./timing_request.service";


@NgModule({
  imports:      [ BrowserModule, FormsModule, AppRoutingModule, HttpModule ],
  declarations: [
    AppComponent,
    ArticlesComponent,
    SpiderComponent,
    SettingsComponent,
    LogsComponent,
    StatusComponent
  ],
  providers:    [ ArticleService, TimingRequestService ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
