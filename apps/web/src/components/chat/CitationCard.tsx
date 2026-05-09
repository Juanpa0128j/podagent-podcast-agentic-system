interface CitationCardProps {
  episodeTitle: string;
  podcastName: string;
  tsStart: number;
  tsEnd: number;
  excerpt: string;
}

export default function CitationCard({
  episodeTitle,
  podcastName,
  tsStart,
  excerpt,
}: CitationCardProps) {
  return (
    <div className="rounded border bg-slate-50 p-3 text-sm">
      <p className="font-semibold">{episodeTitle}</p>
      <p className="text-slate-500">{podcastName}</p>
      <p className="mt-1 text-slate-700">{excerpt}</p>
      <p className="mt-1 text-xs text-slate-400">{tsStart}s</p>
    </div>
  );
}
