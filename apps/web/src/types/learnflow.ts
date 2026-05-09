export interface PhaseStep {
  action: string;
  when: string;
  duration: string;
  why: string;
}

export interface Phase {
  name: string;
  duration: string;
  steps: PhaseStep[];
}

export interface ActionItem {
  action: string;
  when?: string;
  why: string;
}

export interface ContentMapping {
  section_id: string;
  reason: string;
}

export interface Plan {
  goal: string;
  estimated_duration: string;
  phases: Phase[];
  dos: ActionItem[];
  donts: ActionItem[];
  relevant_content: ContentMapping[];
}

export interface GlossaryTerm {
  term: string;
  definition: string;
}

export interface Flashcard {
  id: string;
  question: string;
  answer: string;
}

export type FlashcardResult = "known" | "unknown";

export interface SectionContent {
  section_id: string;
  summary: string;
  key_points: string[];
  glossary: GlossaryTerm[];
  flashcards: Flashcard[];
}

export interface CheckinResponse {
  date: string;
  question: string;
  answer: boolean;
}

export interface UserProgress {
  goal: string;
  plan_id: string;
  completed_steps: string[];
  completed_sections: string[];
  flashcard_results: Record<string, FlashcardResult>;
  checkin_responses: CheckinResponse[];
  streak: number;
}
