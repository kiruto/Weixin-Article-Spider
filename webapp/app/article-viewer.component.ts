/**
 * Created by yuriel on 12/2/16.
 */
import {Component, Input, OnChanges, SimpleChange, OnInit} from "@angular/core";
import {ArticleViewerService} from "./article-viewer.service";
@Component({
  moduleId: module.id,
  selector: 'article-viewer',
  templateUrl: 'article-viewer.template.html'
})
export class ArticleViewerComponent implements OnInit {

  hide: boolean = true;

  constructor(private articleViewerService: ArticleViewerService) {}

  ngOnInit() {
    this.articleViewerService.url.subscribe((url: string) => {
      if (url && '' != url.trim()) {
        this.hide = false;
      }
    })
  }

  close() {
    this.hide = true;
  }
}
