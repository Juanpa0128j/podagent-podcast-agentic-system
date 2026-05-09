export interface Episode {
  id: string;
  title: string;
  description: string;
  duration: number;
  podcastName: string;
  source: string;
  status: string;
}

export interface Chunk {
  id: number;
  text: string;
  tsStart: number;
  tsEnd: number;
  episodeId: string;
  score?: number;
}

export interface SearchScope {
  type: "episode" | "podcast" | "library";
  id?: string;
}
