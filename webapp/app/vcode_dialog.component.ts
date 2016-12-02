/**
 * Created by yuriel on 11/30/16.
 */
import {Component, OnInit, Input} from "@angular/core";
import {VCodeService} from "./vcode.service";
import {MDLDialog} from "./mdl-components";
@Component({
  moduleId: module.id,
  selector: 'vcode-dialog',
  templateUrl: 'vcode_dialog.html'
})
export class VCodeDialogComponent implements OnInit {

  @Input() inputValue: string = '';
  type: string = '';
  dialog = document.querySelector('#vcode_dialog') as MDLDialog;
  vcodeImgSrc = '';

  constructor(private vcodeService: VCodeService) {}

  ngOnInit() {
    this.requestVCodeStatus()
  }

  requestVCodeStatus() {
    this.vcodeService.loadVcode().then(response => {
      if(response.need_input) {
        this.type = response.type;
        this.vcodeImgSrc = '/vcode/img?v=' + Math.random();
        this.showInputDialog();
      }
      setTimeout(this.requestVCodeStatus.bind(this), 1000);
    }).catch(err => {
      console.log(err)
    })
  }

  showInputDialog() {
    this.dialog.showModal()
  }

  submit() {
    this.vcodeService.resolveVcode(this.inputValue, this.type).catch(err => {
      console.log(err);
    });
    this.dialog.close()
  }
}
