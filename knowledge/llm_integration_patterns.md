# LLM Integration Patterns

This document establishes standardized patterns for integrating Large Language Models (LLMs) into homelab projects, ensuring consistency, auditability, and resilience.

## 1. Database Schema for Auditing
All LLM interactions should be persisted for troubleshooting and quality assessment.

### Recommended `TranslationHistory` Schema (FastAPI/SQLAlchemy)
```python
class LLMLog(Base):
    __tablename__ = "llm_logs"
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Context
    request_id = Column(String, index=True)  # Trace ID for end-to-end debugging
    feature_area = Column(String)            # e.g., "translation", "summarization"
    
    # Model Metadata
    model_id = Column(String)               # The actual model string used (e.g., "gpt-4o")
    provider = Column(String)               # e.g., "openai", "local-ollama"
    
    # Prompt & Response
    prompt_template = Column(String)        # Name or version of the prompt
    input_text = Column(Text)
    output_text = Column(Text)
    
    # Performance & Cost
    latency_ms = Column(Integer)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    
    # Quality (Optional)
    score = Column(Float, nullable=True)    # Automated or manual score
```

## 2. Structured Interaction (Pydantic)
Use Pydantic V2 to define clear contracts for LLM inputs and outputs.

### Pattern: Typed Response Extraction
```python
class LLMResponse(BaseModel):
    content: str
    usage: Dict[str, int]
    model: str
    finish_reason: str
```

## 3. Resilience & Fallback Strategies
- **Timeout Management**: Always set explicit timeouts for LLM calls (e.g., 30s for complex translations).
- **Retries**: Use exponential backoff for `5xx` or rate-limit errors.
- **Failover**: If the primary `LLM_HOST` is unreachable, log a critical error and either return a meaningful "Service Unavailable" response or switch to a lightweight local fallback (e.g., a tiny local Ollama model).

## 4. Prompt Management
- **Versioned Templates**: Avoid hardcoding prompts in Python logic. Use a central `prompts.yaml` or a dedicated `PromptBuilder` class.
- **Environment Variables**: Use `.env` only for model selection (`LLM_MODEL`) and API keys, not for the prompt text itself.

## 5. Testing & Mocking
- **Isolation**: Always mock LLM responses in the primary test suite to ensure speed and zero-cost testing.
- **Metadata Assertions**: Tests MUST verify that token usage and latency metadata are correctly captured and persisted, even when using mocked responses.
- **Edge Cases**: Mock LLM failures (e.g., `429 Too Many Requests`) to verify the application's error handling and reporting logic.
