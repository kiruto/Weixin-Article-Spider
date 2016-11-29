import { Component } from '@angular/core';
import {Tag} from "./tag.model";

@Component({
  moduleId: module.id,
  selector: 'my-app',
  templateUrl: 'app.template.html'
})
export class AppComponent {
  title = 'Weixin Spider Article Viewer';
  tags = [
    new Tag('文章列表', 'articles'),
    new Tag('订阅公众号', 'settings'),
    new Tag('更新日志', 'logs'),
    new Tag('状态', 'status')
  ];
  selected = this.tags[0];

  onSelect(tag: Tag): void  {
    console.log('clicked:' + tag.name);
    this.selected = tag;
  }
}
