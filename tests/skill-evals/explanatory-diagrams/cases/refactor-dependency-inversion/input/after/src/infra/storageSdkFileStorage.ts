import type { StorageClient } from "@example/storage-sdk";
import type { FileStorage } from "../shipping/ports";

export class StorageSdkFileStorage implements FileStorage {
  constructor(private readonly client: StorageClient) {}

  async save(key: string, body: Uint8Array, contentType: string): Promise<void> {
    await this.client.putObject(key, body, { contentType });
  }
}
