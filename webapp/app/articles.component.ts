/**
 * Created by yuriel on 11/23/16.
 */
import {Component, OnInit, Inject} from "@angular/core";
import {ArticleService} from "./article.service";
import {ActivatedRoute, Params, Router} from "@angular/router";
import { Location } from '@angular/common';

export class Article {
  hash_id: String;
  title: String;
  info: String;
  version: String;
  content: string;
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
  create_at: string[] = [];
  written: string[] = [];

  constructor(
    private router: Router,
    @Inject(ArticleService) private articleService: ArticleService,
    @Inject(ActivatedRoute) private route: ActivatedRoute,
    @Inject(Location) private location: Location
  ) {}

  ngOnInit(): void {
    //console.log(this.location.path());
    let path = this.location.path();
    this.route.params
      .switchMap((params: Params) => {
        if (path.includes('created_at'))
          return this.articleService.getArticlesByCreatedDate(params['date']);
        else if (path.includes('written'))
          return this.articleService.getArticlesByWrittenDate(params['date']);
        else if (path.includes('author'))
          return this.articleService.getArticlesByAuthor(params['author'])
      })
      .subscribe(articles => {
        this.articles = articles as Article[];
        return null;
      });
    this.articleService.getCreatedDate().then(date => {
      this.create_at = date;
    }).catch(err => {
      console.log(err)
    });
    this.articleService.getWrittenDate().then(date => {
      this.written = date;
    }).catch(err => {
      console.log(err);
    })
  }

  viewArticle(article: Article) {
    this.router.navigate(['proxy/', this.getProxyUrlByPath(article.content)]);
  }

  getProxyUrlByPath(path: string) {
    let encode_url = encodeURIComponent('/cache/html/' + path);
    return encode_url;
  }
}
