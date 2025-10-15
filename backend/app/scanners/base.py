# backend/app/scanners/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import asyncio
import aiohttp

class BaseScanner(ABC):
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.results = []
    
    @abstractmethod
    async def scan(self) -> List[Dict[str, Any]]:
        pass
