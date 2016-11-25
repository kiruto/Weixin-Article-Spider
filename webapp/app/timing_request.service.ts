/**
 * Created by yuriel on 11/25/16.
 */
import {Injectable} from "@angular/core";
import {Http} from "@angular/http";
import {ProgressResponse, LogsResponse, OperationResponse, WXIDResponse} from "./response.model";
@Injectable()
export class TimingRequestService {
  constructor(private http: Http) {}

  getLogs(start: number): Promise<LogsResponse> {
    return this.http.get('/rest/log/' + start)
      .toPromise()
      .then(response => {
        return response.json() as LogsResponse;
      });
  }

  getProgress(): Promise<ProgressResponse> {
    return this.http.get('/rest/progress')
      .toPromise()
      .then(response => {
        return response.json() as ProgressResponse;
      })
  }

  getStatus(): Promise<OperationResponse> {
    return this.http.get('/rest/status')
      .toPromise()
      .then(response => {
        return response.json() as OperationResponse;
      })
  }

  getWXID(): Promise<WXIDResponse> {
    return this.http.get('/rest/wxid/list')
      .toPromise()
      .then(response => {
        return response.json() as WXIDResponse;
      })
  }

  batchWXID(data: string[]): Promise<OperationResponse> {
    return this.http.post('/rest/wxid/batch/', JSON.stringify(data))
      .toPromise()
      .then(response => {
        return response.json() as OperationResponse;
      })
  }

  removeWXID(id: String): Promise<OperationResponse> {
    return this.http.get('/rest/exid/remove/' + id)
      .toPromise()
      .then(response => {
        return response.json() as OperationResponse;
      })
  }
}
