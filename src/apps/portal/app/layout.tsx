import type { Metadata } from "next";
import type { ReactNode } from "react";

// Global Tailwind layers (tokens + base styles) live here to keep shadcn/ui tokens hydrated.
import "./globals.css";

export const metadata: Metadata = {
  title: "Container Base Portal",
  description: "Operator and admin console for Container Base.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      {/* Tailwind utility scaffold applies default typography/background for every page. */}
      <body className="min-h-screen bg-white text-neutral-900 antialiased">{children}</body>
    </html>
  );
}
