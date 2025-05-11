// next.config.mjs
import mdx from "@next/mdx";

const withMDX = mdx({ extension: /\.mdx?$/, options: {} });

/** @type {import('next').NextConfig} */
const nextConfig = {
  basePath: "/magic/portfolio",
  assetPrefix: "/magic/portfolio",
  trailingSlash: true,
  pageExtensions: ["ts", "tsx", "md", "mdx"],
  transpilePackages: ["next-mdx-remote"],
  sassOptions: {
    compiler: "modern",
    silenceDeprecations: ["legacy-js-api"],
  },
  images: {
    loader: "default",
    path: "/magic/portfolio/_next/image",  // ← путь к Image API
  },
};

export default withMDX(nextConfig);