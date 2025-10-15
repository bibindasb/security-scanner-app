# backend/app/scanners/scanner_manager.py
import asyncio
from typing import List, Dict, Any
from .headers_scanner import HeadersScanner
from .ssl_scanner import SSLScanner
from .port_scanner import PortScanner

class ScannerManager:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.scanners = [
            HeadersScanner(target_url),
            SSLScanner(target_url),
            PortScanner(target_url),
        ]
    
    async def run_all_scans(self) -> List[Dict[str, Any]]:
        all_findings = []
        
        # Run all scanners concurrently
        tasks = [scanner.scan() for scanner in self.scanners]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Handle scanner errors
                all_findings.append({
                    'type': 'error',
                    'severity': 'info',
                    'title': f'Scanner {type(self.scanners[i]).__name__} Failed',
                    'description': f'Scanner error: {str(result)}',
                    'location': 'Scanner'
                })
            else:
                all_findings.extend(result)
        
        return all_findings
    
    async def run_specific_scans(self, scan_types: List[str]) -> List[Dict[str, Any]]:
        scanner_map = {
            'headers': HeadersScanner,
            'ssl': SSLScanner,
            'ports': PortScanner,
        }
        
        selected_scanners = []
        for scan_type in scan_types:
            if scan_type in scanner_map:
                selected_scanners.append(scanner_map[scan_type](self.target_url))
        
        self.scanners = selected_scanners
        return await self.run_all_scans()