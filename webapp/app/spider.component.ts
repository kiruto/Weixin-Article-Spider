/**
 * Created by yuriel on 11/23/16.
 */
import {Component, OnInit} from "@angular/core";
import {ArticleService} from "./article.service";
@Component({
  selector: 'spider',
  templateUrl: 'app/spider.template.html',
})
export class SpiderComponent implements OnInit {

  constructor(private articleService: ArticleService) {  }
  ngOnInit(): void {

  }
}
