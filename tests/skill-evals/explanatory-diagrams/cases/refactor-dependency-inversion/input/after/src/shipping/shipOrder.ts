import type { Order } from "../orders/order";
import type { FileStorage, LabelIssuer, Mailer } from "./ports";

export interface Shipment {
  trackingNumber: string;
  labelKey: string;
}

export interface ShipOrderDeps {
  labelIssuer: LabelIssuer;
  fileStorage: FileStorage;
  mailer: Mailer;
}

export function createShipOrder({ labelIssuer, fileStorage, mailer }: ShipOrderDeps) {
  return async function shipOrder(order: Order): Promise<Shipment> {
    const { trackingNumber, pdf } = await labelIssuer.issue({
      recipient: order.shippingAddress,
      weightGrams: totalWeight(order),
    });

    const labelKey = `labels/${order.id}.pdf`;
    await fileStorage.save(labelKey, pdf, "application/pdf");

    await mailer.send({
      from: "shop@example.com",
      to: order.customerEmail,
      subject: `ご注文 ${order.id} を出荷しました`,
      text: `ご注文の商品を出荷しました。\nお問い合わせ番号：${trackingNumber}`,
    });

    return { trackingNumber, labelKey };
  };
}

function totalWeight(order: Order): number {
  return order.items.reduce((sum, item) => sum + item.weightGrams * item.quantity, 0);
}
