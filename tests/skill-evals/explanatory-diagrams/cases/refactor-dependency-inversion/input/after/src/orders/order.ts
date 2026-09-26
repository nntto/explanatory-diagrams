export interface Address {
  name: string;
  postalCode: string;
  address: string;
  phone: string;
}

export interface OrderItem {
  productName: string;
  quantity: number;
  weightGrams: number;
}

export interface Order {
  id: string;
  status: "paid" | "shipped";
  customerEmail: string;
  shippingAddress: Address;
  items: OrderItem[];
  trackingNumber?: string;
}
