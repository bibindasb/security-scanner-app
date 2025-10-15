# backend/app/scanners/headers_scanner.py
import aiohttp
from typing import Dict, Any, List
from .base import BaseScanner

class HeadersScanner(BaseScanner):
    async def scan(self) -> List[Dict[str, Any]]:
        findings = []
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.target_url) as response:
                    headers = response.headers
                    
                    # Check security headers
                    security_headers = {
                        'Content-Security-Policy': 'medium',
                        'X-Frame-Options': 'medium',
                        'X-Content-Type-Options': 'low',
                        'Strict-Transport-Security': 'high',
                        'X-XSS-Protection': 'low'
                    }
                    
                    for header, severity in security_headers.items():
                        if header not in headers:
                            findings.append({
                                'type': 'misconfiguration',
                                'severity': severity,
                                'title': f'Missing Security Header: {header}',
                                'description': f'The {header} security header is missing.',
                                'remediation': f'Configure the {header} header appropriately.',
                                'owasp_category': 'A05:2021 - Security Misconfiguration',
                                'location': 'HTTP Headers'
                            })
        
        except Exception as e:
            findings.append({
                'type': 'error',
                'severity': 'info',
                'title': 'Header Scan Failed',
                'description': f'Failed to scan headers: {str(e)}',
                'location': 'HTTP Headers'
            })
        
        return findings