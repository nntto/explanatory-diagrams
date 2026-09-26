// 使っている SDK は型定義を同梱していないので、使う分だけここで宣言する。

declare module "@example/carrier-sdk" {
  export interface Recipient {
    name: string;
    postalCode: string;
    address: string;
    phone: string;
  }

  export interface CreateShipmentRequest {
    recipient: Recipient;
    packages: { weightGrams: number }[];
  }

  export interface CreateShipmentResponse {
    trackingNumber: string;
    labelPdf: Uint8Array;
  }

  export class CarrierClient {
    constructor(options: { apiKey: string });
    createShipment(request: CreateShipmentRequest): Promise<CreateShipmentResponse>;
  }
}

declare module "@example/storage-sdk" {
  export class StorageClient {
    constructor(options: { bucket: string });
    putObject(key: string, body: Uint8Array, options?: { contentType?: string }): Promise<void>;
  }
}

declare module "@example/mail-sdk" {
  export interface MailMessage {
    from: string;
    to: string;
    subject: string;
    text: string;
  }

  export class MailClient {
    constructor(options: { apiKey: string });
    send(message: MailMessage): Promise<{ messageId: string }>;
  }
}

declare module "@example/db-sdk" {
  export interface Collection<T> {
    findOne(filter: Partial<T>): Promise<T | null>;
    updateOne(filter: Partial<T>, update: Partial<T>): Promise<void>;
  }

  export class DbClient {
    constructor(options: { url: string });
    collection<T>(name: string): Collection<T>;
  }
}
