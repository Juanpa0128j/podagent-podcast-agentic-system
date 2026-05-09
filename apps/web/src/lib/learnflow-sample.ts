import type { Plan, SectionContent } from "../types/learnflow";

export const samplePlan: Plan = {
  goal: "Mejorar Concentracion",
  estimated_duration: "4 semanas",
  phases: [
    {
      name: "Fase 1: Base neurobiologica",
      duration: "Semana 1",
      steps: [
        {
          action: "Configura ventanas de enfoque de 90 minutos",
          when: "Manana",
          duration: "90 min",
          why: "Alinea el trabajo profundo con picos de alerta",
        },
        {
          action: "Limita cafeina despues de las 14:00",
          when: "Tarde",
          duration: "Diario",
          why: "Protege la calidad del sueno y la atencion",
        },
      ],
    },
    {
      name: "Fase 2: Consolidacion",
      duration: "Semanas 2-3",
      steps: [
        {
          action: "Introduce respiracion fisiologica",
          when: "Antes de estudiar",
          duration: "2-3 min",
          why: "Reduce el estres agudo y mejora la concentracion",
        },
      ],
    },
    {
      name: "Fase 3: Dominio",
      duration: "Semana 4",
      steps: [
        {
          action: "Evalua progreso con pruebas cortas",
          when: "Fin de semana",
          duration: "20 min",
          why: "Refuerza la memoria activa",
        },
      ],
    },
  ],
  dos: [
    {
      action: "Bloquea tiempo sin notificaciones",
      when: "Durante sesiones de estudio",
      why: "Evita interrupciones que rompen el foco",
    },
    {
      action: "Usa luz natural al comenzar",
      when: "Mananas",
      why: "Activa el estado de alerta",
    },
  ],
  donts: [
    {
      action: "Multitarea",
      why: "Reduce la calidad del aprendizaje",
    },
    {
      action: "Saltarte el descanso",
      why: "Afecta la retencion",
    },
  ],
  relevant_content: [
    {
      section_id: "focus-101",
      reason: "Explica ciclos de atencion y dopamina",
    },
    {
      section_id: "sleep-boost",
      reason: "Relacion entre sueno profundo y memoria",
    },
  ],
};

export const sampleSection: SectionContent = {
  section_id: "focus-101",
  summary:
    "Esta seccion explica como los ciclos de alerta influyen en la concentracion. Conecta la respiracion y la luz natural con mayor enfoque.",
  key_points: [
    "Los ciclos ultradianos duran ~90 minutos",
    "La luz matutina mejora el estado de alerta",
    "Breves descansos sostienen la atencion",
  ],
  glossary: [
    {
      term: "Ciclo ultradiano",
      definition: "Ritmo biologico de 90-120 minutos en el cuerpo",
    },
    {
      term: "Dopamina",
      definition: "Neurotransmisor asociado a motivacion y enfoque",
    },
  ],
  flashcards: [
    {
      id: "fc-1",
      question: "Cuanto dura un ciclo ultradiano tipico?",
      answer: "Aproximadamente 90 minutos.",
    },
    {
      id: "fc-2",
      question: "Por que la luz matutina ayuda al enfoque?",
      answer: "Activa el sistema de alerta y regula el ritmo circadiano.",
    },
    {
      id: "fc-3",
      question: "Que efecto tienen los descansos cortos?",
      answer: "Recargan la atencion y previenen la fatiga.",
    },
    {
      id: "fc-4",
      question: "Que neurotransmisor se asocia al enfoque?",
      answer: "La dopamina.",
    },
    {
      id: "fc-5",
      question: "Que practica reduce el estres antes de estudiar?",
      answer: "La respiracion fisiologica.",
    },
  ],
};
