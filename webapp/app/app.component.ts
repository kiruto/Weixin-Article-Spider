import { Component } from '@angular/core';
import {Tag} from "./tag.model";

@Component({
  moduleId: module.id,
  selector: 'my-app',
  templateUrl: 'main_component.html'
})
export class AppComponent {
  title = '文章列表';
  tags = [
    new Tag('文章列表', 'articles'),
    new Tag('设置', 'settings'),
    new Tag('日志', 'logs'),
    new Tag('状态', 'status')
  ];
  selected = this.tags[0];

  onSelect(tag: Tag): void  {
    console.log('clicked:' + tag.name);
    this.selected = tag;
  }
}
