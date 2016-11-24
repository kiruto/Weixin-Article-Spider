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
  getArticlesByCreatedDate(date: String, onError?: (err: any) => Promise<Article[]>): Promise<Article[]> {
    date = ArticleService.validDate(date);
    return this.http.get('/rest/article/date/create_at/' + date)
      .toPromise()
      .then(response => {
        console.log(response);
        console.log(response.json());
        return response.json().articles as Article[]
      })
      .catch(onError)
  }
  getArticlesByWrittenDate(date: String, onError?: (err: any) => Promise<Article[]>): Promise<Article[]> {
    date = ArticleService.validDate(date);
    return this.http.get('/rest/article/date/written/' + date)
      .toPromise().then(response => {
        console.log(response);
        return response.json();
      })
      .catch(onError);
  }

  private static validDate(date: String) {
    if (date == '') {
      let today = new Date();
      return today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();
    }
    return date;
  }
}
