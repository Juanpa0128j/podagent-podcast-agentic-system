import SectionLoader from "../../../components/learnflow/SectionLoader";
import { sampleSection } from "../../../lib/learnflow-sample";

interface SectionPageProps {
  params: Promise<{ id: string }>;
  searchParams?: Promise<{ goal?: string | string[] }>;
}

export default async function SectionPage({
  params,
  searchParams,
}: SectionPageProps) {
  const { id } = await params;
  const resolved = (await searchParams) ?? {};
  const goalParam = Array.isArray(resolved.goal)
    ? resolved.goal[0]
    : resolved.goal;

  const fallbackSection = {
    ...sampleSection,
    section_id: id,
  };

  return (
    <SectionLoader
      sectionId={id}
      goal={goalParam}
      fallbackSection={fallbackSection}
    />
  );
}
