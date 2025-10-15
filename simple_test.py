#!/usr/bin/env python3
"""
Simple test to verify the AI providers work correctly
"""
import asyncio
import json
import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

async def test_openrouter_provider():
    """Test OpenRouter provider directly"""
    print("🧪 Testing OpenRouter Provider...")
    
    try:
        from app.ai.openrouter_provider import OpenRouterProvider
        
        # Check if API key is available
        api_key = os.getenv('OPENROUTE_API_KEY')
        if not api_key:
            print("❌ OPENROUTE_API_KEY not set")
            return False
        
        provider = OpenRouterProvider(api_key=api_key)
        
        # Test with mock findings
        mock_findings = [
            {
                "id": "test_finding",
                "type": "vulnerability",
                "severity": "high",
                "title": "Test Security Issue",
                "description": "This is a test finding for AI analysis"
            }
        ]
        
        print("🤖 Running OpenRouter analysis...")
        result = await provider.analyze_findings(mock_findings)
        
        if 'error' in result:
            print(f"⚠️  OpenRouter returned error: {result['error']}")
            return False
        
        print("✅ OpenRouter test completed successfully!")
        print(f"📊 Summary: {result.get('summary', 'N/A')[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ OpenRouter test failed: {str(e)}")
        return False

async def test_gemini_provider():
    """Test Gemini provider directly"""
    print("\n🧪 Testing Gemini Provider...")
    
    try:
        from app.ai.gemini_provider import GeminiProvider
        
        # Check if API key is available
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY not set")
            return False
        
        provider = GeminiProvider(api_key=api_key)
        
        # Test with mock findings
        mock_findings = [
            {
                "id": "test_finding",
                "type": "vulnerability",
                "severity": "high",
                "title": "Test Security Issue",
                "description": "This is a test finding for AI analysis"
            }
        ]
        
        print("🤖 Running Gemini analysis...")
        result = await provider.analyze_findings(mock_findings)
        
        if 'error' in result:
            print(f"⚠️  Gemini returned error: {result['error']}")
            return False
        
        print("✅ Gemini test completed successfully!")
        print(f"📊 Summary: {result.get('summary', 'N/A')[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Gemini test failed: {str(e)}")
        return False

def test_scanner_imports():
    """Test that scanner modules can be imported"""
    print("\n🧪 Testing Scanner Imports...")
    
    try:
        from app.scanners.headers_scanner import HeadersScanner
        from app.scanners.ssl_scanner import SSLScanner
        from app.scanners.port_scanner import PortScanner
        from app.scanners.scanner_manager import ScannerManager
        
        print("✅ All scanner modules imported successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Scanner import test failed: {str(e)}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n🧪 Testing Configuration...")
    
    try:
        from app.config import settings
        
        print(f"📋 Database URL: {settings.DATABASE_URL}")
        print(f"📋 Redis URL: {settings.REDIS_URL}")
        print(f"📋 OpenRouter API Key: {'Set' if settings.OPENROUTE_API_KEY else 'Not set'}")
        print(f"📋 Gemini API Key: {'Set' if settings.GEMINI_API_KEY else 'Not set'}")
        
        print("✅ Configuration loaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {str(e)}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Security Scanner Simple Test")
    print("=" * 50)
    
    # Test configuration
    config_success = test_configuration()
    
    # Test scanner imports
    scanner_success = test_scanner_imports()
    
    # Test AI providers (only if API keys are available)
    openrouter_success = await test_openrouter_provider()
    gemini_success = await test_gemini_provider()
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    print(f"   Configuration: {'✅ PASS' if config_success else '❌ FAIL'}")
    print(f"   Scanner Imports: {'✅ PASS' if scanner_success else '❌ FAIL'}")
    print(f"   OpenRouter: {'✅ PASS' if openrouter_success else '❌ FAIL'}")
    print(f"   Gemini: {'✅ PASS' if gemini_success else '❌ FAIL'}")
    
    # Overall success if core components work
    core_success = config_success and scanner_success
    ai_success = openrouter_success or gemini_success
    
    if core_success:
        print("\n🎉 Core functionality is working!")
        if ai_success:
            print("🤖 AI integration is also working!")
        else:
            print("⚠️  AI integration needs API keys to work")
        return True
    else:
        print("\n❌ Core functionality has issues")
        return False

if __name__ == "__main__":
    # Load environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    # Set up environment for testing
    os.environ.setdefault("OPENROUTE_API_KEY", "")
    os.environ.setdefault("GEMINI_API_KEY", "")
    
    success = asyncio.run(main())
    sys.exit(0 if success else 1)