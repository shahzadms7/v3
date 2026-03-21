"""
GovRAG V3 — AI Provider (Multi-provider fallback chain)
Created: March 21, 2026 | Microsoft Hackathon

HOW IT WORKS (for Shahzad & Zara):
We have 3 AI providers, all FREE. If one fails, we try the next:
  Gemini Key 1 → Gemini Key 2 → Grok → Error

WHY multiple providers?
- Gemini has rate limits on free tier
- If Google is down, Grok still works
- For judges: shows enterprise resilience pattern
"""

import json
import asyncio
import httpx
import google.generativeai as genai
from .config import settings


class AIProvider:
    """Multi-provider AI with automatic fallback."""

    def __init__(self):
        self.providers = []
        self._setup_providers()

    def _setup_providers(self):
        """Register all available AI providers."""

        # Provider 1: Gemini Key 1
        if settings.GEMINI_API_KEY:
            self.providers.append({
                "name": "Gemini-1",
                "models": ["gemini-2.0-flash", "gemini-1.5-flash"],
                "key": settings.GEMINI_API_KEY,
                "type": "gemini",
            })

        # Provider 2: Gemini Key 2
        if settings.GEMINI_API_KEY_2:
            self.providers.append({
                "name": "Gemini-2",
                "models": ["gemini-2.0-flash", "gemini-1.5-flash"],
                "key": settings.GEMINI_API_KEY_2,
                "type": "gemini",
            })

        # Provider 3: Grok (xAI)
        if settings.GROK_API_KEY:
            self.providers.append({
                "name": "Grok",
                "models": ["grok-3-mini-fast"],
                "key": settings.GROK_API_KEY,
                "type": "grok",
            })

    async def _call_gemini(self, key: str, model: str, system: str, user: str) -> str:
        """Call Google Gemini API."""
        genai.configure(api_key=key)
        m = genai.GenerativeModel(model)
        response = await asyncio.to_thread(
            m.generate_content,
            f"{system}\n\n{user}",
            generation_config=genai.GenerationConfig(
                temperature=settings.AI_TEMPERATURE,
                max_output_tokens=settings.AI_MAX_TOKENS,
            ),
        )
        return response.text

    async def _call_grok(self, key: str, model: str, system: str, user: str) -> str:
        """Call Grok (xAI) API — OpenAI-compatible endpoint."""
        async with httpx.AsyncClient(timeout=settings.AI_TIMEOUT_SECONDS) as client:
            resp = await client.post(
                "https://api.x.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    "temperature": settings.AI_TEMPERATURE,
                    "max_tokens": settings.AI_MAX_TOKENS,
                },
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]

    async def generate(self, system_prompt: str, user_prompt: str) -> dict:
        """
        Call AI with full fallback chain.
        Returns: {"text": str, "provider": str, "model": str}
        """
        errors = []

        for provider in self.providers:
            for model in provider["models"]:
                try:
                    if provider["type"] == "gemini":
                        text = await self._call_gemini(provider["key"], model, system_prompt, user_prompt)
                    elif provider["type"] == "grok":
                        text = await self._call_grok(provider["key"], model, system_prompt, user_prompt)
                    else:
                        continue

                    if text and text.strip():
                        return {"text": text.strip(), "provider": provider["name"], "model": model}

                except Exception as e:
                    errors.append(f"{provider['name']}/{model}: {str(e)[:100]}")

        raise RuntimeError(f"All AI providers failed: {' | '.join(errors)}")

    @staticmethod
    def extract_json(text: str) -> dict:
        """Extract JSON from AI response (handles markdown code blocks)."""
        # Direct parse
        try:
            return json.loads(text)
        except (json.JSONDecodeError, TypeError):
            pass

        # From markdown code block
        import re
        code_block = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if code_block:
            try:
                return json.loads(code_block.group(1))
            except (json.JSONDecodeError, TypeError):
                pass

        # Find JSON object
        json_match = re.search(r"\{[\s\S]*\}", text)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except (json.JSONDecodeError, TypeError):
                pass

        # Fallback: return as raw text
        return {
            "answer": text,
            "sources_cited": [],
            "confidence": 50,
            "warnings": ["Could not parse structured response"],
        }


# Singleton
ai_provider = AIProvider()
