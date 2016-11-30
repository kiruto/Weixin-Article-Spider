/**
 * Created by yuriel on 11/25/16.
 */
export class OperationResponse {
  flag: number;
  msg: string;
}

export class LogsResponse extends OperationResponse {
  log: string[];
}

export class ProgressResponse extends OperationResponse {
  total: number;
  progress: number;
  sub_task_total: number;
  sub_task_progress: number;

  public static isStop(progress: ProgressResponse): boolean {
    return progress.total == 0 && progress.progress == -1 &&
      progress.sub_task_total == 0 && progress.sub_task_progress == -1
  }
}

export class WXIDResponse extends OperationResponse {
  wxid_list: WXID[];
}

export class WXID {
  name: string;
  extra: WXIDExtra;
}

export class WXIDExtra {
  img: string;
  jieshao: string;
  name: string;
  post_perm: number;
  qrcode: string;
  red_count: number;
  renzhen: string;
  url: string;
  version: string;
  wechatid: string;
}

export class VcodeResponse extends OperationResponse {
  need_input: boolean;
  type: string;
}
