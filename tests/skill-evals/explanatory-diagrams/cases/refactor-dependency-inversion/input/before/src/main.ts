import { createServer } from "node:http";
import { findOrder, markShipped } from "./orders/orderStore";
import { shipOrder } from "./shipping/shipOrder";

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
