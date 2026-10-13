import handler from "vinext/server/fetch-handler";
import official from "../data/hosted-official-media.json";
import catalog from "../data/hosting-assets.json";
import { createMediaHandler } from "./media-proxy.mjs";

const media = createMediaHandler([
  { prefix: "/official-drafts/", base: official.base_url, assets: official.assets },
  { prefix: "/", base: catalog.image_base_url, assets: catalog.assets },
]);

export default {
  async fetch(request: Request, env: { ASSETS?: Fetcher }, ctx: ExecutionContext) {
    const response = await media(request);
    if (response) return response;
    if (env.ASSETS) {
      const asset = await env.ASSETS.fetch(request);
      if (asset.status !== 404) return asset;
    }
    return handler.fetch(request, env, ctx);
  },
};
