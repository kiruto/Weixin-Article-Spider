/**
 * Created by yuriel on 11/23/16.
 */
export class Tag {
  name: String;
  router: String;

  constructor (name: String = '', router: String = '') {
    this.name = name;
    this.router = router;
  }
}
