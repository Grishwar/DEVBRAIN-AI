import type { Metadata } from "next";
import "./globals.css";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

export const metadata: Metadata = {
  title: "DevBrain AI",
  description: "AI-powered Codebase Memory Assistant built with Cognee.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Sidebar />

        <div
          style={{
            marginLeft: "260px",
            minHeight: "100vh",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <Navbar />

          <main
            className="page-container"
            style={{
              flex: 1,
              padding: "32px",
            }}
          >
            {children}
          </main>

          <Footer />
        </div>
      </body>
    </html>
  );
}