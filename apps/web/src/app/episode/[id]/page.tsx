export default function EpisodePage({ params }: { params: { id: string } }) {
  return (
    <main className="flex h-screen flex-col p-4">
      <h1 className="text-2xl font-bold">Episode {params.id}</h1>
      <p className="text-slate-500">Episode detail stub.</p>
    </main>
  );
}
