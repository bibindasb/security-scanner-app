# backend/app/ai/openrouter_provider.py
import httpx
import json
from typing import Dict, Any, List
from .base import AIProvider

class OpenRouterProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "meta-llama/llama-2-70b-chat"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://security-scanner.app",
            "X-Title": "Security Scanner"
        }
    
    async def analyze_findings(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        prompt = self._build_prompt(findings)
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json={
                        "model": self.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a cybersecurity expert analyzing security scan findings. Provide detailed, actionable remediation steps in JSON format."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.3,
                        "max_tokens": 2000
                    }
                )
                
                if response.status_code != 200:
                    raise Exception(f"OpenRouter API error: {response.status_code} - {response.text}")
                
                data = response.json()
                ai_response = data["choices"][0]["message"]["content"]
                analysis = self._parse_response(ai_response)
                return analysis
                
        except Exception as e:
            return {
                "error": f"OpenRouter analysis failed: {str(e)}",
                "summary": "AI analysis unavailable",
                "prioritized_remediation": [],
                "additional_recommendations": []
            }
    
    def _build_prompt(self, findings: List[Dict[str, Any]]) -> str:
        findings_json = json.dumps(findings, indent=2)
        
        return f"""
        Analyze these security scan findings and provide a comprehensive security assessment. Focus on:

        1. **Risk Assessment**: Overall security posture and critical issues
        2. **Prioritized Remediation**: Specific, actionable steps ordered by severity
        3. **Technical Details**: Sample code, commands, and configuration examples
        4. **Additional Recommendations**: Proactive security measures

        **Security Findings:**
        {findings_json}

        **Response Format (JSON):**
        {{
            "summary": "Overall risk assessment and key findings summary",
            "risk_score": "high|medium|low",
            "prioritized_remediation": [
                {{
                    "priority": "critical|high|medium|low",
                    "action": "Specific action to take",
                    "description": "Detailed explanation of the action",
                    "findings_affected": ["finding_id1", "finding_id2"],
                    "sample_code": {{
                        "language": "code language",
                        "code": "sample code/commands here",
                        "explanation": "What this code does"
                    }},
                    "verification": "How to verify the fix"
                }}
            ],
            "additional_recommendations": [
                {{
                    "category": "Security Category",
                    "recommendation": "Specific recommendation",
                    "rationale": "Why this is important"
                }}
            ],
            "compliance_notes": "Any relevant compliance considerations (OWASP, NIST, etc.)"
        }}

        Ensure all responses are practical, specific, and immediately actionable for security teams.
        """
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        try:
            # Clean the response - remove markdown code blocks if present
            cleaned_response = response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            
            # Extract JSON from response
            start = cleaned_response.find('{')
            end = cleaned_response.rfind('}') + 1
            
            if start == -1 or end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = cleaned_response[start:end]
            return json.loads(json_str)
            
        except Exception as e:
            return {
                "error": f"Failed to parse OpenRouter response: {str(e)}",
                "summary": "AI analysis completed but response parsing failed",
                "prioritized_remediation": [],
                "additional_recommendations": [],
                "raw_response": response[:500] + "..." if len(response) > 500 else response
            }