"use client";

import { useEffect, useState } from "react";
import { generateSectionContent } from "../../lib/mcp-client";
import { useLearnFlow } from "../../lib/plan-store";
import MCPAppRenderer from "../../lib/mcp-apps/renderer";
import type { SectionContent } from "../../types/learnflow";

interface SectionLoaderProps {
  sectionId: string;
  goal?: string;
  fallbackSection: SectionContent;
  /** Title shown in SectionView header. Defaults to a generic label. */
  title?: string;
  /** Description shown in SectionView header. Defaults to a generic label. */
  description?: string;
}

const SECTION_HINT = { component: "SectionView", version: 1 } as const;

const DEFAULT_TITLE = "Regulacion de enfoque y energia";
const DEFAULT_DESCRIPTION =
  "Resumen del episodio con foco en atencion sostenida y aprendizaje activo.";

export default function SectionLoader({
  sectionId,
  goal,
  fallbackSection,
  title = DEFAULT_TITLE,
  description = DEFAULT_DESCRIPTION,
}: SectionLoaderProps) {
  const { state, actions } = useLearnFlow();
  const [content, setContent] = useState<SectionContent>(
    state.section?.section_id === sectionId ? state.section : fallbackSection
  );

  const effectiveGoal = goal ?? state.plan?.goal ?? "";

  useEffect(() => {
    if (!effectiveGoal) {
      return;
    }

    if (state.section?.section_id === sectionId) {
      setContent(state.section);
      return;
    }

    let cancelled = false;

    generateSectionContent(sectionId, effectiveGoal)
      .then((fetched) => {
        if (cancelled) {
          return;
        }
        actions.setSection(fetched);
        setContent(fetched);
      })
      .catch(() => {
        // Keep fallback on error
      });

    return () => {
      cancelled = true;
    };
  }, [sectionId, effectiveGoal, state.section, actions]);

  return (
    <MCPAppRenderer
      hint={SECTION_HINT}
      data={{ title, description, content }}
    />
  );
}
