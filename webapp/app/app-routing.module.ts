import {Routes, RouterModule} from "@angular/router";
import {ArticlesComponent} from "./articles.component";
import {NgModule} from "@angular/core";
import {StatusComponent} from "./status.component";
import {SettingsComponent} from "./settings.component";
import {LogsComponent} from "./logs.component";
import {IFrameComponent} from "./iframe.component";
import {HOME_PATH, TODAY_STRING} from "./config.constant";
/**
 * Created by yuriel on 11/23/16.
 */

const routes: Routes = [
  { path: '', redirectTo: HOME_PATH, pathMatch: 'full' },
  { path: '*', redirectTo: HOME_PATH },
  { path: '**', redirectTo: HOME_PATH },
  { path: 'articles', children: [
    { path: '', redirectTo: 'created_at', pathMatch: 'full' },
    { path: 'created_at', children: [
      { path: '', pathMatch: 'full', redirectTo: TODAY_STRING },
      { path: ':date', component: ArticlesComponent }
    ]},
    { path: 'written', children: [
      { path: '', pathMatch: 'full', redirectTo: TODAY_STRING },
      { path: ':date', component: ArticlesComponent }
    ] },
    { path: 'author/:author', component: ArticlesComponent }
  ]},
  { path: 'settings', component: SettingsComponent },
  { path: 'logs', component: LogsComponent },
  { path: 'status', component: StatusComponent },
  { path: 'proxy', children: [
    { path: ':url_encoded', component: IFrameComponent },
    { path: '', redirectTo: HOME_PATH, pathMatch: 'full' }
  ] }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
