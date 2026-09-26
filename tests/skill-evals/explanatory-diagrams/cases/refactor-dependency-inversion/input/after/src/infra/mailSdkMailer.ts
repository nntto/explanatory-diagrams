import type { MailClient } from "@example/mail-sdk";
import type { Mail, Mailer } from "../shipping/ports";

export class MailSdkMailer implements Mailer {
  constructor(private readonly client: MailClient) {}

  async send(mail: Mail): Promise<void> {
    await this.client.send(mail);
  }
}
