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
        return response.json().articles as Article[]
      })
      .catch(onError)
  }
  getArticlesByWrittenDate(date: String, onError?: (err: any) => Promise<Article[]>): Promise<Article[]> {
    date = ArticleService.validDate(date);
    return this.http.get('/rest/article/date/written/' + date)
      .toPromise().then(response => {
        return response.json().articles as Article[];
      })
      .catch(onError);
  }

  getArticlesByAuthor(author: string): Promise<Article[]> {
    author = author.trim();
    return this.http.get('/rest/article/author/' + author)
      .toPromise()
      .then(response => {
        return response.json().articles as Article[];
      })
  }

  getCreatedDate(): Promise<string[]> {
    return this.http.get('/rest/date/create_at').toPromise().then(response => {
      let result = response.json();
      return result.date as string[];
    })
  }

  getWrittenDate(): Promise<string[]> {
    return this.http.get('/rest/date/written').toPromise().then(response => {
      let result = response.json();
      return result.date as string[];
    })
  }

  private static validDate(date: String) {
    if (date == '') {
      let today = new Date();
      return today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();
    }
    return date;
  }
}
