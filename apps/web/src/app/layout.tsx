import "./globals.css";
import "@copilotkit/react-ui/styles.css";
import { Inter } from "next/font/google";

import TopNav from "../components/learnflow/TopNav";
import { ProgressProvider } from "../lib/progress-store";
import { LearnFlowProvider } from "../lib/plan-store";
import { CopilotShell } from "../components/copilotkit/CopilotShell";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen bg-surface text-on-surface`}>
        <LearnFlowProvider>
          <ProgressProvider>
            <CopilotShell>
              <TopNav />
              <main className="mx-auto max-w-6xl px-6 py-10">
                {children}
              </main>
            </CopilotShell>
          </ProgressProvider>
        </LearnFlowProvider>
      </body>
    </html>
  );
}
