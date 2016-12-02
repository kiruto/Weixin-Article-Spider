/**
 * Created by yuriel on 11/30/16.
 */
import {Component, OnInit} from "@angular/core";
import {ActivatedRoute, Params} from "@angular/router";
import {DomSanitizer, SafeResourceUrl} from "@angular/platform-browser";
import { Location } from '@angular/common';
import {getUrl} from "./config.constant";
import {ArticleViewerService} from "./article-viewer.service";
@Component({
  moduleId: module.id,
  selector: 'inner-frame',
  templateUrl: 'iframe.template.html'
})
export class IFrameComponent implements OnInit {
  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private santization: DomSanitizer,
    private articleViewerService: ArticleViewerService
  ) {}

  ngOnInit() {
    if (this.location.path().includes('proxy')) {
      this.setUrl(this.getUrl())
    } else {
      this.articleViewerService.url.subscribe((url: string) => {
        if ('' != url.trim()) {
          this.setUrl(decodeURIComponent(url));
        }
      })
    }
  }

  setUrl(url: string) {
    let frame = document.getElementById('iframe') as HTMLIFrameElement;
    frame.src = url;
    frame.onload = () => {
      frame.style.height = '100%';
      this.onLoad(frame);
    }
  }

  private onLoad(element: HTMLIFrameElement) {
    this.proxyImgs(element);
    this.removeScripts(element);
    this.removeOtherElements(element);
    element.style.height = element.contentWindow.document.body.scrollHeight + 'px';
  }

  private proxyImgs(element: HTMLIFrameElement) {
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

  private removeScripts(element: HTMLIFrameElement) {
    let scripts = element.contentDocument.getElementsByTagName('script');
    let i = scripts.length;
    while(i--) {
      scripts[i].parentNode.removeChild(scripts[i])
    }
  }

  private removeOtherElements(element: HTMLIFrameElement) {
    element.contentDocument.getElementById('sg_cmt_area').remove();
  }

  private getUrl() {
    let result: string = '';
    this.route.params.forEach(params => {
      result = "/.." + decodeURIComponent(params['url_encoded']);
    });
    console.log(result);
    return result;
  }

  private getSafeUrl() {
    let result: any = null;
    this.route.params.forEach(params => {
      let url = "/.." + decodeURIComponent(params['url_encoded']);
      result = this.santization.bypassSecurityTrustUrl(url)
    });
    console.log(result);
    return result;
  }
}
