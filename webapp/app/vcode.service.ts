/**
 * Created by yuriel on 11/30/16.
 */
import {Injectable} from "@angular/core";
import {Http} from "@angular/http";
import {VcodeResponse, OperationResponse} from "./response.model";
@Injectable()
export class VCodeService {
  constructor(private http: Http) {}


  loadVcode(): Promise<VcodeResponse> {
    return this.http.get('/rest/vcode/status').toPromise().then(response => {
      return response.json() as VcodeResponse;
    })
  }

  resolveVcode(code: string, type: string = 'article_list'): Promise<OperationResponse> {
    return this.http.post('/rest/vcode/resolve', JSON.stringify({'vcode': code, 'type': type}))
      .toPromise().then(response => {
        return response.json() as OperationResponse;
      })
  }
}
