import type { CarrierClient } from "@example/carrier-sdk";
import type { Label, LabelIssuer, LabelRequest } from "../shipping/ports";

export class CarrierSdkLabelIssuer implements LabelIssuer {
  constructor(private readonly client: CarrierClient) {}

  async issue({ recipient, weightGrams }: LabelRequest): Promise<Label> {
    const { trackingNumber, labelPdf } = await this.client.createShipment({
      recipient,
      packages: [{ weightGrams }],
    });
    return { trackingNumber, pdf: labelPdf };
  }
}
