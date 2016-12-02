/**
 * Created by yuriel on 12/2/16.
 */
import {Injectable, EventEmitter} from "@angular/core";
@Injectable()
export class ArticleViewerService {
  url = new EventEmitter<string>();
}
