# backend/app/scanners/port_scanner.py
import asyncio
from typing import Dict, Any, List
import nmap
from .base import BaseScanner

class PortScanner(BaseScanner):
    async def scan(self) -> List[Dict[str, Any]]:
        findings = []
        
        try:
            # Use asyncio to run nmap in thread pool
            loop = asyncio.get_event_loop()
            findings = await loop.run_in_executor(None, self._run_nmap_scan)
        except Exception as e:
            findings.append({
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
            # Quick scan of common ports
            nm.scan(hostname, arguments='-F --host-timeout 30s')
            
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    for port in ports:
                        state = nm[host][proto][port]['state']
                        if state == 'open':
                            service = nm[host][proto][port].get('name', 'unknown')
                            findings.append({
                                'type': 'information',
                                'severity': 'info',
                                'title': f'Open Port Found: {port}/{service}',
                                'description': f'Port {port} ({service}) is {state}.',
                                'remediation': f'Ensure port {port} is properly secured or closed if not needed.',
                                'location': f'Port {port}',
                                'evidence': {
                                    'protocol': proto,
                                    'service': service,
                                    'state': state
                                }
                            })
        except Exception as e:
            findings.append({
                'type': 'error',
                'severity': 'info',
                'title': 'Nmap Scan Failed',
                'description': f'Nmap port scan failed: {str(e)}',
                'location': 'Network Ports'
            })
        
        return findings