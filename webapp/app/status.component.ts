import {Component, OnDestroy, OnInit} from "@angular/core";
import {Http} from "@angular/http";
import {OperationResponse, ProgressResponse} from "./response.model";
import {TimingRequestService} from "./timing_request.service";
/**
 * Created by yuriel on 11/24/16.
 */

const DELAY_TIMEOUT = 1000;

class Task {
  constructor(public id: number,
              public name: String,
              public run: () => Promise<OperationResponse>) {}
}

@Component({
  moduleId: module.id,
  templateUrl: 'status.template.html'
})
export class StatusComponent implements OnInit, OnDestroy {
  constructor(private http: Http,
              private timingRequestService: TimingRequestService) {}

  logsTimerHandler: number;
  progressTimerHandler: number;
  statusTimerHandler: number;

  logs: string[] = [];
  progress: number;
  status: string;

  message: any = '';
  tasks = [
    new Task(0, "运行", () => {
      return this.http.get('/start')
        .toPromise()
        .then(response => {
          this.logs = [];
          return response.json() as OperationResponse
        })
    }),
    new Task(1, "停止", () => {
      return this.http.get('/stop')
        .toPromise()
        .then(response => response.json() as OperationResponse)
    }),
    new Task(2, "日志文件", () => {
      window.open('/log/files/', '_blank');
      return new Promise<OperationResponse>((resolve, reject) => {
        resolve(new OperationResponse());
      });
    })
  ];

  ngOnInit() {
    this.loadLogs();
    this.getStatus();
    this.getProgress();
  }

  ngOnDestroy() {
    clearTimeout(this.logsTimerHandler);
    clearTimeout(this.progressTimerHandler);
    clearTimeout(this.statusTimerHandler);
  }

  runTask(task: Task) {
    task.run().then(response => {
      this.message = response.msg;
      return response;
    }).catch(error => {
      this.message = error;
      return null;
    })
  }

  loadLogs() {
    this.timingRequestService.getLogs(this.logs.length).then(response => {
      let logs = response.log;
      this.logs = this.logs.concat(logs);
      this.logsTimerHandler = setTimeout(this.loadLogs.bind(this), DELAY_TIMEOUT);
    }).catch(err => {
      this.errorHandler('loadLogs', err);
    })
  }

  getProgress() {
    this.timingRequestService.getProgress().then(response => {
      this.progress = this.updateProgress(response);
      this.progressTimerHandler = setTimeout(this.getProgress.bind(this), DELAY_TIMEOUT);
    }).catch(err => {
      this.errorHandler('getProgress', err);
    })
  }

  updateProgress(response: ProgressResponse): number {
    console.log(response);
    if (response.total == 0 && response.progress < 0) return 0;
    if (response.total == 0 || response.sub_task_total == 0) return 0;
    let topProgress = response.progress / response.total;
    let subProgress = response.sub_task_progress / (response.sub_task_total * response.total);
    console.log(topProgress, subProgress);
    return topProgress + subProgress;
  }

  getStatus() {
    this.timingRequestService.getStatus().then(response => {
      this.status = response.msg;
      this.statusTimerHandler = setTimeout(this.getStatus.bind(this), DELAY_TIMEOUT);
    }).catch(err => {
      this.errorHandler('getStatus', err);
    })
  }

  errorHandler(name: String, err: any) {
    console.log('Error at request', name, err);
    this.message = err;
  }
}
