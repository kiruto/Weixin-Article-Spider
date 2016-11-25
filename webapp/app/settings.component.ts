import {Component, OnInit, Input} from "@angular/core";
import {TimingRequestService} from "./timing_request.service";
import {WXID} from "./response.model";
/**
 * Created by yuriel on 11/24/16.
 */
@Component({
  moduleId: module.id,
  templateUrl: 'settings.template.html'
})
export class SettingsComponent implements OnInit {
  @Input() wxidList: WXID[] = [];
  @Input() inputValue: string = '';
  message: string;

  constructor(private timingRequestService: TimingRequestService) {}

  ngOnInit() {
    this.updateList();
  }

  updateList() {
    this.timingRequestService.getWXID().then(response => {
      this.wxidList = response.wxid_list;
    }).catch(error => {
      this.errorHandler('getWXID', error);
    })
  }

  addWXID() {
    let list = this.inputValue.trim().split('\n');
    this.timingRequestService.batchWXID(list).then(response => {
      this.message = response.msg;
      this.updateList();
      this.inputValue = '';
    }).catch(err => {
      this.message = err;
    });
  }

  remove(wx: WXID) {
    this.timingRequestService.removeWXID(wx.name).then(response => {
      this.message = response.msg;
      this.updateList();
    }).catch(err => {
      this.message = err;
    })
  }

  errorHandler(name: String, err: any) {
    console.log(name, err);
    this.message = err;
  }
}
