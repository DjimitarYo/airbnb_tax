import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Host Cleaner Marketplace",
  description: "Marketplace for Bulgarian short-term rental hosts and verified cleaners.",
  applicationName: "Host Cleaner Marketplace",
};

export const viewport: Viewport = {
  themeColor: "#0f766e",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

