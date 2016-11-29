import {Directive, AfterViewChecked} from "@angular/core";
/**
 * Created by yuriel on 11/29/16.
 */
declare var componentHandler: any;

@Directive({
  selector: '[mdl]'
})
export class MDL implements AfterViewChecked {
  ngAfterViewChecked() {
    if (componentHandler) {
      componentHandler.upgradeAllRegistered();
    }
  }
}
