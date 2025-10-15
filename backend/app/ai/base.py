# backend/app/ai/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json

class AIProvider(ABC):
    @abstractmethod
    async def analyze_findings(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        pass