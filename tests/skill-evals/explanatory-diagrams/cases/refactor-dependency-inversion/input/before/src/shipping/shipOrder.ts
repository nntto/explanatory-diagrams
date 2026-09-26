import { CarrierClient } from "@example/carrier-sdk";
import { MailClient } from "@example/mail-sdk";
import { StorageClient } from "@example/storage-sdk";
import type { Order } from "../orders/order";

const carrier = new CarrierClient({ apiKey: process.env.CARRIER_API_KEY ?? "" });
const storage = new StorageClient({ bucket: process.env.LABEL_BUCKET ?? "" });
const mail = new MailClient({ apiKey: process.env.MAIL_API_KEY ?? "" });

export interface Shipment {
  trackingNumber: string;
  labelKey: string;
}

export async function shipOrder(order: Order): Promise<Shipment> {
  const { trackingNumber, labelPdf } = await carrier.createShipment({
    recipient: order.shippingAddress,
    packages: [{ weightGrams: totalWeight(order) }],
  });

  const labelKey = `labels/${order.id}.pdf`;
  await storage.putObject(labelKey, labelPdf, { contentType: "application/pdf" });

  await mail.send({
    from: "shop@example.com",
    to: order.customerEmail,
    subject: `ご注文 ${order.id} を出荷しました`,
    text: `ご注文の商品を出荷しました。\nお問い合わせ番号：${trackingNumber}`,
  });

  return { trackingNumber, labelKey };
}

function totalWeight(order: Order): number {
  return order.items.reduce((sum, item) => sum + item.weightGrams * item.quantity, 0);
}
