interface Episode {
  id: string;
  title: string;
  podcastName: string;
  status: string;
}

export default function EpisodeList({ episodes }: { episodes: Episode[] }) {
  return (
    <ul className="space-y-2">
      {episodes.map((ep) => (
        <li key={ep.id} className="rounded border p-3">
          <p className="font-medium">{ep.title}</p>
          <p className="text-sm text-slate-500">
            {ep.podcastName} — {ep.status}
          </p>
        </li>
      ))}
    </ul>
  );
}
