from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Optional

from app.routes.schemas.base import BaseSchema
from app.routes.schemas.bot_kb import (
    BedrockKnowledgeBaseInput,
    BedrockKnowledgeBaseOutput,
)
from pydantic import Field, root_validator, validator

if TYPE_CHECKING:
    from app.repositories.models.custom_bot import BotModel

# Knowledge sync status type
# NOTE: `ORIGINAL_NOT_FOUND` is used when the original bot is removed.
type_sync_status = Literal[
    "QUEUED",
    "KNOWLEDGE_BASE_STACK_CREATED",
    "RUNNING",
    "SUCCEEDED",
    "FAILED",
    "ORIGINAL_NOT_FOUND",
]


class EmbeddingParams(BaseSchema):
    chunk_size: int
    chunk_overlap: int
    enable_partition_pdf: bool


class GenerationParams(BaseSchema):
    max_tokens: int
    top_k: int
    top_p: float
    temperature: float
    stop_sequences: list[str]


class SearchParams(BaseSchema):
    max_results: int


class AgentTool(BaseSchema):
    name: str
    description: str


class Agent(BaseSchema):
    tools: list[AgentTool]


class AgentInput(BaseSchema):
    tools: list[str] = Field(..., description="List of tool names")


class Knowledge(BaseSchema):
    source_urls: list[str]
    sitemap_urls: list[str]
    filenames: list[str]
    s3_urls: list[str]

    @validator("s3_urls", each_item=True)
    def validate_s3_url(cls, v):
        if not v.startswith("s3://"):
            raise ValueError(f"Invalid S3 URL format: {v}")

        url_parts = v.replace("s3://", "").split("/")
        if len(url_parts) < 1:
            raise ValueError(f"Invalid S3 URL format: {v}")

        bucket_name = url_parts.pop(0)
        prefix = "/".join(url_parts)

        if not bucket_name:
            raise ValueError(f"Invalid S3 URL format: {v}")

        if not v.endswith("/"):
            raise ValueError(f"Invalid S3 URL format (must end with a '/'): {v}")

        return v


class KnowledgeDiffInput(BaseSchema):
    source_urls: list[str]
    sitemap_urls: list[str]
    s3_urls: list[str]
    added_filenames: list[str]
    deleted_filenames: list[str]
    unchanged_filenames: list[str]


class ConversationQuickStarter(BaseSchema):
    title: str
    example: str


class BotInput(BaseSchema):
    id: str
    title: str
    instruction: str
    description: str | None
    embedding_params: EmbeddingParams | None
    generation_params: GenerationParams | None
    search_params: SearchParams | None
    agent: Optional[AgentInput] = None
    knowledge: Knowledge | None
    display_retrieved_chunks: bool
    conversation_quick_starters: list[ConversationQuickStarter] | None
    bedrock_knowledge_base: BedrockKnowledgeBaseInput | None = None


class BotModifyInput(BaseSchema):
    title: str
    instruction: str
    description: str | None
    embedding_params: EmbeddingParams | None
    generation_params: GenerationParams | None
    search_params: SearchParams | None
    agent: Optional[AgentInput] = None
    knowledge: KnowledgeDiffInput | None
    display_retrieved_chunks: bool
    conversation_quick_starters: list[ConversationQuickStarter] | None
    bedrock_knowledge_base: BedrockKnowledgeBaseInput | None = None

    def has_update_files(self) -> bool:
        return self.knowledge is not None and (
            len(self.knowledge.added_filenames) > 0
            or len(self.knowledge.deleted_filenames) > 0
        )

    def is_embedding_required(self, current_bot_model: BotModel) -> bool:
        if self.has_update_files():
            return True

        if self.knowledge is not None and current_bot_model.has_knowledge():
            if (
                set(self.knowledge.source_urls)
                == set(current_bot_model.knowledge.source_urls)
                and set(self.knowledge.sitemap_urls)
                == set(current_bot_model.knowledge.sitemap_urls)
                and set(self.knowledge.s3_urls)
                == set(current_bot_model.knowledge.s3_urls)
            ):
                pass
            else:
                return True

        if (
            self.embedding_params is not None
            and current_bot_model.embedding_params is not None
        ):
            if (
                self.embedding_params.chunk_size
                == current_bot_model.embedding_params.chunk_size
                and self.embedding_params.chunk_overlap
                == current_bot_model.embedding_params.chunk_overlap
                and self.embedding_params.enable_partition_pdf
                == current_bot_model.embedding_params.enable_partition_pdf
            ):
                pass
            else:
                return True

        return False


class BotModifyOutput(BaseSchema):
    id: str
    title: str
    instruction: str
    description: str
    embedding_params: EmbeddingParams
    generation_params: GenerationParams
    search_params: SearchParams
    agent: Agent
    knowledge: Knowledge
    conversation_quick_starters: list[ConversationQuickStarter]
    bedrock_knowledge_base: BedrockKnowledgeBaseOutput | None


class BotOutput(BaseSchema):
    id: str
    title: str
    description: str
    instruction: str
    create_time: float
    last_used_time: float
    is_public: bool
    is_pinned: bool
    # Whether the bot is owned by the user
    owned: bool
    embedding_params: EmbeddingParams
    generation_params: GenerationParams
    search_params: SearchParams
    agent: Agent
    knowledge: Knowledge
    sync_status: type_sync_status
    sync_status_reason: str
    sync_last_exec_id: str
    display_retrieved_chunks: bool
    conversation_quick_starters: list[ConversationQuickStarter]
    bedrock_knowledge_base: BedrockKnowledgeBaseOutput | None


class BotMetaOutput(BaseSchema):
    id: str
    title: str
    description: str
    create_time: float
    last_used_time: float
    is_pinned: bool
    is_public: bool
    owned: bool
    # Whether the bot is available or not.
    # This can be `False` if the bot is not owned by the user and original bot is removed.
    available: bool
    sync_status: type_sync_status
    has_bedrock_knowledge_base: bool


class BotSummaryOutput(BaseSchema):
    id: str
    title: str
    description: str
    create_time: float
    last_used_time: float
    is_pinned: bool
    is_public: bool
    has_agent: bool
    owned: bool
    sync_status: type_sync_status
    has_knowledge: bool
    conversation_quick_starters: list[ConversationQuickStarter]
    owned_and_has_bedrock_knowledge_base: bool = Field(
        ...,
        description="Whether the bot has Bedrock KnowledgeBase attributes. Note that if bot alias, always false.",
    )


class BotSwitchVisibilityInput(BaseSchema):
    to_public: bool


class BotPinnedInput(BaseSchema):
    pinned: bool


class BotPresignedUrlOutput(BaseSchema):
    url: str
