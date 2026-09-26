import type { Address } from "../orders/order";

// 出荷の処理が外に頼むこと。SDK を使う実装は src/infra/ にある。

export interface LabelRequest {
  recipient: Address;
  weightGrams: number;
}

export interface Label {
  trackingNumber: string;
  pdf: Uint8Array;
}

/** 配送業者に送り状を発行してもらう */
export interface LabelIssuer {
  issue(request: LabelRequest): Promise<Label>;
}

/** ファイルを保存する */
export interface FileStorage {
  save(key: string, body: Uint8Array, contentType: string): Promise<void>;
}

export interface Mail {
  from: string;
  to: string;
  subject: string;
  text: string;
}

/** メールを送る */
export interface Mailer {
  send(mail: Mail): Promise<void>;
}
