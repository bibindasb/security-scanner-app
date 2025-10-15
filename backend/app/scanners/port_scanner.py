# backend/app/scanners/port_scanner.py
import asyncio
from typing import Dict, Any, List
import nmap
from .base import BaseScanner

class PortScanner(BaseScanner):
    # Common ports and their security implications
    DANGEROUS_PORTS = {
        21: {'service': 'FTP', 'severity': 'medium', 'description': 'FTP service - consider using SFTP'},
        23: {'service': 'Telnet', 'severity': 'high', 'description': 'Telnet - unencrypted remote access'},
        25: {'service': 'SMTP', 'severity': 'low', 'description': 'SMTP mail server'},
        53: {'service': 'DNS', 'severity': 'low', 'description': 'DNS service'},
        80: {'service': 'HTTP', 'severity': 'medium', 'description': 'HTTP - should redirect to HTTPS'},
        110: {'service': 'POP3', 'severity': 'medium', 'description': 'POP3 - unencrypted email'},
        143: {'service': 'IMAP', 'severity': 'medium', 'description': 'IMAP - unencrypted email'},
        443: {'service': 'HTTPS', 'severity': 'info', 'description': 'HTTPS - encrypted web traffic'},
        993: {'service': 'IMAPS', 'severity': 'info', 'description': 'IMAPS - encrypted email'},
        995: {'service': 'POP3S', 'severity': 'info', 'description': 'POP3S - encrypted email'},
        3389: {'service': 'RDP', 'severity': 'high', 'description': 'RDP - remote desktop access'},
        5432: {'service': 'PostgreSQL', 'severity': 'high', 'description': 'PostgreSQL database'},
        3306: {'service': 'MySQL', 'severity': 'high', 'description': 'MySQL database'},
        6379: {'service': 'Redis', 'severity': 'high', 'description': 'Redis database'},
        27017: {'service': 'MongoDB', 'severity': 'high', 'description': 'MongoDB database'},
        22: {'service': 'SSH', 'severity': 'medium', 'description': 'SSH - secure shell access'},
        8080: {'service': 'HTTP-Alt', 'severity': 'medium', 'description': 'Alternative HTTP port'},
        8443: {'service': 'HTTPS-Alt', 'severity': 'info', 'description': 'Alternative HTTPS port'},
        9200: {'service': 'Elasticsearch', 'severity': 'high', 'description': 'Elasticsearch database'},
        5601: {'service': 'Kibana', 'severity': 'high', 'description': 'Kibana dashboard'},
        3000: {'service': 'Node.js', 'severity': 'medium', 'description': 'Node.js development server'},
        5000: {'service': 'Flask', 'severity': 'medium', 'description': 'Flask development server'},
        8000: {'service': 'Django', 'severity': 'medium', 'description': 'Django development server'}
    }
    
    async def scan(self) -> List[Dict[str, Any]]:
        findings = []
        
        try:
            # Use asyncio to run nmap in thread pool
            loop = asyncio.get_event_loop()
            findings = await loop.run_in_executor(None, self._run_nmap_scan)
        except Exception as e:
            findings.append({
                'id': 'port_scan_error',
                'type': 'error',
                'severity': 'info',
                'title': 'Port Scan Failed',
                'description': f'Failed to scan ports: {str(e)}',
                'location': 'Network Ports'
            })
        
        return findings
    
    def _run_nmap_scan(self) -> List[Dict[str, Any]]:
        findings = []
        hostname = self.target_url.split('//')[-1].split('/')[0].split(':')[0]
        
        try:
            nm = nmap.PortScanner()
            # Comprehensive scan with service detection
            nm.scan(hostname, arguments='-sS -sV -O --script vuln --host-timeout 60s')
            
            for host in nm.all_hosts():
                host_info = nm[host]
                
                # Check if host is up
                if host_info['status']['state'] != 'up':
                    findings.append({
                        'id': 'host_down',
                        'type': 'information',
                        'severity': 'info',
                        'title': 'Host Unreachable',
                        'description': f'Host {hostname} is not responding to ping',
                        'location': 'Network'
                    })
                    continue
                
                # Analyze open ports
                open_ports = []
                for proto in host_info.all_protocols():
                    ports = host_info[proto].keys()
                    for port in ports:
                        port_info = host_info[proto][port]
                        if port_info['state'] == 'open':
                            open_ports.append(port)
                            findings.extend(self._analyze_port(port, port_info, proto))
                
                # Check for common security issues
                findings.extend(self._check_security_patterns(open_ports, host_info))
                
        except Exception as e:
            findings.append({
                'id': 'nmap_scan_error',
                'type': 'error',
                'severity': 'info',
                'title': 'Nmap Scan Failed',
                'description': f'Nmap port scan failed: {str(e)}',
                'location': 'Network Ports'
            })
        
        return findings
    
    def _analyze_port(self, port: int, port_info: dict, protocol: str) -> List[Dict[str, Any]]:
        findings = []
        
        service = port_info.get('name', 'unknown')
        product = port_info.get('product', '')
        version = port_info.get('version', '')
        extrainfo = port_info.get('extrainfo', '')
        
        # Check if port is in dangerous ports list
        if port in self.DANGEROUS_PORTS:
            port_data = self.DANGEROUS_PORTS[port]
            
            # Determine severity based on context
            severity = port_data['severity']
            if port in [5432, 3306, 6379, 27017, 9200, 5601]:  # Database ports
                if not any(secure in extrainfo.lower() for secure in ['ssl', 'tls', 'encrypted']):
                    severity = 'high'
            
            findings.append({
                'id': f'port_{port}_{service.lower()}',
                'type': 'information' if severity == 'info' else 'vulnerability',
                'severity': severity,
                'title': f'Open Port: {port}/{service}',
                'description': f'{port_data["description"]}. Service: {service} {product} {version}'.strip(),
                'remediation': self._get_port_remediation(port, service, product, version),
                'owasp_category': 'A05:2021 - Security Misconfiguration',
                'location': f'Port {port}',
                'evidence': {
                    'port': port,
                    'protocol': protocol,
                    'service': service,
                    'product': product,
                    'version': version,
                    'extrainfo': extrainfo,
                    'state': port_info['state']
                }
            })
        
        # Check for version disclosure
        if version and version != 'unknown':
            findings.append({
                'id': f'version_disclosure_{port}',
                'type': 'information_disclosure',
                'severity': 'low',
                'title': f'Version Disclosure on Port {port}',
                'description': f'Service version disclosed: {service} {product} {version}',
                'remediation': 'Disable or obfuscate version information in service banners',
                'owasp_category': 'A05:2021 - Security Misconfiguration',
                'location': f'Port {port}',
                'evidence': {
                    'port': port,
                    'service': service,
                    'version': version,
                    'product': product
                }
            })
        
        return findings
    
    def _get_port_remediation(self, port: int, service: str, product: str, version: str) -> str:
        """Get specific remediation advice for a port"""
        if port in [21, 23]:
            return 'Disable unencrypted protocols and use encrypted alternatives (SFTP, SSH)'
        elif port in [25, 110, 143]:
            return 'Ensure email services use encryption (SMTPS, IMAPS, POP3S)'
        elif port == 80:
            return 'Redirect HTTP to HTTPS and implement HSTS'
        elif port in [5432, 3306, 6379, 27017, 9200]:
            return 'Ensure database is not exposed to the internet, use VPN or private networks'
        elif port == 3389:
            return 'Secure RDP with strong authentication, consider VPN access only'
        elif port in [3000, 5000, 8000]:
            return 'Development servers should not be exposed in production'
        else:
            return f'Review necessity of exposing port {port} and implement proper security controls'
    
    def _check_security_patterns(self, open_ports: List[int], host_info: dict) -> List[Dict[str, Any]]:
        findings = []
        
        # Check for common insecure configurations
        if 80 in open_ports and 443 not in open_ports:
            findings.append({
                'id': 'http_without_https',
                'type': 'vulnerability',
                'severity': 'high',
                'title': 'HTTP Without HTTPS',
                'description': 'HTTP port 80 is open but HTTPS port 443 is not available',
                'remediation': 'Enable HTTPS and redirect HTTP traffic to HTTPS',
                'owasp_category': 'A02:2021 - Cryptographic Failures',
                'location': 'Network Ports'
            })
        
        # Check for database exposure
        db_ports = [5432, 3306, 6379, 27017, 9200, 5601]
        exposed_db_ports = [port for port in open_ports if port in db_ports]
        if exposed_db_ports:
            findings.append({
                'id': 'database_exposure',
                'type': 'vulnerability',
                'severity': 'critical',
                'title': 'Database Ports Exposed',
                'description': f'Database ports exposed to internet: {exposed_db_ports}',
                'remediation': 'Move databases to private networks and use VPN or bastion hosts for access',
                'owasp_category': 'A05:2021 - Security Misconfiguration',
                'location': 'Network Ports',
                'evidence': {
                    'exposed_ports': exposed_db_ports
                }
            })
        
        # Check for development servers in production
        dev_ports = [3000, 5000, 8000, 8080]
        exposed_dev_ports = [port for port in open_ports if port in dev_ports]
        if exposed_dev_ports:
            findings.append({
                'id': 'development_servers_exposed',
                'type': 'vulnerability',
                'severity': 'medium',
                'title': 'Development Servers Exposed',
                'description': f'Development server ports exposed: {exposed_dev_ports}',
                'remediation': 'Remove development servers from production environment',
                'owasp_category': 'A05:2021 - Security Misconfiguration',
                'location': 'Network Ports',
                'evidence': {
                    'exposed_ports': exposed_dev_ports
                }
            })
        
        return findings