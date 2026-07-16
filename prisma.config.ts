import "dotenv/config";
import { defineConfig } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: {
    path: "prisma/migrations",
  },
  // Connection URL for Migrate CLI (deploy). Read directly so offline commands
  // (generate/diff, Docker build) don't fail when DATABASE_URL is unset.
  // Runtime connections use the adapter in src/lib/prisma.ts.
  datasource: {
    url: process.env.DATABASE_URL,
  },
});
