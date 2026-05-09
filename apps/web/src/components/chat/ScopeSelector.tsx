"use client";

export default function ScopeSelector() {
  return (
    <select className="rounded border px-2 py-1 text-sm">
      <option value="library">All podcasts</option>
      <option value="podcast">This podcast</option>
      <option value="episode">This episode</option>
    </select>
  );
}
