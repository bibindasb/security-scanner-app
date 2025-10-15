# backend/app/ai/ollama_provider.py
import ollama
from typing import Dict, Any, List
from .base import AIProvider

class OllamaProvider(AIProvider):
    def __init__(self, base_url: str, model: str = "llama2"):
        self.client = ollama.Client(host=base_url)
        self.model = model
    
    async def analyze_findings(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        prompt = self._build_prompt(findings)
        
        try:
            response = self.client.generate(model=self.model, prompt=prompt)
            analysis = self._parse_response(response['response'])
            return analysis
        except Exception as e:
            return {
                "error": str(e),
                "prioritized_remediation": [],
                "sample_code": {}
            }
    
    def _build_prompt(self, findings: List[Dict[str, Any]]) -> str:
        findings_json = json.dumps(findings, indent=2)
        
        return f"""
        Analyze these security scan findings and provide:
        1. Prioritized remediation steps based on severity
        2. Sample code/commands for fixes
        3. Additional security recommendations
        
        Findings:
        {findings_json}
        
        Respond in JSON format:
        {{
            "summary": "Overall risk assessment",
            "prioritized_remediation": [
                {{
                    "priority": "critical|high|medium|low",
                    "action": "specific action to take",
                    "findings_affected": ["finding_id1", "finding_id2"],
                    "sample_code": {{
                        "language": "code language",
                        "code": "sample code here"
                    }}
                }}
            ],
            "additional_recommendations": ["recommendation1", "recommendation2"]
        }}
        """
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        try:
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            return json.loads(json_str)
        except:
            return {
                "error": "Failed to parse AI response",
                "prioritized_remediation": [],
                "additional_recommendations": []
            }