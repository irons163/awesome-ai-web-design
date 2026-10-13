import type { ReactNode } from "react";

export const metadata = {
  title: "Awesome AI Web Design",
  description: "74 design studies with original AI prompts and preserved previews.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return <html lang="zh-Hant"><body>{children}</body></html>;
}
