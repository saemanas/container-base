import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

import js from "@eslint/js";
import globals from "globals";
import nextPlugin from "@next/eslint-plugin-next";
import tseslint from "typescript-eslint";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const portalNextConfig = nextPlugin.configs["core-web-vitals"];

export default tseslint.config(
  {
    ignores: [
      "**/node_modules/**",
      "**/.next/**",
      "**/dist/**",
      "**/build/**",
      "**/coverage/**",
      "**/*.tsbuildinfo",
      "**/.turbo/**",
    ],
  },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    ...portalNextConfig,
    files: ["src/apps/portal/**/*.{js,jsx,ts,tsx}", "eslint.config.mjs"],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        projectService: true,
        tsconfigRootDir: resolve(__dirname, "src/apps/portal"),
      },
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    rules: {
      ...portalNextConfig.rules,
      "@typescript-eslint/no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
      "no-console": "off",
      "@next/next/no-html-link-for-pages": "off",
      "react/react-in-jsx-scope": "off",
    },
    settings: {
      ...portalNextConfig.settings,
      next: {
        rootDir: ["src/apps/portal"],
      },
    },
  }
);
