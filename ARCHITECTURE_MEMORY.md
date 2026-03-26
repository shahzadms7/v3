## ARCHITECTURE_MEMORY.md

### User Task
1. Application not giving 20 tools (modules) when doing analysis.
2. Analysis speed is too slow (1 minute).
3. `README.md` not updated.

### Key Finding: Critical AI Provider Misconfiguration
*   The system's core AI inference engine is dysfunctional. Documentation (`ARCHITECTURE.md`) states Azure OpenAI is primary with Gemini/Grok fallbacks. However, `app/core/ai_provider.py` attempts to use only Gemini/Grok, but `app/core/config.py` *does not provide API keys for Gemini or Grok*, leading to *no AI providers being initialized whatsoever* for module generation.
*   This is the direct cause of modules returning "No output available for this section" and a major contributor to performance issues.

### Architectural Proposal for AI Provider Configuration
**Problem Summary:** No AI provider is correctly initialized, causing modules to fail.

**Architectural Decision:** Prioritize and correctly implement Azure OpenAI as the sole AI provider for core module generation in V3, aligning with the project's "100% Microsoft Azure Stack" focus and existing `config.py` setup.

**Proposed Changes:**
1.  **Modify `app/core/ai_provider.py`:**
    *   Remove Gemini/Grok configuration logic.
    *   Implement logic to directly initialize and use Azure OpenAI (using `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_KEY`, `AZURE_OPENAI_DEPLOYMENT` from `settings`).
    *   Add a `_call_azure_openai` method and update `generate` to use it.
2.  **Verify `app/core/config.py`:** Ensure `AZURE_OPENAI` settings are correctly loaded (already confirmed).
3.  **Update `app/api/main.py`:** Ensure the `ai_provider` instance is correctly imported and passed to module generation functions.

**Impact:**
*   **Resolves "No output available"**: Modules will generate content.
*   **Improves Performance**: Utilizes the intended, optimized Azure OpenAI deployment.
*   **Aligns Architecture**: Brings implementation in line with documentation emphasis on Azure.

### Next Steps (Action Plan)
I have identified the root cause for the 