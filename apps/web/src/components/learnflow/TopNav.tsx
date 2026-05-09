import Link from "next/link";

const tabs = [
  { label: "Plan", href: "/plan" },
  { label: "Estudio", href: "/section/intro" },
  { label: "Progreso", href: "/progress" },
];

export default function TopNav() {
  return (
    <header className="sticky top-0 z-10 border-b border-slate-200/70 bg-white/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <div className="flex items-center gap-3">
          <span className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-primary text-sm font-semibold text-white">
            LF
          </span>
          <span className="text-lg font-semibold tracking-tight text-on-surface">
            LearnFlow
          </span>
        </div>
        <nav className="flex items-center gap-6 text-sm font-medium text-slate-600">
          {tabs.map((tab) => (
            <Link
              key={tab.href}
              href={tab.href}
              className="transition hover:text-primary"
            >
              {tab.label}
            </Link>
          ))}
        </nav>
        <Link
          href="/"
          className="text-sm font-medium text-slate-500 transition hover:text-primary"
        >
          Nueva meta
        </Link>
      </div>
    </header>
  );
}
