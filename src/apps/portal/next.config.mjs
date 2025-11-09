import { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

// Force Turbopack to treat the portal app directory as the workspace root
const appDir = dirname(fileURLToPath(import.meta.url));

/** @type {import('next').NextConfig} */
const nextConfig = {
  turbopack: {
    root: appDir,
  },
};

export default nextConfig;
