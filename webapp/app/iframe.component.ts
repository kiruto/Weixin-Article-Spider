/**
 * Created by yuriel on 11/30/16.
 */
import {Component, OnInit} from "@angular/core";
import {ActivatedRoute, Params} from "@angular/router";
import {DomSanitizer, SafeResourceUrl} from     "@angular/platform-browser";
@Component({
  moduleId: module.id,
  selector: 'inner-frame',
  templateUrl: 'iframe.template.html'
})
export class IFrameComponent implements OnInit {
  constructor(
    private route: ActivatedRoute,
    private santization: DomSanitizer
  ) {}

  ngOnInit() {
    let frame = document.getElementById('iframe') as HTMLIFrameElement;
    frame.setAttribute('src', this.getUrl());
    frame.onload = () => {
      this.onLoad(frame);
    }
  }

  onLoad(element: HTMLIFrameElement) {
    let imgs = element.contentDocument.getElementsByTagName('img');
    console.log(imgs);
    Array.prototype.forEach.call(imgs, (node: Element) => {
      let src = node.getAttribute('data-src');
      if (!src) return;
      let srcEncode = encodeURIComponent(src);
      node.setAttribute('src', '/proxy/image/' + srcEncode);
    });
    element.contentDocument.getElementById('sg_cmt_area').remove();
    element.style.height = element.contentWindow.document.body.scrollHeight + 'px';
  }

  getUrl() {
    let result: string = '';
    this.route.params.forEach(params => {
      result = "/.." + decodeURIComponent(params['url_encoded']);
    });
    console.log(result);
    return result;
  }

  getSafeUrl() {
    let result: any = null;
    this.route.params.forEach(params => {
      let url = "/.." + decodeURIComponent(params['url_encoded']);
      result = this.santization.bypassSecurityTrustUrl(url)
    });
    console.log(result);
    return result;
  }
}
