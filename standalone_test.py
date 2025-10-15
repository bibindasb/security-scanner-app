#!/usr/bin/env python3
"""
Standalone test for AI providers without full application dependencies
"""
import asyncio
import json
import os
import sys

async def test_openrouter_standalone():
    """Test OpenRouter API directly"""
    print("🧪 Testing OpenRouter API...")
    
    try:
        import httpx
        
        api_key = os.getenv('OPENROUTE_API_KEY')
        if not api_key:
            print("❌ OPENROUTE_API_KEY not set")
            return False
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://security-scanner.app",
            "X-Title": "Security Scanner"
        }
        
        prompt = """
        Analyze these security findings and provide remediation steps in JSON format:
        
        [
            {
                "id": "test_finding",
                "type": "vulnerability", 
                "severity": "high",
                "title": "Missing Security Header",
                "description": "Content-Security-Policy header is missing"
            }
        ]
        
        Respond with JSON containing summary, prioritized_remediation, and additional_recommendations.
        """
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": "meta-llama/llama-2-70b-chat",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a cybersecurity expert. Provide JSON responses only."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.3,
                    "max_tokens": 1000
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data["choices"][0]["message"]["content"]
                print("✅ OpenRouter API test successful!")
                print(f"📊 Response: {ai_response[:200]}...")
                return True
            else:
                print(f"❌ OpenRouter API error: {response.status_code} - {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ OpenRouter test failed: {str(e)}")
        return False

async def test_gemini_standalone():
    """Test Gemini API directly"""
    print("\n🧪 Testing Gemini API...")
    
    try:
        import httpx
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY not set")
            return False
        
        prompt = """
        Analyze these security findings and provide remediation steps in JSON format:
        
        [
            {
                "id": "test_finding",
                "type": "vulnerability",
                "severity": "high", 
                "title": "Missing Security Header",
                "description": "Content-Security-Policy header is missing"
            }
        ]
        
        Respond with JSON containing summary, prioritized_remediation, and additional_recommendations.
        """
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}",
                json={
                    "contents": [{
                        "parts": [{
                            "text": prompt
                        }]
                    }],
                    "generationConfig": {
                        "temperature": 0.3,
                        "maxOutputTokens": 1000
                    }
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if "candidates" in data and data["candidates"]:
                    ai_response = data["candidates"][0]["content"]["parts"][0]["text"]
                    print("✅ Gemini API test successful!")
                    print(f"📊 Response: {ai_response[:200]}...")
                    return True
                else:
                    print(f"❌ Gemini API error: No candidates in response")
                    return False
            else:
                print(f"❌ Gemini API error: {response.status_code} - {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Gemini test failed: {str(e)}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\n🧪 Testing File Structure...")
    
    required_files = [
        "backend/app/ai/openrouter_provider.py",
        "backend/app/ai/gemini_provider.py", 
        "backend/app/ai/manager.py",
        "backend/app/scanners/headers_scanner.py",
        "backend/app/scanners/ssl_scanner.py",
        "backend/app/scanners/port_scanner.py",
        "backend/app/api/ai.py",
        "backend/app/config.py",
        "docker-compose.yml",
        "README.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files exist!")
        return True

def test_docker_config():
    """Test Docker configuration"""
    print("\n🧪 Testing Docker Configuration...")
    
    try:
        with open("docker-compose.yml", "r") as f:
            content = f.read()
        
        # Check that Ollama is removed
        if "ollama" in content:
            print("❌ Ollama service still present in docker-compose.yml")
            return False
        
        # Check that new environment variables are present
        if "OPENROUTE_API_KEY" not in content:
            print("❌ OPENROUTE_API_KEY not found in docker-compose.yml")
            return False
        
        if "GEMINI_API_KEY" not in content:
            print("❌ GEMINI_API_KEY not found in docker-compose.yml")
            return False
        
        print("✅ Docker configuration looks good!")
        return True
        
    except Exception as e:
        print(f"❌ Docker config test failed: {str(e)}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Security Scanner Standalone Test")
    print("=" * 50)
    
    # Test file structure
    files_success = test_file_structure()
    
    # Test Docker configuration
    docker_success = test_docker_config()
    
    # Test AI providers (only if API keys are available)
    openrouter_success = await test_openrouter_standalone()
    gemini_success = await test_gemini_standalone()
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    print(f"   File Structure: {'✅ PASS' if files_success else '❌ FAIL'}")
    print(f"   Docker Config: {'✅ PASS' if docker_success else '❌ FAIL'}")
    print(f"   OpenRouter API: {'✅ PASS' if openrouter_success else '❌ FAIL'}")
    print(f"   Gemini API: {'✅ PASS' if gemini_success else '❌ FAIL'}")
    
    # Overall success
    core_success = files_success and docker_success
    ai_success = openrouter_success or gemini_success
    
    if core_success:
        print("\n🎉 Core setup is complete!")
        if ai_success:
            print("🤖 AI integration is working!")
        else:
            print("⚠️  AI integration needs API keys to work")
        print("\n📋 Next steps:")
        print("   1. Set up your API keys in .env file")
        print("   2. Run: docker-compose up -d")
        print("   3. Visit: http://localhost:3000")
        return True
    else:
        print("\n❌ Setup has issues that need to be fixed")
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