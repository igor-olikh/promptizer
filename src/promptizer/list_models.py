"""Utility to list available models from OpenAI and Gemini APIs."""

import asyncio
from typing import List, Dict
import google.generativeai as genai
from openai import AsyncOpenAI
from .config import Config


async def list_openai_models() -> List[Dict[str, str]]:
    """List all available OpenAI models.
    
    Returns:
        List of dictionaries with model information
    """
    try:
        Config.validate()
        client = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)
        
        models = []
        async for model in client.models.list():
            model_info = {
                "id": model.id,
                "created": str(model.created) if hasattr(model, 'created') else "N/A",
                "owned_by": model.owned_by if hasattr(model, 'owned_by') else "N/A",
            }
            models.append(model_info)
        
        return sorted(models, key=lambda x: x["id"])
    except Exception as e:
        print(f"❌ Error listing OpenAI models: {e}")
        return []


def list_gemini_models() -> List[Dict[str, str]]:
    """List all available Gemini models.
    
    Returns:
        List of dictionaries with model information
    """
    try:
        Config.validate()
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        
        models = []
        for model in genai.list_models():
            # Filter only models that support generateContent
            if 'generateContent' in model.supported_generation_methods:
                model_info = {
                    "name": model.name,
                    "display_name": model.display_name if hasattr(model, 'display_name') else model.name,
                    "supported_methods": ", ".join(model.supported_generation_methods),
                    "input_token_limit": str(model.input_token_limit) if hasattr(model, 'input_token_limit') else "N/A",
                    "output_token_limit": str(model.output_token_limit) if hasattr(model, 'output_token_limit') else "N/A",
                }
                models.append(model_info)
        
        return sorted(models, key=lambda x: x["name"])
    except Exception as e:
        print(f"❌ Error listing Gemini models: {e}")
        import traceback
        traceback.print_exc()
        return []


async def list_all_models():
    """List all available models from both providers."""
    print("=" * 80)
    print("AVAILABLE MODELS")
    print("=" * 80)
    
    # List OpenAI models
    print("\n📋 OpenAI Models:")
    print("-" * 80)
    openai_models = await list_openai_models()
    if openai_models:
        for model in openai_models:
            print(f"  • {model['id']}")
            if model.get('owned_by') and model['owned_by'] != 'N/A':
                print(f"    Owned by: {model['owned_by']}")
        print(f"\n  Total: {len(openai_models)} models")
    else:
        print("  ❌ No models found or error occurred")
    
    # List Gemini models
    print("\n📋 Gemini Models (with generateContent support):")
    print("-" * 80)
    gemini_models = list_gemini_models()
    if gemini_models:
        for model in gemini_models:
            print(f"  • {model['name']}")
            if model.get('display_name') and model['display_name'] != model['name']:
                print(f"    Display Name: {model['display_name']}")
            if model.get('supported_methods'):
                print(f"    Methods: {model['supported_methods']}")
            if model.get('input_token_limit') != 'N/A':
                print(f"    Input Tokens: {model['input_token_limit']}")
            if model.get('output_token_limit') != 'N/A':
                print(f"    Output Tokens: {model['output_token_limit']}")
            print()
        print(f"  Total: {len(gemini_models)} models")
    else:
        print("  ❌ No models found or error occurred")
    
    # Show current configuration
    print("\n" + "=" * 80)
    print("CURRENT CONFIGURATION")
    print("=" * 80)
    print(f"  OpenAI Model: {Config.OPENAI_MODEL}")
    print(f"  Gemini Model: {Config.GEMINI_MODEL}")
    
    # Check if configured models are available
    print("\n" + "=" * 80)
    print("CONFIGURATION VALIDATION")
    print("=" * 80)
    
    openai_available = any(m['id'] == Config.OPENAI_MODEL for m in openai_models)
    gemini_available = any(m['name'] == Config.GEMINI_MODEL or 
                          Config.GEMINI_MODEL in m['name'] for m in gemini_models)
    
    if openai_available:
        print(f"  ✅ OpenAI model '{Config.OPENAI_MODEL}' is available")
    else:
        print(f"  ❌ OpenAI model '{Config.OPENAI_MODEL}' is NOT available")
        if openai_models:
            print(f"     Available models: {', '.join([m['id'] for m in openai_models[:5]])}")
    
    if gemini_available:
        print(f"  ✅ Gemini model '{Config.GEMINI_MODEL}' is available")
    else:
        print(f"  ❌ Gemini model '{Config.GEMINI_MODEL}' is NOT available")
        if gemini_models:
            print(f"     Available models:")
            for m in gemini_models[:5]:
                print(f"       - {m['name']}")
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    if not openai_available and openai_models:
        print(f"  💡 Update OPENAI_MODEL in .env to one of the available models above")
    if not gemini_available and gemini_models:
        print(f"  💡 Update GEMINI_MODEL in .env to one of the available models above")
        if gemini_models:
            # Suggest the first available model
            suggested = gemini_models[0]['name']
            print(f"     Suggested: GEMINI_MODEL={suggested}")


if __name__ == "__main__":
    asyncio.run(list_all_models())

