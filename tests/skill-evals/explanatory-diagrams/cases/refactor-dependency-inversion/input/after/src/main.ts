import { createServer } from "node:http";
import { CarrierClient } from "@example/carrier-sdk";
import { MailClient } from "@example/mail-sdk";
import { StorageClient } from "@example/storage-sdk";
import { CarrierSdkLabelIssuer } from "./infra/carrierSdkLabelIssuer";
import { MailSdkMailer } from "./infra/mailSdkMailer";
import { StorageSdkFileStorage } from "./infra/storageSdkFileStorage";
import { findOrder, markShipped } from "./orders/orderStore";
import { createShipOrder } from "./shipping/shipOrder";

const shipOrder = createShipOrder({
  labelIssuer: new CarrierSdkLabelIssuer(new CarrierClient({ apiKey: process.env.CARRIER_API_KEY ?? "" })),
  fileStorage: new StorageSdkFileStorage(new StorageClient({ bucket: process.env.LABEL_BUCKET ?? "" })),
  mailer: new MailSdkMailer(new MailClient({ apiKey: process.env.MAIL_API_KEY ?? "" })),
});

const server = createServer(async (req, res) => {
  const match = req.method === "POST" ? req.url?.match(/^\/orders\/([^/]+)\/ship$/) : undefined;
  if (!match) {
    res.writeHead(404).end();
    return;
  }

  try {
    const order = await findOrder(match[1]);
    if (!order) {
      res.writeHead(404).end();
      return;
    }
    const shipment = await shipOrder(order);
    await markShipped(order.id, shipment.trackingNumber);
    res.writeHead(200, { "content-type": "application/json" }).end(JSON.stringify(shipment));
  } catch (error) {
    console.error(error);
    res.writeHead(500).end();
  }
});

server.listen(Number(process.env.PORT ?? 3000));
