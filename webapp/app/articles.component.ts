/**
 * Created by yuriel on 11/23/16.
 */
import {Component, OnInit, Inject} from "@angular/core";
import {ArticleService} from "./article.service";
import {ActivatedRoute, Params} from "@angular/router";
import { Location } from '@angular/common';

export class Article {
  hash_id: String;
  title: String;
  info: String;
  version: String;
  content: String;
  created_at: String;
  date_time: String;
  extra: ArticleExtra;
}

export class ArticleExtra {
  author: String;
  content_url: String;
  copyright_stat: number;
  cover: String;
  datetime: number;
  digest: String;
  fileid: number;
  main: number;
  qunfa_id: number;
  source_url: String;
  title: String;
  type: String;
}

@Component({
  selector: 'article-list',
  templateUrl: 'app/articles.template.html'
})
export class ArticlesComponent implements OnInit {
  articles: Article[];
  selected_article: Article;
  constructor(
    @Inject(ArticleService) private articleService: ArticleService,
    @Inject(ActivatedRoute) private route: ActivatedRoute,
    @Inject(Location) private location: Location
  ) {}
  ngOnInit(): void {
    this.route.params
      .switchMap((params: Params) => {
        return this.articleService.getArticlesByCreatedDate(params['date'])
      })
      .subscribe(articles => {
        console.log(articles);
        this.articles = articles as Article[];
        return null;
      });
  }
}
