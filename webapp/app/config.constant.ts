import {formatDate} from "./utils";
/**
 * Created by yuriel on 12/1/16.
 */
export const HOST = window.location.host;

export const TODAY_STRING: string = formatDate();
export const HOME_PATH = 'articles/create_at/' + TODAY_STRING;

export function getUrl(url: string): string {
  if (url.startsWith('/')) {
    return '//' + HOST + url
  } else {
    return '//' + HOST + '/' + url
  }
}
