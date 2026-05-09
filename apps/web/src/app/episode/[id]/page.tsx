export default async function EpisodePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return (
    <main className="flex h-screen flex-col p-4">
      <h1 className="text-2xl font-bold">Episode {id}</h1>
      <p className="text-slate-500">Episode detail stub.</p>
    </main>
  );
}
