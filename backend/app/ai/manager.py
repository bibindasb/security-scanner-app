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
        if settings.OPENROUTE_API_KEY and settings.OPENROUTE_API_KEY != "sk-or-v1-your_actual_openrouter_api_key_here":
            try:
                self.providers['openrouter'] = OpenRouterProvider(
                    api_key=settings.OPENROUTE_API_KEY,
                    model=settings.OPENROUTE_MODEL
                )
                print(f"✅ OpenRouter provider initialized with model: {settings.OPENROUTE_MODEL}")
            except Exception as e:
                print(f"⚠️  Failed to initialize OpenRouter provider: {str(e)}")
        
        # Gemini provider
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_actual_gemini_api_key_here":
            try:
                self.providers['gemini'] = GeminiProvider(
                    api_key=settings.GEMINI_API_KEY,
                    model=settings.GEMINI_MODEL
                )
                print(f"✅ Gemini provider initialized with model: {settings.GEMINI_MODEL}")
            except Exception as e:
                print(f"⚠️  Failed to initialize Gemini provider: {str(e)}")
        
        # Fallback to OpenRouter if available and no providers were initialized
        if not self.providers and settings.OPENROUTE_API_KEY and settings.OPENROUTE_API_KEY != "sk-or-v1-your_actual_openrouter_api_key_here":
            try:
                self.providers['openrouter'] = OpenRouterProvider(
                    api_key=settings.OPENROUTE_API_KEY,
                    model=settings.OPENROUTE_MODEL
                )
                print(f"✅ OpenRouter provider initialized as fallback with model: {settings.OPENROUTE_MODEL}")
            except Exception as e:
                print(f"⚠️  Failed to initialize OpenRouter fallback: {str(e)}")
        
        if not self.providers:
            print("⚠️  No AI providers available. Please configure valid API keys in .env file")
    
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
        
        try:
            result = await self.providers[provider].analyze_findings(findings)
            
            # If the result contains an error and we have other providers, try fallback
            if 'error' in result and len(self.providers) > 1:
                fallback_providers = [p for p in self.providers.keys() if p != provider]
                for fallback_provider in fallback_providers:
                    try:
                        print(f"⚠️  {provider} failed, trying fallback to {fallback_provider}")
                        fallback_result = await self.providers[fallback_provider].analyze_findings(findings)
                        if 'error' not in fallback_result:
                            return fallback_result
                    except Exception as e:
                        print(f"⚠️  Fallback to {fallback_provider} also failed: {str(e)}")
                        continue
            
            return result
            
        except Exception as e:
            # If the primary provider fails completely, try other providers
            if len(self.providers) > 1:
                fallback_providers = [p for p in self.providers.keys() if p != provider]
                for fallback_provider in fallback_providers:
                    try:
                        print(f"⚠️  {provider} failed with exception, trying fallback to {fallback_provider}")
                        return await self.providers[fallback_provider].analyze_findings(findings)
                    except Exception as fallback_e:
                        print(f"⚠️  Fallback to {fallback_provider} also failed: {str(fallback_e)}")
                        continue
            
            # If all providers fail, return a generic error
            return {
                "error": f"All AI providers failed. Last error: {str(e)}",
                "summary": "AI analysis unavailable - All providers failed",
                "prioritized_remediation": [],
                "additional_recommendations": [],
                "troubleshooting": {
                    "issue": "All AI providers unavailable",
                    "solution": "Check your API keys and network connection",
                    "steps": [
                        "1. Verify API keys in .env file are valid",
                        "2. Check internet connection",
                        "3. Restart the application",
                        "4. Check provider status pages"
                    ]
                }
            }
    
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