import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import {Tag} from "./tag.model";
import { Location } from '@angular/common';
import {Router} from "@angular/router";
import {HOME_PATH} from "./config.constant";

@Component({
  moduleId: module.id,
  selector: 'my-app',
  templateUrl: 'app.template.html'
})
export class AppComponent implements OnInit {
  title = 'Weixin Spider Article Viewer';
  tags = [
    new Tag('文章列表', 'articles'),
    new Tag('订阅公众号', 'settings'),
    new Tag('更新日志', 'logs'),
    new Tag('状态', 'status')
  ];
  selected = this.tags[0];

  constructor(private router: Router,
              private location: Location) { }

  ngOnInit() {
    if ('' == this.location.path()) {
      this.router.navigate([HOME_PATH]);
      this.router.navigateByUrl(HOME_PATH);
    }
  }

  onSelect(tag: Tag): void  {
    console.log('clicked:' + tag.name);
    this.selected = tag;
  }
}
