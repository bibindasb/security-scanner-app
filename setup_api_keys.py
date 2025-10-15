#!/usr/bin/env python3
"""
Setup script to help configure API keys for the Security Scanner
"""
import os
import sys

def setup_api_keys():
    """Interactive setup for API keys"""
    print("🔑 Security Scanner API Key Setup")
    print("=" * 40)
    print()
    print("This script will help you set up your API keys for the Security Scanner.")
    print("You need at least one AI provider API key for the application to work.")
    print()
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please copy .env.example to .env first:")
        print("   cp .env.example .env")
        return False
    
    # Read current .env file
    with open('.env', 'r') as f:
        content = f.read()
    
    # Get API keys from user
    print("Enter your API keys (press Enter to skip):")
    print()
    
    # OpenRouter API Key
    openrouter_key = input("OpenRouter API Key (https://openrouter.ai/): ").strip()
    if openrouter_key and not openrouter_key.startswith('sk-or-v1-'):
        print("⚠️  Warning: OpenRouter API keys usually start with 'sk-or-v1-'")
        confirm = input("Continue anyway? (y/N): ").strip().lower()
        if confirm != 'y':
            openrouter_key = ""
    
    # Gemini API Key
    gemini_key = input("Gemini API Key (https://makersuite.google.com/app/apikey): ").strip()
    
    # OpenAI API Key
    openai_key = input("OpenAI API Key (https://platform.openai.com/api-keys): ").strip()
    if openai_key and not openai_key.startswith('sk-'):
        print("⚠️  Warning: OpenAI API keys usually start with 'sk-'")
        confirm = input("Continue anyway? (y/N): ").strip().lower()
        if confirm != 'y':
            openai_key = ""
    
    # Check if at least one key is provided
    if not any([openrouter_key, gemini_key, openai_key]):
        print("❌ No API keys provided. At least one AI provider is required.")
        return False
    
    # Update .env file
    updated_content = content
    
    if openrouter_key:
        updated_content = updated_content.replace(
            'OPENROUTE_API_KEY=sk-or-v1-your_actual_openrouter_api_key_here',
            f'OPENROUTE_API_KEY={openrouter_key}'
        )
        print("✅ OpenRouter API key updated")
    
    if gemini_key:
        updated_content = updated_content.replace(
            'GEMINI_API_KEY=your_actual_gemini_api_key_here',
            f'GEMINI_API_KEY={gemini_key}'
        )
        print("✅ Gemini API key updated")
    
    if openai_key:
        updated_content = updated_content.replace(
            'OPENAI_API_KEY=sk-your_actual_openai_api_key_here',
            f'OPENAI_API_KEY={openai_key}'
        )
        print("✅ OpenAI API key updated")
    
    # Write updated .env file
    with open('.env', 'w') as f:
        f.write(updated_content)
    
    print()
    print("🎉 API keys configured successfully!")
    print()
    print("Next steps:")
    print("1. Test your configuration: python3 standalone_test.py")
    print("2. Start the application: docker-compose up -d")
    print("3. Visit: http://localhost:3000")
    
    return True

if __name__ == "__main__":
    success = setup_api_keys()
    sys.exit(0 if success else 1)