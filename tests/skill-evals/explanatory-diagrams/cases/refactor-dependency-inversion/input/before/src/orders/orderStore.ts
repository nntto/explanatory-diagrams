import { DbClient } from "@example/db-sdk";
import type { Order } from "./order";

const orders = new DbClient({ url: process.env.DATABASE_URL ?? "" }).collection<Order>("orders");

export function findOrder(id: string): Promise<Order | null> {
  return orders.findOne({ id });
}

export async function markShipped(id: string, trackingNumber: string): Promise<void> {
  await orders.updateOne({ id }, { status: "shipped", trackingNumber });
}
