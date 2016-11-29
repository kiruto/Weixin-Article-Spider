import {Component, OnInit, OnDestroy} from "@angular/core";
import {Http} from "@angular/http";
import Timer = NodeJS.Timer;
/**
 * Created by yuriel on 11/24/16.
 */
@Component({
  moduleId: module.id,
  templateUrl: 'logs.template.html'
})
export class  LogsComponent {
  constructor(private http: Http) {}

}
