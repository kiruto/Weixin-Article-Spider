import {Routes, RouterModule} from "@angular/router";
import {ArticlesComponent} from "./articles.component";
import {NgModule} from "@angular/core";
/**
 * Created by yuriel on 11/23/16.
 */
const routes: Routes = [
  { path: 'articles', redirectTo: 'articles/created_at/', pathMatch: 'full'},
  { path: 'articles/created_at/:date', component: ArticlesComponent },
  { path: 'articles/written/:date', component: ArticlesComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
