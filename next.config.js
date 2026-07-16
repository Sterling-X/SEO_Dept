/** @type {import('next').NextConfig} */
const nextConfig = {
  // Produces a minimal self-contained server build for the Docker/Cloud Run image.
  output: "standalone",
  experimental: {
    serverComponentsExternalPackages: ["@prisma/client", "prisma"],
  },
}

module.exports = nextConfig
