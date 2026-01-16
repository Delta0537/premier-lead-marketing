"""
Premier Lead Marketing - Unified AI Chat
=========================================
Chat with Claude AND Gemini in one interface.
Switch between models or compare responses side-by-side.

Usage:
  python ai_chat.py

Commands:
  /claude  - Switch to Claude
  /gemini  - Switch to Gemini
  /both    - Get responses from both
  /compare - Compare responses side-by-side
  /cost    - Show token usage and costs
  /clear   - Clear conversation history
  /exit    - Exit chat
"""

import os
import sys
from datetime import datetime
from typing import Optional, Dict, List
from dataclasses import dataclass, field

# Check for required packages
try:
    import anthropic
except ImportError:
    print("Installing anthropic...")
    os.system("pip install anthropic")
    import anthropic

try:
    import google.generativeai as genai
except ImportError:
    print("Installing google-generativeai...")
    os.system("pip install google-generativeai")
    import google.generativeai as genai


# ==================== CONFIGURATION ====================

@dataclass
class Config:
    """Configuration for AI Chat."""
    ANTHROPIC_API_KEY: str = os.getenv('ANTHROPIC_API_KEY', '')
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')

    CLAUDE_MODEL: str = "claude-sonnet-4-20250514"
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"

    MAX_TOKENS: int = 4096

    # Pricing per 1M tokens
    CLAUDE_INPUT_PRICE: float = 3.00
    CLAUDE_OUTPUT_PRICE: float = 15.00
    GEMINI_INPUT_PRICE: float = 0.075  # Gemini is much cheaper
    GEMINI_OUTPUT_PRICE: float = 0.30


# ==================== TOKEN TRACKER ====================

@dataclass
class TokenTracker:
    """Track token usage and costs."""
    claude_input: int = 0
    claude_output: int = 0
    gemini_input: int = 0
    gemini_output: int = 0

    def add_claude(self, input_tokens: int, output_tokens: int):
        self.claude_input += input_tokens
        self.claude_output += output_tokens

    def add_gemini(self, input_tokens: int, output_tokens: int):
        self.gemini_input += input_tokens
        self.gemini_output += output_tokens

    def get_claude_cost(self) -> float:
        input_cost = (self.claude_input / 1_000_000) * Config.CLAUDE_INPUT_PRICE
        output_cost = (self.claude_output / 1_000_000) * Config.CLAUDE_OUTPUT_PRICE
        return input_cost + output_cost

    def get_gemini_cost(self) -> float:
        input_cost = (self.gemini_input / 1_000_000) * Config.GEMINI_INPUT_PRICE
        output_cost = (self.gemini_output / 1_000_000) * Config.GEMINI_OUTPUT_PRICE
        return input_cost + output_cost

    def get_summary(self) -> str:
        claude_cost = self.get_claude_cost()
        gemini_cost = self.get_gemini_cost()
        total_cost = claude_cost + gemini_cost

        return f"""
╔══════════════════════════════════════════════════════════════╗
║                    TOKEN USAGE & COSTS                       ║
╠══════════════════════════════════════════════════════════════╣
║  CLAUDE                                                      ║
║    Input:  {self.claude_input:>10,} tokens                              ║
║    Output: {self.claude_output:>10,} tokens                              ║
║    Cost:   ${claude_cost:>10.4f}                                    ║
╠══════════════════════════════════════════════════════════════╣
║  GEMINI                                                      ║
║    Input:  {self.gemini_input:>10,} tokens                              ║
║    Output: {self.gemini_output:>10,} tokens                              ║
║    Cost:   ${gemini_cost:>10.4f}                                    ║
╠══════════════════════════════════════════════════════════════╣
║  TOTAL COST: ${total_cost:>10.4f}                                   ║
╚══════════════════════════════════════════════════════════════╝
"""


# ==================== AI CLIENTS ====================

class ClaudeClient:
    """Claude API client."""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.conversation: List[Dict] = []

    def chat(self, message: str, tracker: TokenTracker) -> str:
        self.conversation.append({"role": "user", "content": message})

        response = self.client.messages.create(
            model=Config.CLAUDE_MODEL,
            max_tokens=Config.MAX_TOKENS,
            system="You are a helpful AI assistant. Be concise and direct.",
            messages=self.conversation
        )

        # Track tokens
        tracker.add_claude(response.usage.input_tokens, response.usage.output_tokens)

        assistant_message = response.content[0].text
        self.conversation.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    def clear(self):
        self.conversation = []


class GeminiClient:
    """Gemini API client."""

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        self.chat_session = self.model.start_chat(history=[])

    def chat(self, message: str, tracker: TokenTracker) -> str:
        response = self.chat_session.send_message(message)

        # Estimate tokens (Gemini doesn't always return exact counts)
        input_tokens = len(message.split()) * 1.3  # Rough estimate
        output_tokens = len(response.text.split()) * 1.3
        tracker.add_gemini(int(input_tokens), int(output_tokens))

        return response.text

    def clear(self):
        self.chat_session = self.model.start_chat(history=[])


# ==================== MAIN CHAT INTERFACE ====================

class UnifiedChat:
    """Unified chat interface for Claude and Gemini."""

    def __init__(self):
        self.config = Config()
        self.tracker = TokenTracker()
        self.current_model = "claude"  # Default

        # Initialize clients
        self.claude = None
        self.gemini = None

        if self.config.ANTHROPIC_API_KEY:
            try:
                self.claude = ClaudeClient(self.config.ANTHROPIC_API_KEY)
                print("[OK] Claude initialized")
            except Exception as e:
                print(f"[WARN] Claude init failed: {e}")
        else:
            print("[WARN] ANTHROPIC_API_KEY not set - Claude disabled")

        if self.config.GEMINI_API_KEY:
            try:
                self.gemini = GeminiClient(self.config.GEMINI_API_KEY)
                print("[OK] Gemini initialized")
            except Exception as e:
                print(f"[WARN] Gemini init failed: {e}")
        else:
            print("[WARN] GEMINI_API_KEY not set - Gemini disabled")

    def process_command(self, cmd: str) -> bool:
        """Process slash commands. Returns True if should continue."""
        cmd = cmd.lower().strip()

        if cmd == '/exit':
            print(self.tracker.get_summary())
            print("\nGoodbye!")
            return False

        elif cmd == '/claude':
            if self.claude:
                self.current_model = 'claude'
                print("\n[SWITCHED] Now using Claude\n")
            else:
                print("\n[ERROR] Claude not available\n")

        elif cmd == '/gemini':
            if self.gemini:
                self.current_model = 'gemini'
                print("\n[SWITCHED] Now using Gemini\n")
            else:
                print("\n[ERROR] Gemini not available\n")

        elif cmd == '/both':
            self.current_model = 'both'
            print("\n[SWITCHED] Now using BOTH models\n")

        elif cmd == '/compare':
            self.current_model = 'compare'
            print("\n[SWITCHED] Compare mode - side by side responses\n")

        elif cmd == '/cost':
            print(self.tracker.get_summary())

        elif cmd == '/clear':
            if self.claude:
                self.claude.clear()
            if self.gemini:
                self.gemini.clear()
            print("\n[CLEARED] Conversation history cleared\n")

        elif cmd == '/help':
            self.print_help()

        else:
            print(f"\n[UNKNOWN] Unknown command: {cmd}")
            print("Type /help for available commands\n")

        return True

    def print_help(self):
        print("""
╔══════════════════════════════════════════════════════════════╗
║                      AVAILABLE COMMANDS                      ║
╠══════════════════════════════════════════════════════════════╣
║  /claude   - Switch to Claude only                           ║
║  /gemini   - Switch to Gemini only                           ║
║  /both     - Get responses from both models                  ║
║  /compare  - Compare responses side-by-side                  ║
║  /cost     - Show token usage and costs                      ║
║  /clear    - Clear conversation history                      ║
║  /help     - Show this help                                  ║
║  /exit     - Exit chat                                       ║
╚══════════════════════════════════════════════════════════════╝
""")

    def chat(self, message: str) -> str:
        """Send message and get response based on current mode."""

        if self.current_model == 'claude':
            if not self.claude:
                return "[ERROR] Claude not available"
            return self.claude.chat(message, self.tracker)

        elif self.current_model == 'gemini':
            if not self.gemini:
                return "[ERROR] Gemini not available"
            return self.gemini.chat(message, self.tracker)

        elif self.current_model == 'both':
            responses = []
            if self.claude:
                try:
                    claude_resp = self.claude.chat(message, self.tracker)
                    responses.append(f"\n{'='*30} CLAUDE {'='*30}\n{claude_resp}")
                except Exception as e:
                    responses.append(f"\n{'='*30} CLAUDE {'='*30}\n[ERROR] {e}")

            if self.gemini:
                try:
                    gemini_resp = self.gemini.chat(message, self.tracker)
                    responses.append(f"\n{'='*30} GEMINI {'='*30}\n{gemini_resp}")
                except Exception as e:
                    responses.append(f"\n{'='*30} GEMINI {'='*30}\n[ERROR] {e}")

            return '\n'.join(responses)

        elif self.current_model == 'compare':
            # Side by side comparison
            claude_resp = "[Not available]"
            gemini_resp = "[Not available]"

            if self.claude:
                try:
                    claude_resp = self.claude.chat(message, self.tracker)
                except Exception as e:
                    claude_resp = f"[ERROR] {e}"

            if self.gemini:
                try:
                    gemini_resp = self.gemini.chat(message, self.tracker)
                except Exception as e:
                    gemini_resp = f"[ERROR] {e}"

            return f"""
╔══════════════════════════════════════════════════════════════╗
║                         CLAUDE                               ║
╚══════════════════════════════════════════════════════════════╝
{claude_resp}

╔══════════════════════════════════════════════════════════════╗
║                         GEMINI                               ║
╚══════════════════════════════════════════════════════════════╝
{gemini_resp}
"""

        return "[ERROR] Unknown model"

    def run(self):
        """Run the chat interface."""
        print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              Premier Lead Marketing - Unified AI Chat                         ║
║                                                                               ║
║                    Claude + Gemini in One Interface                           ║
║                                                                               ║
║         Type /help for commands | /exit to quit | /cost for usage             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
        """)

        # Show current status
        model_status = f"Current model: {self.current_model.upper()}"
        print(f"\n[STATUS] {model_status}\n")

        while True:
            try:
                # Show prompt with current model
                prompt_indicator = {
                    'claude': '🟣 Claude',
                    'gemini': '🔵 Gemini',
                    'both': '🟣🔵 Both',
                    'compare': '⚖️ Compare'
                }.get(self.current_model, self.current_model)

                user_input = input(f"\n[{prompt_indicator}] You: ").strip()

                if not user_input:
                    continue

                # Check for commands
                if user_input.startswith('/'):
                    if not self.process_command(user_input):
                        break
                    continue

                # Get response
                print("\n[Thinking...]")
                response = self.chat(user_input)
                print(f"\n{response}")

            except KeyboardInterrupt:
                print("\n\n[INFO] Use /exit to quit properly")
                continue
            except Exception as e:
                print(f"\n[ERROR] {e}")
                continue


# ==================== MAIN ====================

def main():
    """Main entry point."""

    # Check for API keys
    if not os.getenv('ANTHROPIC_API_KEY') and not os.getenv('GEMINI_API_KEY'):
        print("""
[ERROR] No API keys found!

Set at least one:
  $env:ANTHROPIC_API_KEY='your-key'
  $env:GEMINI_API_KEY='your-key'

Or permanently:
  [System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'key', 'User')
  [System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'key', 'User')
""")
        return

    chat = UnifiedChat()
    chat.run()


if __name__ == "__main__":
    main()
