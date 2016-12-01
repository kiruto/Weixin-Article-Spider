import {formatDate} from "./utils";
/**
 * Created by yuriel on 12/1/16.
 */
export const HOST = '127.0.0.1';
export const PORT = '6303';

export const TODAY_STRING: string = formatDate();
export const HOME_PATH = 'articles/create_at/' + TODAY_STRING;

export function getUrl(url: string): string {
  if (url.startsWith('/')) {
    return 'http://' + HOST + ':' + PORT + url
  } else {
    return 'http://' + HOST + ':' + PORT + '/' + url
  }
}
