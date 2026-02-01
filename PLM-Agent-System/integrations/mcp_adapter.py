#!/usr/bin/env python3
"""
MCP Adapter - Connects PLM Orchestrator to OpenAI, Anthropic, and Google APIs
This adapter uses the same API keys configured for Cursor MCP agents
"""

import os
import asyncio
from typing import Dict, Optional, Any
import time

# Try importing API clients (install if needed)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("[WARNING] openai package not installed. Install with: pip install openai")

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("[WARNING] anthropic package not installed. Install with: pip install anthropic")

# Try new google-genai package first, then fallback to deprecated one
GENAI_NEW = False
try:
    from google import genai as genai_new
    GEMINI_AVAILABLE = True
    GENAI_NEW = True
except ImportError:
    try:
        import google.generativeai as genai
        GEMINI_AVAILABLE = True
        print("[WARNING] Using deprecated google.generativeai - consider: pip install google-genai")
    except ImportError:
        GEMINI_AVAILABLE = False
        print("[WARNING] google-genai package not installed. Install with: pip install google-genai")


class MCPAdapter:
    """Adapter to connect PLM Orchestrator with actual AI APIs"""
    
    def __init__(self):
        self.claude_client = None
        self.chatgpt_client = None
        self.gemini_client = None
        self.initialize_clients()
    
    def initialize_clients(self):
        """Initialize API clients from environment variables

        Key Priority (PLM-specific keys first, then general):
        - PLM_ANTHROPIC_API_KEY -> ANTHROPIC_API_KEY
        - PLM_GEMINI_API_KEY -> GEMINI_API_KEY
        - PLM_OPENAI_API_KEY -> OPENAI_API_KEY
        """

        # Initialize Claude (Anthropic) - Check PLM key first, then general
        if ANTHROPIC_AVAILABLE:
            # PLM key for heavy branding work, general key for other use
            PLM_KEY = 'YOUR_PLM_ANTHROPIC_API_KEY_HERE'
            GENERAL_KEY = 'YOUR_ANTHROPIC_API_KEY_HERE'
            api_key = os.getenv('PLM_ANTHROPIC_API_KEY') or os.getenv('ANTHROPIC_API_KEY') or PLM_KEY
            if api_key:
                try:
                    self.claude_client = anthropic.Anthropic(api_key=api_key)
                    key_source = "PLM_ANTHROPIC_API_KEY" if os.getenv('PLM_ANTHROPIC_API_KEY') else ("ANTHROPIC_API_KEY" if os.getenv('ANTHROPIC_API_KEY') else "hardcoded")
                    print(f"[OK] Claude API client initialized (using {key_source})")
                except Exception as e:
                    print(f"[WARNING] Failed to initialize Claude client: {e}")
            else:
                print("[WARNING] No Anthropic API key found (checked PLM_ANTHROPIC_API_KEY, ANTHROPIC_API_KEY)")
        else:
            print("[WARNING] anthropic package not available")
        
        # Initialize ChatGPT (OpenAI) - Check PLM key first, then general
        if OPENAI_AVAILABLE:
            api_key = os.getenv('PLM_OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY')
            if api_key:
                try:
                    # Workaround for httpx proxy compatibility issue
                    # Try normal initialization first
                    try:
                        self.chatgpt_client = openai.OpenAI(api_key=api_key)
                    except TypeError as proxy_error:
                        if "proxies" in str(proxy_error):
                            # Create custom httpx client without proxies to avoid compatibility issue
                            import httpx
                            http_client = httpx.Client()
                            self.chatgpt_client = openai.OpenAI(
                                api_key=api_key,
                                http_client=http_client
                            )
                        else:
                            raise
                    key_source = "PLM_OPENAI_API_KEY" if os.getenv('PLM_OPENAI_API_KEY') else "OPENAI_API_KEY"
                    print(f"[OK] ChatGPT API client initialized (using {key_source})")
                except Exception as e:
                    print(f"[WARNING] Failed to initialize ChatGPT client: {e}")
                    print("[INFO] ChatGPT will use fallback/mock responses")
            else:
                print("[WARNING] No OpenAI API key found (checked PLM_OPENAI_API_KEY, OPENAI_API_KEY)")
        else:
            print("[WARNING] openai package not available")
        
        # Initialize Gemini (Google) - Check PLM key first, then general, then hardcoded fallback
        if GEMINI_AVAILABLE:
            api_key = os.getenv('PLM_GEMINI_API_KEY') or os.getenv('GEMINI_API_KEY') or 'AIzaSyADUfdebyiEiPkYMCvITRKjPzT1nA_hkgw'
            if api_key:
                try:
                    if GENAI_NEW:
                        # Use new google-genai package
                        self.gemini_client = genai_new.Client(api_key=api_key)
                        self.gemini_model = 'gemini-2.5-flash'
                        self.gemini_vision_client = self.gemini_client  # 2.5 Flash supports vision
                        key_source = "PLM_GEMINI_API_KEY" if os.getenv('PLM_GEMINI_API_KEY') else ("GEMINI_API_KEY" if os.getenv('GEMINI_API_KEY') else "hardcoded")
                        print(f"[OK] Gemini API client initialized (google-genai, gemini-2.5-flash, using {key_source})")
                    else:
                        # Use deprecated package
                        genai.configure(api_key=api_key)
                        key_source = "PLM_GEMINI_API_KEY" if os.getenv('PLM_GEMINI_API_KEY') else ("GEMINI_API_KEY" if os.getenv('GEMINI_API_KEY') else "hardcoded")
                        try:
                            self.gemini_client = genai.GenerativeModel('gemini-2.5-flash')
                            self.gemini_vision_client = self.gemini_client
                            print(f"[OK] Gemini API client initialized (gemini-2.5-flash, using {key_source})")
                        except Exception as e1:
                            try:
                                self.gemini_client = genai.GenerativeModel('gemini-2.0-flash')
                                self.gemini_vision_client = self.gemini_client
                                print(f"[OK] Gemini API client initialized (gemini-2.0-flash, using {key_source})")
                            except Exception as e2:
                                self.gemini_client = genai.GenerativeModel('gemini-pro')
                                self.gemini_vision_client = None
                                print(f"[!] Gemini Flash unavailable, using gemini-pro: {e1}, {e2}")
                except Exception as e:
                    print(f"[WARNING] Failed to initialize Gemini client: {e}")
            else:
                print("[WARNING] No Gemini API key found (checked PLM_GEMINI_API_KEY, GEMINI_API_KEY)")
        else:
            print("[WARNING] google-genai package not available")
    
    async def call_claude(self, prompt: str, model: str = "claude-sonnet-3-5-haiku-20241022", image_path: str = None) -> Dict:
        """Call Claude API via Anthropic - DEFAULT: Haiku (12x cheaper than Sonnet 4). Use Sonnet 4 only for complex tasks. Supports vision API"""
        if not self.claude_client:
            return {
                "response": "Claude client not initialized. Check ANTHROPIC_API_KEY.",
                "error": "client_not_initialized",
                "tokens_used": 0,
                "processing_time": 0
            }
        
        try:
            start_time = time.time()
            
            # Build message content
            message_content = prompt
            
            # If image provided, add it to message (Claude vision API)
            if image_path and os.path.exists(image_path):
                try:
                    # Read image as base64 for Claude API
                    import base64
                    with open(image_path, 'rb') as image_file:
                        image_data = base64.b64encode(image_file.read()).decode('utf-8')
                    
                    # Determine image media type
                    ext = os.path.splitext(image_path)[1].lower()
                    media_type_map = {
                        '.jpg': 'image/jpeg',
                        '.jpeg': 'image/jpeg',
                        '.png': 'image/png',
                        '.gif': 'image/gif',
                        '.webp': 'image/webp'
                    }
                    media_type = media_type_map.get(ext, 'image/jpeg')
                    
                    # Use Claude Haiku (flash) for vision - cheaper and faster than Sonnet 4
                    vision_model = "claude-sonnet-3-5-haiku-20241022"  # Flash version - cheaper for vision
                    
                    # Create message with image
                    message = self.claude_client.messages.create(
                        model=vision_model,  # Use Haiku (flash) for vision
                        max_tokens=4096,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image",
                                        "source": {
                                            "type": "base64",
                                            "media_type": media_type,
                                            "data": image_data
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": prompt
                                    }
                                ]
                            }
                        ]
                    )
                    print(f"[OK] Analyzed logo image using Claude Haiku (flash) vision: {os.path.basename(image_path)}")
                except Exception as e:
                    print(f"[!] Claude vision API failed: {e} - using text-only")
                    # Fall back to text-only
                    message = self.claude_client.messages.create(
                        model=model,
                        max_tokens=4096,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
            else:
                # Text-only message
                message = self.claude_client.messages.create(
                    model=model,
                    max_tokens=4096,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
            
            processing_time = time.time() - start_time
            
            response_text = message.content[0].text if message.content else ""
            input_tokens = message.usage.input_tokens if hasattr(message, 'usage') else 0
            output_tokens = message.usage.output_tokens if hasattr(message, 'usage') else 0
            
            return {
                "response": response_text,
                "confidence": 0.95,
                "tokens_used": input_tokens + output_tokens,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "processing_time": processing_time,
                "model": model
            }
        except Exception as e:
            return {
                "response": f"Error calling Claude: {str(e)}",
                "error": str(e),
                "tokens_used": 0,
                "processing_time": 0
            }
    
    async def call_chatgpt(self, prompt: str, model: str = "gpt-4") -> Dict:
        """Call ChatGPT API via OpenAI - Using GPT-4 (not Turbo) for cost optimization"""
        if not self.chatgpt_client:
            return {
                "response": "ChatGPT client not initialized. Check OPENAI_API_KEY.",
                "error": "client_not_initialized",
                "tokens_used": 0,
                "processing_time": 0
            }
        
        try:
            start_time = time.time()
            
            response = self.chatgpt_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4096
            )
            
            processing_time = time.time() - start_time
            
            response_text = response.choices[0].message.content if response.choices else ""
            tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else 0
            
            return {
                "response": response_text,
                "confidence": 0.95,
                "tokens_used": tokens_used,
                "processing_time": processing_time,
                "model": model
            }
        except Exception as e:
            return {
                "response": f"Error calling ChatGPT: {str(e)}",
                "error": str(e),
                "tokens_used": 0,
                "processing_time": 0
            }
    
    async def call_gemini(self, prompt: str, model: str = "gemini-2.5-flash", image_path: str = None) -> Dict:
        """Call Gemini API via Google - Using Gemini 2.5 Flash (latest model with vision support)"""
        if not self.gemini_client:
            return {
                "response": "Gemini client not initialized. Check GEMINI_API_KEY.",
                "error": "client_not_initialized",
                "tokens_used": 0,
                "processing_time": 0
            }

        try:
            start_time = time.time()

            if GENAI_NEW:
                # New google-genai package
                contents = prompt

                # If image provided, add it to contents
                if image_path and os.path.exists(image_path):
                    try:
                        import base64
                        with open(image_path, 'rb') as f:
                            image_data = base64.b64encode(f.read()).decode('utf-8')

                        ext = os.path.splitext(image_path)[1].lower()
                        mime_types = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.gif': 'image/gif', '.webp': 'image/webp'}
                        mime_type = mime_types.get(ext, 'image/jpeg')

                        contents = [
                            {"text": prompt},
                            {"inline_data": {"mime_type": mime_type, "data": image_data}}
                        ]
                        print(f"[OK] Analyzing image with Gemini 2.5 Flash: {os.path.basename(image_path)}")
                    except Exception as e:
                        print(f"[!] Could not load image: {e}")

                response = self.gemini_client.models.generate_content(
                    model=self.gemini_model,
                    contents=contents
                )
                response_text = response.text if response.text else ""

                # Get token counts if available
                tokens_used = 0
                if hasattr(response, 'usage_metadata') and response.usage_metadata:
                    tokens_used = (response.usage_metadata.prompt_token_count or 0) + (response.usage_metadata.candidates_token_count or 0)
                else:
                    tokens_used = len(prompt.split()) + len(response_text.split())

            else:
                # Old deprecated package
                if image_path and os.path.exists(image_path):
                    try:
                        import PIL.Image
                        img = PIL.Image.open(image_path)
                        response = self.gemini_client.generate_content([prompt, img])
                        print(f"[OK] Analyzed logo using Gemini: {os.path.basename(image_path)}")
                    except ImportError:
                        print("[!] PIL/Pillow not installed")
                        response = self.gemini_client.generate_content(prompt)
                    except Exception as e:
                        error_msg = str(e)
                        if "429" in error_msg or "quota" in error_msg.lower():
                            print(f"[!] Gemini quota exceeded: {e}")
                            return await self.call_claude(prompt, model="claude-sonnet-3-5-haiku-20241022", image_path=image_path)
                        response = self.gemini_client.generate_content(prompt)
                else:
                    response = self.gemini_client.generate_content(prompt)

                response_text = response.text if response.text else ""
                tokens_used = len(prompt.split()) + len(response_text.split())

            processing_time = time.time() - start_time

            return {
                "response": response_text,
                "confidence": 0.95,
                "tokens_used": tokens_used,
                "processing_time": processing_time,
                "model": model,
                "image_analyzed": image_path if image_path and os.path.exists(image_path) else None
            }
        except Exception as e:
            error_msg = str(e)
            # Handle quota errors gracefully
            if "429" in error_msg or "quota" in error_msg.lower() or "RESOURCE_EXHAUSTED" in error_msg:
                return {
                    "response": f"Gemini quota exceeded. Please wait or get a new API key from https://aistudio.google.com/apikey",
                    "error": "quota_exceeded",
                    "tokens_used": 0,
                    "processing_time": 0
                }
            return {
                "response": f"Error calling Gemini: {str(e)}",
                "error": str(e),
                "tokens_used": 0,
                "processing_time": 0
            }
    
    async def call_agent(self, agent_name: str, prompt: str) -> Dict:
        """Unified interface to call any agent"""
        agent_name_lower = agent_name.lower()
        
        if agent_name_lower in ["claude", "anthropic"]:
            return await self.call_claude(prompt)
        elif agent_name_lower in ["chatgpt", "openai", "gpt"]:
            return await self.call_chatgpt(prompt)
        elif agent_name_lower in ["gemini", "google"]:
            return await self.call_gemini(prompt)
        else:
            return {
                "response": f"Unknown agent: {agent_name}. Use 'claude', 'chatgpt', or 'gemini'.",
                "error": "unknown_agent",
                "tokens_used": 0,
                "processing_time": 0
            }


# Global adapter instance
_adapter_instance = None

def get_mcp_adapter() -> MCPAdapter:
    """Get or create global MCP adapter instance"""
    global _adapter_instance
    if _adapter_instance is None:
        _adapter_instance = MCPAdapter()
    return _adapter_instance
