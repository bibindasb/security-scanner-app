# backend/app/scanners/headers_scanner.py
import aiohttp
import re
from typing import Dict, Any, List
from .base import BaseScanner

class HeadersScanner(BaseScanner):
    async def scan(self) -> List[Dict[str, Any]]:
        findings = []
        
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers={'User-Agent': 'SecurityScanner/1.0'}
            ) as session:
                async with session.get(self.target_url, allow_redirects=True) as response:
                    headers = response.headers
                    
                    # Check security headers with detailed analysis
                    security_checks = [
                        {
                            'header': 'Content-Security-Policy',
                            'severity': 'high',
                            'check': self._check_csp,
                            'description': 'Content Security Policy helps prevent XSS attacks'
                        },
                        {
                            'header': 'X-Frame-Options',
                            'severity': 'medium',
                            'check': self._check_frame_options,
                            'description': 'Prevents clickjacking attacks'
                        },
                        {
                            'header': 'X-Content-Type-Options',
                            'severity': 'low',
                            'check': self._check_content_type_options,
                            'description': 'Prevents MIME type sniffing'
                        },
                        {
                            'header': 'Strict-Transport-Security',
                            'severity': 'high',
                            'check': self._check_hsts,
                            'description': 'Enforces HTTPS connections'
                        },
                        {
                            'header': 'X-XSS-Protection',
                            'severity': 'low',
                            'check': self._check_xss_protection,
                            'description': 'Enables browser XSS filtering'
                        },
                        {
                            'header': 'Referrer-Policy',
                            'severity': 'low',
                            'check': self._check_referrer_policy,
                            'description': 'Controls referrer information'
                        },
                        {
                            'header': 'Permissions-Policy',
                            'severity': 'medium',
                            'check': self._check_permissions_policy,
                            'description': 'Controls browser features and APIs'
                        }
                    ]
                    
                    for check in security_checks:
                        header = check['header']
                        if header in headers:
                            result = check['check'](headers[header])
                            if not result['valid']:
                                findings.append({
                                    'id': f"header_{header.lower().replace('-', '_')}_misconfig",
                                    'type': 'misconfiguration',
                                    'severity': check['severity'],
                                    'title': f'Insecure {header} Configuration',
                                    'description': f'{check["description"]}. {result["issue"]}',
                                    'remediation': result['remediation'],
                                    'owasp_category': 'A05:2021 - Security Misconfiguration',
                                    'location': 'HTTP Headers',
                                    'evidence': {
                                        'header': header,
                                        'value': headers[header],
                                        'issue': result['issue']
                                    }
                                })
                        else:
                            findings.append({
                                'id': f"header_{header.lower().replace('-', '_')}_missing",
                                'type': 'misconfiguration',
                                'severity': check['severity'],
                                'title': f'Missing Security Header: {header}',
                                'description': f'{check["description"]}. The {header} header is not present.',
                                'remediation': f'Add the {header} header with appropriate configuration.',
                                'owasp_category': 'A05:2021 - Security Misconfiguration',
                                'location': 'HTTP Headers'
                            })
                    
                    # Check for dangerous headers
                    dangerous_headers = ['Server', 'X-Powered-By', 'X-AspNet-Version']
                    for header in dangerous_headers:
                        if header in headers:
                            findings.append({
                                'id': f"header_{header.lower().replace('-', '_')}_info_disclosure",
                                'type': 'information_disclosure',
                                'severity': 'low',
                                'title': f'Information Disclosure: {header}',
                                'description': f'The {header} header reveals server information that could aid attackers.',
                                'remediation': f'Remove or obfuscate the {header} header.',
                                'owasp_category': 'A05:2021 - Security Misconfiguration',
                                'location': 'HTTP Headers',
                                'evidence': {
                                    'header': header,
                                    'value': headers[header]
                                }
                            })
        
        except Exception as e:
            findings.append({
                'id': 'header_scan_error',
                'type': 'error',
                'severity': 'info',
                'title': 'Header Scan Failed',
                'description': f'Failed to scan headers: {str(e)}',
                'location': 'HTTP Headers'
            })
        
        return findings
    
    def _check_csp(self, value: str) -> Dict[str, Any]:
        """Check Content Security Policy configuration"""
        issues = []
        if not value:
            return {'valid': False, 'issue': 'CSP header is empty', 'remediation': 'Configure a proper CSP policy'}
        
        # Check for unsafe-inline or unsafe-eval
        if 'unsafe-inline' in value:
            issues.append('unsafe-inline directive allows inline scripts')
        if 'unsafe-eval' in value:
            issues.append('unsafe-eval directive allows eval() usage')
        
        if issues:
            return {
                'valid': False,
                'issue': '; '.join(issues),
                'remediation': 'Remove unsafe directives and use nonces or hashes for inline content'
            }
        
        return {'valid': True, 'issue': '', 'remediation': ''}
    
    def _check_frame_options(self, value: str) -> Dict[str, Any]:
        """Check X-Frame-Options configuration"""
        valid_values = ['DENY', 'SAMEORIGIN']
        if value.upper() not in valid_values:
            return {
                'valid': False,
                'issue': f'Invalid value: {value}',
                'remediation': 'Use DENY or SAMEORIGIN'
            }
        return {'valid': True, 'issue': '', 'remediation': ''}
    
    def _check_content_type_options(self, value: str) -> Dict[str, Any]:
        """Check X-Content-Type-Options configuration"""
        if value.lower() != 'nosniff':
            return {
                'valid': False,
                'issue': f'Should be "nosniff", got: {value}',
                'remediation': 'Set to "nosniff"'
            }
        return {'valid': True, 'issue': '', 'remediation': ''}
    
    def _check_hsts(self, value: str) -> Dict[str, Any]:
        """Check Strict-Transport-Security configuration"""
        if not value:
            return {'valid': False, 'issue': 'HSTS header is empty', 'remediation': 'Configure HSTS with max-age'}
        
        # Check for max-age
        if 'max-age' not in value:
            return {
                'valid': False,
                'issue': 'Missing max-age directive',
                'remediation': 'Add max-age directive (e.g., max-age=31536000)'
            }
        
        # Check max-age value
        max_age_match = re.search(r'max-age=(\d+)', value)
        if max_age_match:
            max_age = int(max_age_match.group(1))
            if max_age < 31536000:  # Less than 1 year
                return {
                    'valid': False,
                    'issue': f'Max-age too short: {max_age} seconds',
                    'remediation': 'Set max-age to at least 31536000 (1 year)'
                }
        
        return {'valid': True, 'issue': '', 'remediation': ''}
    
    def _check_xss_protection(self, value: str) -> Dict[str, Any]:
        """Check X-XSS-Protection configuration"""
        if value not in ['1', '1; mode=block']:
            return {
                'valid': False,
                'issue': f'Should be "1" or "1; mode=block", got: {value}',
                'remediation': 'Set to "1; mode=block" for better protection'
            }
        return {'valid': True, 'issue': '', 'remediation': ''}
    
    def _check_referrer_policy(self, value: str) -> Dict[str, Any]:
        """Check Referrer-Policy configuration"""
        valid_values = ['no-referrer', 'no-referrer-when-downgrade', 'origin', 'origin-when-cross-origin', 'same-origin', 'strict-origin', 'strict-origin-when-cross-origin', 'unsafe-url']
        if value not in valid_values:
            return {
                'valid': False,
                'issue': f'Invalid value: {value}',
                'remediation': 'Use a valid referrer policy value'
            }
        return {'valid': True, 'issue': '', 'remediation': ''}
    
    def _check_permissions_policy(self, value: str) -> Dict[str, Any]:
        """Check Permissions-Policy configuration"""
        # Basic check - more sophisticated analysis could be added
        if not value:
            return {'valid': False, 'issue': 'Permissions-Policy header is empty', 'remediation': 'Configure Permissions-Policy to restrict browser features'}
        return {'valid': True, 'issue': '', 'remediation': ''}