# backend/app/scanners/ssl_scanner.py
import ssl
import socket
import asyncio
from typing import Dict, Any, List
from .base import BaseScanner
from datetime import datetime

class SSLScanner(BaseScanner):
    async def scan(self) -> List[Dict[str, Any]]:
        findings = []
        
        try:
            hostname = self.target_url.split('//')[-1].split('/')[0].split(':')[0]
            
            # Run SSL scan in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            findings = await loop.run_in_executor(None, self._run_ssl_scan, hostname)
        
        except Exception as e:
            findings.append({
                'id': 'ssl_scan_error',
                'type': 'error',
                'severity': 'info',
                'title': 'SSL Scan Failed',
                'description': f'Failed to scan SSL configuration: {str(e)}',
                'location': 'SSL/TLS'
            })
        
        return findings
    
    def _run_ssl_scan(self, hostname: str) -> List[Dict[str, Any]]:
        findings = []
        
        try:
            # Test different TLS versions
            tls_versions = [
                (ssl.PROTOCOL_TLSv1, 'TLSv1'),
                (ssl.PROTOCOL_TLSv1_1, 'TLSv1.1'),
                (ssl.PROTOCOL_TLSv1_2, 'TLSv1.2'),
                (ssl.PROTOCOL_TLS, 'TLSv1.3')  # This will use the highest available
            ]
            
            supported_versions = []
            weak_versions = []
            
            for protocol, version_name in tls_versions:
                try:
                    context = ssl.SSLContext(protocol)
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    
                    with socket.create_connection((hostname, 443), timeout=10) as sock:
                        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                            actual_version = ssock.version()
                            supported_versions.append(actual_version)
                            
                            if actual_version in ['TLSv1', 'TLSv1.1']:
                                weak_versions.append(actual_version)
                            
                            # Get certificate info on first successful connection
                            if not findings:  # Only get cert info once
                                cert = ssock.getpeercert()
                                findings.extend(self._analyze_certificate(cert, hostname))
                                
                except Exception:
                    continue  # Version not supported
            
            # Check for weak protocol versions
            if weak_versions:
                findings.append({
                    'id': 'ssl_weak_protocols',
                    'type': 'vulnerability',
                    'severity': 'high',
                    'title': 'Weak TLS Protocol Versions',
                    'description': f'Server supports deprecated TLS versions: {", ".join(weak_versions)}',
                    'remediation': 'Disable TLSv1 and TLSv1.1, use only TLSv1.2 or higher',
                    'owasp_category': 'A02:2021 - Cryptographic Failures',
                    'location': 'SSL/TLS',
                    'evidence': {
                        'weak_versions': weak_versions,
                        'supported_versions': supported_versions
                    }
                })
            
            # Check if only weak versions are supported
            if supported_versions and all(v in ['TLSv1', 'TLSv1.1'] for v in supported_versions):
                findings.append({
                    'id': 'ssl_only_weak_protocols',
                    'type': 'vulnerability',
                    'severity': 'critical',
                    'title': 'Only Weak TLS Protocols Supported',
                    'description': 'Server only supports deprecated TLS versions',
                    'remediation': 'Immediately upgrade to support TLSv1.2 or higher',
                    'owasp_category': 'A02:2021 - Cryptographic Failures',
                    'location': 'SSL/TLS'
                })
            
            # Test cipher suites
            cipher_findings = self._test_cipher_suites(hostname)
            findings.extend(cipher_findings)
            
        except Exception as e:
            findings.append({
                'id': 'ssl_connection_error',
                'type': 'error',
                'severity': 'info',
                'title': 'SSL Connection Failed',
                'description': f'Could not establish SSL connection: {str(e)}',
                'location': 'SSL/TLS'
            })
        
        return findings
    
    def _analyze_certificate(self, cert: dict, hostname: str) -> List[Dict[str, Any]]:
        findings = []
        
        try:
            # Check certificate expiration
            not_after = cert.get('notAfter')
            if not_after:
                expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                days_until_expiry = (expiry_date - datetime.utcnow()).days
                
                if days_until_expiry < 0:
                    findings.append({
                        'id': 'ssl_cert_expired',
                        'type': 'vulnerability',
                        'severity': 'critical',
                        'title': 'SSL Certificate Expired',
                        'description': f'SSL certificate expired {abs(days_until_expiry)} days ago',
                        'remediation': 'Immediately renew the SSL certificate',
                        'owasp_category': 'A02:2021 - Cryptographic Failures',
                        'location': 'SSL/TLS',
                        'evidence': {
                            'expiry_date': not_after,
                            'days_expired': abs(days_until_expiry)
                        }
                    })
                elif days_until_expiry < 30:
                    findings.append({
                        'id': 'ssl_cert_expiring_soon',
                        'type': 'vulnerability',
                        'severity': 'high',
                        'title': 'SSL Certificate Expiring Soon',
                        'description': f'SSL certificate expires in {days_until_expiry} days',
                        'remediation': 'Renew SSL certificate before expiration',
                        'owasp_category': 'A02:2021 - Cryptographic Failures',
                        'location': 'SSL/TLS',
                        'evidence': {
                            'expiry_date': not_after,
                            'days_until_expiry': days_until_expiry
                        }
                    })
            
            # Check certificate validity period
            not_before = cert.get('notBefore')
            if not_before and not_after:
                not_before_date = datetime.strptime(not_before, '%b %d %H:%M:%S %Y %Z')
                not_after_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                validity_days = (not_after_date - not_before_date).days
                
                if validity_days > 825:  # More than ~2.25 years
                    findings.append({
                        'id': 'ssl_cert_long_validity',
                        'type': 'information',
                        'severity': 'low',
                        'title': 'Long Certificate Validity Period',
                        'description': f'Certificate valid for {validity_days} days (over 2 years)',
                        'remediation': 'Consider shorter certificate validity periods for better security',
                        'owasp_category': 'A02:2021 - Cryptographic Failures',
                        'location': 'SSL/TLS',
                        'evidence': {
                            'validity_days': validity_days,
                            'not_before': not_before,
                            'not_after': not_after
                        }
                    })
            
            # Check subject alternative names
            san_list = []
            for ext in cert.get('subjectAltName', []):
                if ext[0] == 'DNS':
                    san_list.append(ext[1])
            
            if not san_list and hostname not in cert.get('subject', []):
                findings.append({
                    'id': 'ssl_cert_hostname_mismatch',
                    'type': 'vulnerability',
                    'severity': 'high',
                    'title': 'Certificate Hostname Mismatch',
                    'description': f'Certificate does not match hostname {hostname}',
                    'remediation': 'Ensure certificate includes the correct hostname in SAN or CN',
                    'owasp_category': 'A02:2021 - Cryptographic Failures',
                    'location': 'SSL/TLS',
                    'evidence': {
                        'hostname': hostname,
                        'cert_subject': cert.get('subject', []),
                        'san_list': san_list
                    }
                })
            
        except Exception as e:
            findings.append({
                'id': 'ssl_cert_analysis_error',
                'type': 'error',
                'severity': 'info',
                'title': 'Certificate Analysis Failed',
                'description': f'Failed to analyze certificate: {str(e)}',
                'location': 'SSL/TLS'
            })
        
        return findings
    
    def _test_cipher_suites(self, hostname: str) -> List[Dict[str, Any]]:
        findings = []
        
        # This is a simplified cipher suite test
        # In a real implementation, you'd test specific weak ciphers
        try:
            context = ssl.create_default_context()
            context.set_ciphers('HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!SRP:!CAMELLIA')
            
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cipher = ssock.cipher()
                    if cipher:
                        cipher_name = cipher[0]
                        if any(weak in cipher_name.upper() for weak in ['RC4', 'DES', 'MD5', 'NULL']):
                            findings.append({
                                'id': 'ssl_weak_cipher',
                                'type': 'vulnerability',
                                'severity': 'high',
                                'title': 'Weak Cipher Suite',
                                'description': f'Using weak cipher suite: {cipher_name}',
                                'remediation': 'Configure server to use only strong cipher suites',
                                'owasp_category': 'A02:2021 - Cryptographic Failures',
                                'location': 'SSL/TLS',
                                'evidence': {
                                    'cipher_suite': cipher_name,
                                    'cipher_version': cipher[1],
                                    'cipher_bits': cipher[2]
                                }
                            })
        except Exception:
            pass  # Cipher test failed, but not critical
        
        return findings