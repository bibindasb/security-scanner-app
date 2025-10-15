# backend/app/ai/manager.py
from typing import Dict, Any, List
from .ollama_provider import OllamaProvider
from app.config import settings

class AIManager:
    def __init__(self):
        self.providers = {}
        self._setup_providers()
    
    def _setup_providers(self):
        # Local Ollama provider
        self.providers['ollama'] = OllamaProvider(
            base_url=settings.OLLAMA_BASE_URL,
            model="llama2"
        )
        
        # Additional providers can be added here
        # self.providers['openai'] = OpenAIProvider(api_key=settings.OPENAI_API_KEY)
    
    async def analyze_scan(self, findings: List[Dict[str, Any]], provider: str = "ollama") -> Dict[str, Any]:
        if provider not in self.providers:
            raise ValueError(f"Provider {provider} not available")
        
        return await self.providers[provider].analyze_findings(findings)