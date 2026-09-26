import { describe, expect, it } from "vitest";
import type { Order } from "../orders/order";
import type { FileStorage, LabelIssuer, LabelRequest, Mail, Mailer } from "./ports";
import { createShipOrder } from "./shipOrder";

const order: Order = {
  id: "A-1001",
  status: "paid",
  customerEmail: "hanako@example.com",
  shippingAddress: {
    name: "山田 花子",
    postalCode: "164-0001",
    address: "東京都中野区中野 0-0-0",
    phone: "090-0000-0000",
  },
  items: [
    { productName: "マグカップ", quantity: 2, weightGrams: 350 },
    { productName: "コースター", quantity: 1, weightGrams: 200 },
  ],
};

function setup(
  issue: LabelIssuer["issue"] = async () => ({
    trackingNumber: "1234-5678-9012",
    pdf: new Uint8Array([1, 2, 3]),
  }),
) {
  const labelRequests: LabelRequest[] = [];
  const savedFiles: { key: string; body: Uint8Array; contentType: string }[] = [];
  const sentMails: Mail[] = [];

  const labelIssuer: LabelIssuer = {
    issue: (request) => {
      labelRequests.push(request);
      return issue(request);
    },
  };
  const fileStorage: FileStorage = {
    save: async (key, body, contentType) => {
      savedFiles.push({ key, body, contentType });
    },
  };
  const mailer: Mailer = {
    send: async (mail) => {
      sentMails.push(mail);
    },
  };

  const shipOrder = createShipOrder({ labelIssuer, fileStorage, mailer });
  return { shipOrder, labelRequests, savedFiles, sentMails };
}

describe("shipOrder", () => {
  it("送り状を発行し、PDF を保存して、購入者にメールを送る", async () => {
    const { shipOrder, labelRequests, savedFiles, sentMails } = setup();

    const shipment = await shipOrder(order);

    expect(shipment).toEqual({ trackingNumber: "1234-5678-9012", labelKey: "labels/A-1001.pdf" });
    expect(labelRequests).toEqual([{ recipient: order.shippingAddress, weightGrams: 900 }]);
    expect(savedFiles).toEqual([
      { key: "labels/A-1001.pdf", body: new Uint8Array([1, 2, 3]), contentType: "application/pdf" },
    ]);
    expect(sentMails).toEqual([
      {
        from: "shop@example.com",
        to: "hanako@example.com",
        subject: "ご注文 A-1001 を出荷しました",
        text: "ご注文の商品を出荷しました。\nお問い合わせ番号：1234-5678-9012",
      },
    ]);
  });

  it("送り状の発行に失敗したら、保存もメールもしない", async () => {
    const { shipOrder, savedFiles, sentMails } = setup(async () => {
      throw new Error("carrier unavailable");
    });

    await expect(shipOrder(order)).rejects.toThrow("carrier unavailable");
    expect(savedFiles).toEqual([]);
    expect(sentMails).toEqual([]);
  });
});
