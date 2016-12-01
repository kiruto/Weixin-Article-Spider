/**
 * Created by yuriel on 12/1/16.
 */
export function formatDate(date: Date=new Date()): string {
  let mm = date.getMonth() + 1;
  let dd = date.getDate();

  return [date.getFullYear(),
    (mm>9 ? '' : '0') + mm,
    (dd>9 ? '' : '0') + dd
  ].join('-');
}
