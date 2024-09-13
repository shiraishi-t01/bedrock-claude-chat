import { BedrockKnowledgeBase } from '../features/knowledgeBase/types';

export type BotKind = 'private' | 'mixed';

export type BotMeta = {
  id: string;
  title: string;
  description: string;
  createTime: Date;
  lastUsedTime: Date;
  isPublic: boolean;
  isPinned: boolean;
  owned: boolean;
  syncStatus: BotSyncStatus;
};

export type BotKnowledge = {
  sourceUrls: string[];
  // Sitemap cannot be used yet.
  sitemapUrls: string[];
  filenames: string[];
  s3Urls: string[];
};

export type ConversationQuickStarter = {
  title: string;
  example: string;
};

export type EmdeddingParams = {
  chunkSize: number;
  chunkOverlap: number;
  enablePartitionPdf: boolean;
};

export type BotKnowledgeDiff = {
  sourceUrls: string[];
  // Sitemap cannot be used yet.
  sitemapUrls: string[];
  addedFilenames: string[];
  deletedFilenames: string[];
  unchangedFilenames: string[];
  s3Urls: string[];
};

export type BotSyncStatus = 'QUEUED' | 'RUNNING' | 'SUCCEEDED' | 'FAILED';

export type BotListItem = BotMeta & {
  available: boolean;
  hasBedrockKnowledgeBase: boolean;
};

export type GenerationParams = {
  maxTokens: number;
  topK: number;
  topP: number;
  temperature: number;
  stopSequences: string[];
};

export type SearchParams = {
  maxResults: number;
};

export type BotDetails = BotMeta & {
  instruction: string;
  embeddingParams: EmdeddingParams;
  generationParams: GenerationParams;
  searchParams: SearchParams;
  agent: Agent;
  knowledge: BotKnowledge;
  syncStatusReason: string;
  displayRetrievedChunks: boolean;
  conversationQuickStarters: ConversationQuickStarter[];
  bedrockKnowledgeBase: BedrockKnowledgeBase | null;
};

export type BotSummary = BotMeta & {
  hasKnowledge: boolean;
  hasAgent: boolean;
  ownedAndHasBedrockKnowledgeBase: boolean;
  conversationQuickStarters: ConversationQuickStarter[];
};

export type BotFile = {
  filename: string;
  status: 'UPLOADING' | 'UPLOADED' | 'ERROR';
  errorMessage?: string;
  progress?: number;
};

export type RegisterBotRequest = {
  id: string;
  title: string;
  instruction: string;
  agent: AgentInput;
  description?: string;
  embeddingParams?: EmdeddingParams | null;
  generationParams?: GenerationParams;
  searchParams?: SearchParams;
  knowledge?: BotKnowledge;
  displayRetrievedChunks: boolean;
  conversationQuickStarters: ConversationQuickStarter[];
  bedrockKnowledgeBase?: BedrockKnowledgeBase;
};

export type RegisterBotResponse = BotDetails;

export type UpdateBotRequest = {
  title: string;
  instruction: string;
  description?: string;
  agent: AgentInput;
  embeddingParams?: EmdeddingParams | null;
  generationParams?: BotGenerationConfig;
  searchParams?: SearchParams;
  knowledge?: BotKnowledgeDiff;
  displayRetrievedChunks: boolean;
  conversationQuickStarters: ConversationQuickStarter[];
  bedrockKnowledgeBase?: BedrockKnowledgeBase;
};

export type UpdateBotResponse = {
  id: string;
  title: string;
  instruction: string;
  description: string;
  embeddingParams: EmdeddingParams;
  generationParams: GenerationParams;
  searchParams: SearchParams;
  knowledge?: BotKnowledge;
  displayRetrievedChunks: boolean;
  conversationQuickStarters: ConversationQuickStarter[];
  bedrockKnowledgeBase: BedrockKnowledgeBase;
};

export type UpdateBotPinnedRequest = {
  pinned: boolean;
};

export type UpdateBotPinnedResponse = null;

export type UpdateBotVisibilityRequest = {
  toPublic: boolean;
};

export type UpdateBotVisibilityResponse = null;

export type GetBotsRequest =
  | {
      kind: 'private';
      limit?: number;
    }
  | {
      kind: 'mixed';
      limit: number;
    }
  | {
      kind: 'mixed';
      pinned: boolean;
    };

export type GetBotsResponse = BotListItem[];

export type GetMyBotResponse = BotDetails;

export type GetBotSummaryResponse = BotSummary;

export type GetPublicBotResponse = BotDetails;

export type GetPresignedUrlResponse = {
  url: string;
};
