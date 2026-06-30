import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TalentGraph AI",
  description: "Explainable Hiring Intelligence Platform"
};

import { execSync } from "child_process";

let buildInfo = "Unknown Build";
try {
  // Read git info at runtime/build-time
  const sha = execSync('git log -n 1 --format="%h"', { encoding: 'utf-8' }).trim();
  const branch = execSync('git rev-parse --abbrev-ref HEAD', { encoding: 'utf-8' }).trim();
  const time = new Date().toISOString();
  buildInfo = `SHA: ${sha} | Branch: ${branch} | Time: ${time}`;
} catch (e) {
  console.error("Failed to read git info", e);
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <div style={{ position: 'fixed', bottom: 0, left: 0, right: 0, background: '#111', color: '#0f0', padding: '8px', zIndex: 9999, textAlign: 'center', fontFamily: 'monospace', fontSize: '12px', borderTop: '1px solid #333' }}>
          LIVE BUILD INFO: {buildInfo}
        </div>
        {children}
      </body>
    </html>
  );
}
