# backend/app/ai/gemini_provider.py
import httpx
import json
from typing import Dict, Any, List
from .base import AIProvider

class GeminiProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.api_key = api_key
        self.model = model
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    async def analyze_findings(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        prompt = self._build_prompt(findings)
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}?key={self.api_key}",
                    json={
                        "contents": [{
                            "parts": [{
                                "text": prompt
                            }]
                        }],
                        "generationConfig": {
                            "temperature": 0.3,
                            "maxOutputTokens": 2000,
                            "topP": 0.8,
                            "topK": 10
                        }
                    }
                )
                
                if response.status_code != 200:
                    raise Exception(f"Gemini API error: {response.status_code} - {response.text}")
                
                data = response.json()
                
                if "candidates" not in data or not data["candidates"]:
                    raise Exception("No candidates in Gemini response")
                
                ai_response = data["candidates"][0]["content"]["parts"][0]["text"]
                analysis = self._parse_response(ai_response)
                return analysis
                
        except Exception as e:
            return {
                "error": f"Gemini analysis failed: {str(e)}",
                "summary": "AI analysis unavailable",
                "prioritized_remediation": [],
                "additional_recommendations": []
            }
    
    def _build_prompt(self, findings: List[Dict[str, Any]]) -> str:
        findings_json = json.dumps(findings, indent=2)
        
        return f"""
        You are a cybersecurity expert analyzing security scan findings. Provide a comprehensive security assessment with actionable remediation steps.

        **Security Findings to Analyze:**
        {findings_json}

        **Required Analysis:**
        1. **Risk Assessment**: Overall security posture and critical issues
        2. **Prioritized Remediation**: Specific, actionable steps ordered by severity
        3. **Technical Details**: Sample code, commands, and configuration examples
        4. **Additional Recommendations**: Proactive security measures

        **Response Format (JSON only):**
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

        Focus on practical, immediately actionable security improvements. Provide specific code examples and verification steps.
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
                "error": f"Failed to parse Gemini response: {str(e)}",
                "summary": "AI analysis completed but response parsing failed",
                "prioritized_remediation": [],
                "additional_recommendations": [],
                "raw_response": response[:500] + "..." if len(response) > 500 else response
            }