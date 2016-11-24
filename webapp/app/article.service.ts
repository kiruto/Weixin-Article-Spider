/**
 * Created by yuriel on 11/23/16.
 */
import {Injectable, Inject} from "@angular/core";
import {Article} from "./articles.component";
import {Http} from "@angular/http";
import 'rxjs/add/operator/toPromise';
@Injectable()
export class ArticleService {
  constructor(@Inject(Http) private http: Http) {}
  getArticlesByCreatedDate(date: String): Promise<Article[]> {
    if (date == '') {
      let today = new Date();
      date = (today.getMonth() + 1) + "-" + today.getDate() + "-" + today.getFullYear();
    }
    return this.http.get('/rest/article/date/written/' + date)
      .toPromise()
      .then(response => response.json().articles as Article[])
      .catch(error => {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
      })
  }
  /*
  getArticlesByWrittenDate(date: String): Promise<Article[]> {
    return Promise.resolve(null);
  }
  */
}
