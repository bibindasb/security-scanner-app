# backend/app/ai/manager.py
from typing import Dict, Any, List
from .openrouter_provider import OpenRouterProvider
from .gemini_provider import GeminiProvider
from app.config import settings

class AIManager:
    def __init__(self):
        self.providers = {}
        self._setup_providers()
    
    def _setup_providers(self):
        # OpenRouter provider
        if settings.OPENROUTE_API_KEY:
            self.providers['openrouter'] = OpenRouterProvider(
                api_key=settings.OPENROUTE_API_KEY,
                model="meta-llama/llama-2-70b-chat"
            )
        
        # Gemini provider
        if settings.GEMINI_API_KEY:
            self.providers['gemini'] = GeminiProvider(
                api_key=settings.GEMINI_API_KEY,
                model="gemini-pro"
            )
        
        # Fallback to OpenRouter if available
        if not self.providers and settings.OPENROUTE_API_KEY:
            self.providers['openrouter'] = OpenRouterProvider(
                api_key=settings.OPENROUTE_API_KEY,
                model="meta-llama/llama-2-70b-chat"
            )
    
    async def analyze_scan(self, findings: List[Dict[str, Any]], provider: str = None) -> Dict[str, Any]:
        # Auto-select provider if not specified
        if not provider:
            if 'openrouter' in self.providers:
                provider = 'openrouter'
            elif 'gemini' in self.providers:
                provider = 'gemini'
            else:
                raise ValueError("No AI providers available. Please configure API keys.")
        
        if provider not in self.providers:
            available = list(self.providers.keys())
            raise ValueError(f"Provider {provider} not available. Available: {available}")
        
        return await self.providers[provider].analyze_findings(findings)
    
    def get_available_providers(self) -> List[str]:
        return list(self.providers.keys())
    
    def get_provider_models(self, provider: str) -> List[str]:
        if provider == 'openrouter':
            return [
                "meta-llama/llama-2-70b-chat",
                "meta-llama/llama-2-13b-chat",
                "anthropic/claude-3-sonnet",
                "openai/gpt-3.5-turbo",
                "openai/gpt-4"
            ]
        elif provider == 'gemini':
            return [
                "gemini-pro",
                "gemini-pro-vision"
            ]
        return []