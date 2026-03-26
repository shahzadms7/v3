"""
GovRAG V3 — AI Provider (100% Azure OpenAI)
Created: March 21, 2026 | Microsoft Hackathon
100% Azure Stack — Azure OpenAI gpt-4o-mini
"""

import json
import httpx
import re
import os
from .config import settings


class AIProvider:
    """Azure OpenAI provider — 100% Microsoft Azure stack."""

    async def generate(self, system_prompt: str, user_prompt: str) -> dict:
        """
        Call Azure OpenAI gpt-4o-mini.
        Returns: {"text": str, "provider": str, "model": str}
        """
        endpoint = settings.AZURE_OPENAI_ENDPOINT.rstrip("/")
        key = settings.AZURE_OPENAI_KEY
        deploy = settings.AZURE_OPENAI_DEPLOYMENT

        if not endpoint or not key:
            raise RuntimeError("AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_KEY not configured")

        url = f"{endpoint}/openai/deployments/{deploy}/chat/completions?api-version={settings.AZURE_OPENAI_API_VERSION}"
        async with httpx.AsyncClient(timeout=settings.AI_TIMEOUT_SECONDS) as client:
            resp = await client.post(
                url,
                headers={"api-key": key, "Content-Type": "application/json"},
                json={
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": settings.AI_TEMPERATURE,
                    "max_tokens": settings.AI_MAX_TOKENS,
                },
            )
            resp.raise_for_status()
            text = resp.json()["choices"][0]["message"]["content"]
            return {"text": text.strip(), "provider": "Azure OpenAI", "model": deploy}

    @staticmethod
    def extract_json(text: str) -> dict:
        """Extract JSON from AI response (handles markdown code blocks)."""
        try:
            return json.loads(text)
        except (json.JSONDecodeError, TypeError):
            pass

        code_block = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if code_block:
            try:
                return json.loads(code_block.group(1))
            except (json.JSONDecodeError, TypeError):
                pass

        json_match = re.search(r"\{[\s\S]*\}", text)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except (json.JSONDecodeError, TypeError):
                pass

        return {
            "answer": text,
            "sources_cited": [],
            "confidence": 50,
            "warnings": ["Could not parse structured response"],
        }


# Singleton
ai_provider = AIProvider()
