# backend/app/scanners/ssl_scanner.py
import ssl
import socket
from typing import Dict, Any, List
from .base import BaseScanner
from datetime import datetime

class SSLScanner(BaseScanner):
    async def scan(self) -> List[Dict[str, Any]]:
        findings = []
        
        try:
            hostname = self.target_url.split('//')[-1].split('/')[0].split(':')[0]
            
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Check certificate expiration
                    expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (expiry_date - datetime.utcnow()).days
                    
                    if days_until_expiry < 30:
                        findings.append({
                            'type': 'vulnerability',
                            'severity': 'high',
                            'title': 'SSL Certificate Expiring Soon',
                            'description': f'SSL certificate expires in {days_until_expiry} days.',
                            'remediation': 'Renew SSL certificate immediately.',
                            'owasp_category': 'A02:2021 - Cryptographic Failures',
                            'location': 'SSL/TLS'
                        })
                    
                    # Check protocol version
                    if ssock.version() in ['TLSv1', 'TLSv1.1']:
                        findings.append({
                            'type': 'vulnerability',
                            'severity': 'high',
                            'title': 'Weak TLS Protocol Version',
                            'description': f'Using deprecated TLS version: {ssock.version()}',
                            'remediation': 'Upgrade to TLSv1.2 or higher.',
                            'owasp_category': 'A02:2021 - Cryptographic Failures',
                            'location': 'SSL/TLS'
                        })
        
        except Exception as e:
            findings.append({
                'type': 'error',
                'severity': 'info',
                'title': 'SSL Scan Failed',
                'description': f'Failed to scan SSL configuration: {str(e)}',
                'location': 'SSL/TLS'
            })
        
        return findings