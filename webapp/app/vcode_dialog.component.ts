/**
 * Created by yuriel on 11/30/16.
 */
import {Component, OnInit, Input, AfterContentInit} from "@angular/core";
import {VCodeService} from "./vcode.service";
import {MDLDialog} from "./mdl-components";
@Component({
  moduleId: module.id,
  selector: 'vcode-dialog',
  templateUrl: 'vcode_dialog.html'
})
export class VCodeDialogComponent implements AfterContentInit {

  @Input() inputValue: string = '';
  type: string = '';
  vcodeImgSrc = '';

  constructor(private vcodeService: VCodeService) {}

  ngAfterContentInit() {
    this.requestVCodeStatus()
  }

  requestVCodeStatus() {
    this.vcodeService.loadVcode().then(response => {
      if(response.need_input) {
        this.type = response.type;
        this.vcodeImgSrc = '/vcode/img/?v=' + Math.random();
        this.showInputDialog();
      }
      setTimeout(this.requestVCodeStatus.bind(this), 1000);
    }).catch(err => {
      console.log(err)
    })
  }

  getDialog(): MDLDialog {
    return document.querySelector('#vcode_dialog') as MDLDialog;
  }

  showInputDialog() {
    this.getDialog().showModal()
  }

  submit() {
    this.vcodeService.resolveVcode(this.inputValue, this.type).catch(err => {
      console.log(err);
    });
    this.getDialog().close()
  }
}
