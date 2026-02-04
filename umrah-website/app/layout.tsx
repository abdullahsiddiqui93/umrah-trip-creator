import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Umrah Trip Creator - Plan Your Blessed Journey",
  description: "AI-powered Umrah trip planning with real-time flight and hotel options",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
