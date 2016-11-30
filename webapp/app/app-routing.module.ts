import {Routes, RouterModule} from "@angular/router";
import {ArticlesComponent} from "./articles.component";
import {NgModule} from "@angular/core";
import {StatusComponent} from "./status.component";
import {SettingsComponent} from "./settings.component";
import {LogsComponent} from "./logs.component";
/**
 * Created by yuriel on 11/23/16.
 */
let today = new Date();
let todayString: String = today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();
const routes: Routes = [
  { path: '', redirectTo: 'articles', pathMatch: 'full'},
  { path: 'articles', redirectTo: 'articles/created_at/' + todayString, pathMatch: 'full'},
  { path: 'articles/created_at/:date', component: ArticlesComponent },
  { path: 'articles/written/:date', component: ArticlesComponent },
  { path: 'articles/author/:author', component: ArticlesComponent },
  { path: 'settings', component: SettingsComponent },
  { path: 'logs', component: LogsComponent },
  { path: 'status', component: StatusComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
