import { beforeEach, describe, expect, it, vi } from "vitest";
import type { Order } from "../orders/order";
import { shipOrder } from "./shipOrder";

const sdk = vi.hoisted(() => ({
  createShipment: vi.fn(),
  putObject: vi.fn(),
  send: vi.fn(),
}));

vi.mock("@example/carrier-sdk", () => ({
  CarrierClient: class {
    createShipment = sdk.createShipment;
  },
}));
vi.mock("@example/storage-sdk", () => ({
  StorageClient: class {
    putObject = sdk.putObject;
  },
}));
vi.mock("@example/mail-sdk", () => ({
  MailClient: class {
    send = sdk.send;
  },
}));

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

beforeEach(() => {
  vi.clearAllMocks();
  sdk.createShipment.mockResolvedValue({
    trackingNumber: "1234-5678-9012",
    labelPdf: new Uint8Array([1, 2, 3]),
  });
});

describe("shipOrder", () => {
  it("送り状を発行し、PDF を保存して、購入者にメールを送る", async () => {
    const shipment = await shipOrder(order);

    expect(shipment).toEqual({ trackingNumber: "1234-5678-9012", labelKey: "labels/A-1001.pdf" });
    expect(sdk.createShipment).toHaveBeenCalledWith({
      recipient: order.shippingAddress,
      packages: [{ weightGrams: 900 }],
    });
    expect(sdk.putObject).toHaveBeenCalledWith("labels/A-1001.pdf", new Uint8Array([1, 2, 3]), {
      contentType: "application/pdf",
    });
    expect(sdk.send).toHaveBeenCalledWith({
      from: "shop@example.com",
      to: "hanako@example.com",
      subject: "ご注文 A-1001 を出荷しました",
      text: "ご注文の商品を出荷しました。\nお問い合わせ番号：1234-5678-9012",
    });
  });

  it("送り状の発行に失敗したら、保存もメールもしない", async () => {
    sdk.createShipment.mockRejectedValue(new Error("carrier unavailable"));

    await expect(shipOrder(order)).rejects.toThrow("carrier unavailable");
    expect(sdk.putObject).not.toHaveBeenCalled();
    expect(sdk.send).not.toHaveBeenCalled();
  });
});
