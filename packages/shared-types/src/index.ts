"""Shared types generated from Pydantic schemas.

Phase 1: hand-written. Phase 2+: auto-generated in CI.
"""

export interface ImportEpisodeRequest {
  source: "upload";
  ref: string;
}

export interface ImportEpisodeResponse {
  jobId: string;
}

export interface ImportStatusResponse {
  state: "pending" | "processing" | "ready" | "failed";
  progress: number;
  episodeId?: string;
  error?: string;
}

export interface Episode {
  id: string;
  title: string;
  description: string;
  duration: number;
  podcastName: string;
  source: string;
  sourceRef: string;
  status: string;
}

export interface Chunk {
  id: number;
  text: string;
  tsStart: number;
  tsEnd: number;
  episodeId: string;
  embedding?: number[];
  speaker?: string;
}

export interface SearchChunksRequest {
  query: string;
  scope: {
    type: "episode" | "podcast" | "library";
    id?: string;
  };
  k?: number;
  filters?: Record<string, unknown>;
}

export interface SearchChunksResult {
  chunk: Chunk;
  episodeId: string;
  tsStart: number;
  tsEnd: number;
  score: number;
}
