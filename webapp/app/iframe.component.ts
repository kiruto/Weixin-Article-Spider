/**
 * Created by yuriel on 11/30/16.
 */
import {Component, OnInit} from "@angular/core";
import {ActivatedRoute, Params} from "@angular/router";
import {DomSanitizer, SafeResourceUrl} from "@angular/platform-browser";
import {getUrl} from "./config.constant";
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
    this.proxyImgs(element);
    this.removeScripts(element);
    this.removeOtherElements(element);
    element.style.height = element.contentWindow.document.body.scrollHeight + 'px';
  }

  proxyImgs(element: HTMLIFrameElement) {
    let imgs = element.contentDocument.getElementsByTagName('img');
    Array.prototype.forEach.call(imgs, (node: Element) => {
      let src = node.getAttribute('data-src');
      if (!src) {
        src = node.getAttribute('data-backsrc');
      }
      if (!src) {
        src = node.getAttribute('src');
        if (!src || !src.startsWith('http://mmbiz.qpic.cn')) return;
      }
      let srcEncode = encodeURIComponent(src);
      node.setAttribute('src', getUrl('/proxy/image/' + srcEncode));
    });
  }

  removeScripts(element: HTMLIFrameElement) {
    let scripts = element.contentDocument.getElementsByTagName('script');
    let i = scripts.length;
    while(i--) {
      scripts[i].parentNode.removeChild(scripts[i])
    }
  }

  removeOtherElements(element: HTMLIFrameElement) {
    element.contentDocument.getElementById('sg_cmt_area').remove();
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
