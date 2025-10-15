#!/usr/bin/env python3
"""
Test script for the security scanner AI integration
"""
import asyncio
import os
import sys
import json
from pathlib import Path

# Add the backend directory to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.ai.manager import AIManager
from app.scanners.scanner_manager import ScannerManager

async def test_ai_integration():
    """Test AI integration with mock findings"""
    print("🧪 Testing AI Integration...")
    
    # Mock findings data
    mock_findings = [
        {
            "id": "header_csp_missing",
            "type": "misconfiguration",
            "severity": "high",
            "title": "Missing Security Header: Content-Security-Policy",
            "description": "The Content-Security-Policy security header is missing.",
            "remediation": "Configure the Content-Security-Policy header appropriately.",
            "owasp_category": "A05:2021 - Security Misconfiguration",
            "location": "HTTP Headers"
        },
        {
            "id": "ssl_weak_protocols",
            "type": "vulnerability",
            "severity": "high",
            "title": "Weak TLS Protocol Versions",
            "description": "Server supports deprecated TLS versions: TLSv1, TLSv1.1",
            "remediation": "Disable TLSv1 and TLSv1.1, use only TLSv1.2 or higher",
            "owasp_category": "A02:2021 - Cryptographic Failures",
            "location": "SSL/TLS"
        }
    ]
    
    # Initialize AI manager
    ai_manager = AIManager()
    
    print(f"📋 Available providers: {ai_manager.get_available_providers()}")
    
    if not ai_manager.get_available_providers():
        print("❌ No AI providers available. Please set API keys:")
        print("   - OPENROUTE_API_KEY for OpenRouter")
        print("   - GEMINI_API_KEY for Gemini")
        return False
    
    # Test AI analysis
    try:
        print("🤖 Running AI analysis...")
        analysis = await ai_manager.analyze_scan(mock_findings)
        
        print("✅ AI Analysis completed!")
        print(f"📊 Summary: {analysis.get('summary', 'N/A')}")
        print(f"🎯 Risk Score: {analysis.get('risk_score', 'N/A')}")
        print(f"🔧 Remediation Steps: {len(analysis.get('prioritized_remediation', []))}")
        print(f"💡 Recommendations: {len(analysis.get('additional_recommendations', []))}")
        
        if 'error' in analysis:
            print(f"⚠️  Warning: {analysis['error']}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI analysis failed: {str(e)}")
        return False

async def test_scanner_improvements():
    """Test enhanced scanner functionality"""
    print("\n🔍 Testing Enhanced Scanners...")
    
    # Test with a sample URL
    test_url = "https://httpbin.org"  # Safe test URL
    
    try:
        scanner_manager = ScannerManager(test_url)
        print(f"🎯 Scanning: {test_url}")
        
        # Run all scans
        findings = await scanner_manager.run_all_scans()
        
        print(f"✅ Scan completed! Found {len(findings)} issues")
        
        # Categorize findings
        by_severity = {}
        by_type = {}
        
        for finding in findings:
            severity = finding.get('severity', 'unknown')
            finding_type = finding.get('type', 'unknown')
            
            by_severity[severity] = by_severity.get(severity, 0) + 1
            by_type[finding_type] = by_type.get(finding_type, 0) + 1
        
        print("📊 Findings by severity:")
        for severity, count in by_severity.items():
            print(f"   {severity}: {count}")
        
        print("📊 Findings by type:")
        for finding_type, count in by_type.items():
            print(f"   {finding_type}: {count}")
        
        # Show sample findings
        print("\n🔍 Sample findings:")
        for i, finding in enumerate(findings[:3]):  # Show first 3
            print(f"   {i+1}. [{finding.get('severity', 'unknown').upper()}] {finding.get('title', 'No title')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Scanner test failed: {str(e)}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Security Scanner Integration Test")
    print("=" * 50)
    
    # Test AI integration
    ai_success = await test_ai_integration()
    
    # Test scanner improvements
    scanner_success = await test_scanner_improvements()
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    print(f"   AI Integration: {'✅ PASS' if ai_success else '❌ FAIL'}")
    print(f"   Scanner Improvements: {'✅ PASS' if scanner_success else '❌ FAIL'}")
    
    if ai_success and scanner_success:
        print("\n🎉 All tests passed! The integration is working correctly.")
        return True
    else:
        print("\n⚠️  Some tests failed. Please check the configuration.")
        return False

if __name__ == "__main__":
    # Set up environment for testing
    os.environ.setdefault("OPENROUTE_API_KEY", "")
    os.environ.setdefault("GEMINI_API_KEY", "")
    
    success = asyncio.run(main())
    sys.exit(0 if success else 1)