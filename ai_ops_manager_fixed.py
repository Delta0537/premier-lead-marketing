"""
Premier Lead Marketing - AI Operations & Business Development Manager
=====================================================================

An intelligent AI agent that functions as your Operations and Business Development Manager,
handling documentation, CRM analysis, market research, cost control, and strategic planning.

Core Capabilities:
- Document & SOP Generation
- GHL CRM Analysis & Recommendations
- Market Research & Trend Analysis
- Cost Control & Financial Tracking
- Go-to-Market Strategy
- Competitive Intelligence
- Resource Planning

Version: 1.1.0 - Fixed edition with pagination, rate limiting, logging, and token tracking
"""

import os
import sys
import json
import requests
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import anthropic
from dataclasses import dataclass, asdict, field


# ==================== LOGGING SETUP ====================

def setup_logging(log_dir: Path = None) -> logging.Logger:
    """Configure logging with file and console handlers."""
    if log_dir is None:
        log_dir = Path(os.getenv('AI_OPS_LOG_DIR', Path.home() / 'DigitalMarketing' / 'logs'))

    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"ai_ops_{datetime.now().strftime('%Y%m%d')}.log"

    # Create logger
    logger = logging.getLogger('AIOperationsManager')
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # File handler - detailed logs
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # Console handler - info and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Initialize logger
logger = setup_logging()


# ==================== TOKEN TRACKER ====================

@dataclass
class TokenUsage:
    """Track API token usage and costs."""
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    estimated_cost: float = 0.0
    api_calls: int = 0

    # Pricing per 1M tokens (Claude Sonnet 4)
    INPUT_PRICE_PER_M: float = 3.00
    OUTPUT_PRICE_PER_M: float = 15.00

    def add_usage(self, input_tokens: int, output_tokens: int):
        """Add token usage from an API call."""
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.total_tokens += input_tokens + output_tokens
        self.api_calls += 1

        # Calculate cost
        input_cost = (input_tokens / 1_000_000) * self.INPUT_PRICE_PER_M
        output_cost = (output_tokens / 1_000_000) * self.OUTPUT_PRICE_PER_M
        self.estimated_cost += input_cost + output_cost

    def get_summary(self) -> str:
        """Get usage summary string."""
        return (
            f"API Calls: {self.api_calls} | "
            f"Tokens: {self.total_tokens:,} (in: {self.input_tokens:,}, out: {self.output_tokens:,}) | "
            f"Est. Cost: ${self.estimated_cost:.4f}"
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary for saving."""
        return {
            'input_tokens': self.input_tokens,
            'output_tokens': self.output_tokens,
            'total_tokens': self.total_tokens,
            'estimated_cost': self.estimated_cost,
            'api_calls': self.api_calls
        }


# Global token tracker
token_tracker = TokenUsage()


# ==================== RATE LIMITER ====================

class RateLimiter:
    """Rate limiter for API calls."""

    def __init__(self, calls_per_minute: int = 50, calls_per_second: int = 2):
        self.calls_per_minute = calls_per_minute
        self.calls_per_second = calls_per_second
        self.call_timestamps: List[float] = []
        self.min_interval = 1.0 / calls_per_second
        self.last_call_time = 0.0

    def wait_if_needed(self):
        """Wait if we're hitting rate limits."""
        now = time.time()

        # Clean old timestamps (older than 1 minute)
        self.call_timestamps = [t for t in self.call_timestamps if now - t < 60]

        # Check per-minute limit
        if len(self.call_timestamps) >= self.calls_per_minute:
            wait_time = 60 - (now - self.call_timestamps[0])
            if wait_time > 0:
                logger.warning(f"Rate limit: waiting {wait_time:.1f}s (per-minute limit)")
                time.sleep(wait_time)
                now = time.time()

        # Check per-second limit
        time_since_last = now - self.last_call_time
        if time_since_last < self.min_interval:
            wait_time = self.min_interval - time_since_last
            time.sleep(wait_time)
            now = time.time()

        # Record this call
        self.call_timestamps.append(now)
        self.last_call_time = now

    def get_status(self) -> str:
        """Get current rate limit status."""
        now = time.time()
        recent_calls = len([t for t in self.call_timestamps if now - t < 60])
        return f"API calls in last minute: {recent_calls}/{self.calls_per_minute}"


# Global rate limiters
anthropic_limiter = RateLimiter(calls_per_minute=50, calls_per_second=1)
ghl_limiter = RateLimiter(calls_per_minute=100, calls_per_second=5)


# ==================== CONFIGURATION ====================

class Config:
    """Central configuration for the AI Ops Manager."""

    # Paths - Now configurable via environment variables
    BASE_DIR = Path(os.getenv('AI_OPS_BASE_DIR', Path.home() / 'DigitalMarketing'))
    RESOURCES_DIR = BASE_DIR / "Resources"
    DOCS_DIR = BASE_DIR / "Business_Operations" / "Strategic_Planning_Docs"
    OUTPUT_DIR = Path(os.getenv('AI_OPS_OUTPUT_DIR', BASE_DIR / "AI_Generated"))
    COST_TRACKING_DIR = BASE_DIR / "Business_Operations" / "Financial_Models_Full"
    LOG_DIR = Path(os.getenv('AI_OPS_LOG_DIR', BASE_DIR / "logs"))

    # API Keys (from environment)
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    GHL_API_KEY = os.getenv('GHL_API_KEY')
    GHL_LOCATION_ID = os.getenv('GHL_LOCATION_ID')

    # Claude Settings
    CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', "claude-sonnet-4-20250514")
    MAX_TOKENS = int(os.getenv('CLAUDE_MAX_TOKENS', 8192))

    # GHL API Settings
    GHL_BASE_URL = "https://services.leadconnectorhq.com"
    GHL_API_VERSION = "2021-07-28"
    GHL_PAGE_LIMIT = 100  # Max contacts per page

    # Market Research Settings
    TARGET_INDUSTRIES = [
        "Real Estate Agents",
        "Contractors (HVAC, Plumbing, Electrical)",
        "Med Spas",
        "Dentists",
        "Chiropractors",
        "Law Firms (Personal Injury, Family)",
        "Auto Repair Shops",
        "Roofing Companies"
    ]

    # Cost Tracking (Monthly Services)
    KNOWN_SERVICES = {
        "GHL": {"base": 297, "description": "Go High Level CRM"},
        "Claude": {"base": 0, "description": "Anthropic API (usage-based)"},
        "Hosting": {"base": 50, "description": "Website hosting"},
        "Domains": {"base": 15, "description": "Domain registrations"},
        "N8N": {"base": 0, "description": "Self-hosted automation"}
    }

    @classmethod
    def validate(cls) -> Tuple[bool, List[str]]:
        """Validate configuration and return status with any issues."""
        issues = []

        if not cls.ANTHROPIC_API_KEY:
            issues.append("ANTHROPIC_API_KEY not set")

        if not cls.GHL_API_KEY:
            issues.append("GHL_API_KEY not set (GHL features disabled)")

        if not cls.GHL_LOCATION_ID:
            issues.append("GHL_LOCATION_ID not set (GHL features disabled)")

        # Create directories if they don't exist
        for dir_path in [cls.OUTPUT_DIR, cls.LOG_DIR]:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                issues.append(f"Cannot create directory {dir_path}: {e}")

        return len(issues) == 0 or cls.ANTHROPIC_API_KEY is not None, issues

    @classmethod
    def print_config(cls):
        """Print current configuration (masking sensitive values)."""
        print("\n--- Configuration ---")
        print(f"Base Directory: {cls.BASE_DIR}")
        print(f"Output Directory: {cls.OUTPUT_DIR}")
        print(f"Log Directory: {cls.LOG_DIR}")
        print(f"Claude Model: {cls.CLAUDE_MODEL}")
        print(f"Anthropic API Key: {'*' * 20 + cls.ANTHROPIC_API_KEY[-4:] if cls.ANTHROPIC_API_KEY else 'NOT SET'}")
        print(f"GHL API Key: {'*' * 20 + cls.GHL_API_KEY[-4:] if cls.GHL_API_KEY else 'NOT SET'}")
        print(f"GHL Location ID: {cls.GHL_LOCATION_ID or 'NOT SET'}")
        print("--------------------\n")


# ==================== DATA MODELS ====================

@dataclass
class MarketResearch:
    """Market research findings."""
    industry: str
    market_size: str
    avg_client_value: float
    competition_level: str
    pain_points: List[str]
    best_pricing_model: str
    recommended_services: List[str]
    go_to_market_strategy: str
    timestamp: str


@dataclass
class CRMAnalysis:
    """GHL CRM analysis results."""
    total_contacts: int
    active_pipelines: int
    automation_count: int
    conversion_rate: float
    recommendations: List[str]
    quick_wins: List[str]
    infrastructure_gaps: List[str]
    timestamp: str


@dataclass
class CostAnalysis:
    """Monthly cost breakdown."""
    total_monthly_cost: float
    service_breakdown: Dict[str, float]
    overhead_percentage: float
    recommendations: List[str]
    potential_savings: List[Dict[str, Any]]
    timestamp: str


# ==================== CORE AI AGENT ====================

class AIOperationsManager:
    """Main AI Operations & Business Development Manager."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.ANTHROPIC_API_KEY
        if not self.api_key:
            raise ValueError("Anthropic API key required. Set ANTHROPIC_API_KEY environment variable.")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.conversation_history = []
        self.max_history_length = 20  # Limit conversation history

        # Initialize sub-agents
        self.doc_generator = DocumentationAgent(self.client)
        self.crm_analyzer = CRMAnalyzer(self.client)
        self.market_researcher = MarketResearcher(self.client)
        self.cost_controller = CostController(self.client)
        self.strategist = BusinessStrategist(self.client)

        logger.info("AIOperationsManager initialized successfully")

    def analyze_business_state(self) -> Dict:
        """Comprehensive business state analysis."""
        print("\n" + "="*80)
        print("AI OPERATIONS MANAGER - COMPREHENSIVE BUSINESS ANALYSIS")
        print("="*80)

        logger.info("Starting comprehensive business analysis")

        results = {}
        errors = []

        # 1. CRM Analysis
        print("\n[1/4] Analyzing GHL CRM Infrastructure...")
        try:
            crm_analysis = self.crm_analyzer.analyze_infrastructure()
            results['crm'] = crm_analysis
            print(f"  [OK] Found {crm_analysis.total_contacts} contacts, {crm_analysis.active_pipelines} pipelines")
            logger.info(f"CRM analysis complete: {crm_analysis.total_contacts} contacts")
        except Exception as e:
            error_msg = f"CRM analysis failed: {e}"
            print(f"  [WARN] CRM analysis skipped: {e}")
            logger.error(error_msg, exc_info=True)
            errors.append(error_msg)
            results['crm'] = None

        # 2. Cost Analysis
        print("\n[2/4] Analyzing Costs & Overhead...")
        try:
            cost_analysis = self.cost_controller.analyze_costs()
            results['costs'] = cost_analysis
            print(f"  [OK] Monthly costs: ${cost_analysis.total_monthly_cost:.2f}")
            logger.info(f"Cost analysis complete: ${cost_analysis.total_monthly_cost:.2f}/month")
        except Exception as e:
            error_msg = f"Cost analysis failed: {e}"
            print(f"  [WARN] Cost analysis skipped: {e}")
            logger.error(error_msg, exc_info=True)
            errors.append(error_msg)
            results['costs'] = None

        # 3. Market Research
        print("\n[3/4] Researching Market Trends...")
        try:
            market_insights = self.market_researcher.research_top_industries()
            results['markets'] = market_insights
            print(f"  [OK] Analyzed {len(market_insights)} industries")
            logger.info(f"Market research complete: {len(market_insights)} industries")
        except Exception as e:
            error_msg = f"Market research failed: {e}"
            print(f"  [WARN] Market research skipped: {e}")
            logger.error(error_msg, exc_info=True)
            errors.append(error_msg)
            results['markets'] = []

        # 4. Strategic Recommendations
        print("\n[4/4] Generating Strategic Recommendations...")
        try:
            strategy = self.strategist.generate_strategy(
                crm_data=results.get('crm'),
                cost_data=results.get('costs'),
                market_data=results.get('markets', [])
            )
            results['strategy'] = strategy
            rec_count = len(strategy.get('recommendations', []))
            print(f"  [OK] Generated {rec_count} recommendations")
            logger.info(f"Strategy generation complete: {rec_count} recommendations")
        except Exception as e:
            error_msg = f"Strategy generation failed: {e}"
            print(f"  [WARN] Strategy generation skipped: {e}")
            logger.error(error_msg, exc_info=True)
            errors.append(error_msg)
            results['strategy'] = None

        # Add metadata
        results['metadata'] = {
            'timestamp': datetime.now().isoformat(),
            'errors': errors,
            'token_usage': token_tracker.to_dict()
        }

        # Save results
        self._save_analysis(results)

        # Print token usage summary
        print(f"\n[Token Usage] {token_tracker.get_summary()}")

        return results

    def _save_analysis(self, results: Dict):
        """Save analysis results."""
        output_dir = Config.OUTPUT_DIR / "Business_Analysis"
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = output_dir / f"business_analysis_{timestamp}.json"

        # Convert dataclasses to dicts properly
        serializable = {}
        for key, value in results.items():
            if isinstance(value, list):
                serializable[key] = [
                    asdict(item) if hasattr(item, '__dataclass_fields__') else item
                    for item in value
                ]
            elif hasattr(value, '__dataclass_fields__'):
                serializable[key] = asdict(value)
            else:
                serializable[key] = value

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(serializable, f, indent=2, default=str)
            print(f"\n[FILE] Analysis saved: {filepath}")
            logger.info(f"Analysis saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save analysis: {e}", exc_info=True)
            print(f"\n[ERROR] Failed to save analysis: {e}")

    def chat(self, message: str) -> str:
        """Interactive chat with the AI Ops Manager."""
        # Trim history if too long
        if len(self.conversation_history) > self.max_history_length * 2:
            self.conversation_history = self.conversation_history[-self.max_history_length * 2:]
            logger.debug("Trimmed conversation history")

        self.conversation_history.append({
            "role": "user",
            "content": message
        })

        system_prompt = """You are an AI Operations & Business Development Manager for Premier Lead Marketing,
a digital marketing agency specializing in Go High Level implementations for local businesses.

Your responsibilities:
1. Strategic Planning - Market analysis, go-to-market strategies, industry selection
2. Operations Management - CRM optimization, automation workflows, infrastructure
3. Financial Control - Cost tracking, overhead management, pricing strategies
4. Business Development - Lead generation, service offerings, competitive positioning
5. Documentation - SOPs, landing pages, CTAs, technical documentation

Provide actionable, data-driven advice with specific steps. Always consider:
- Cost efficiency and ROI
- Market trends and competitive landscape
- Implementation complexity vs. impact
- Scalability and sustainability

Be direct, analytical, and focused on revenue growth and operational excellence."""

        try:
            anthropic_limiter.wait_if_needed()

            response = self.client.messages.create(
                model=Config.CLAUDE_MODEL,
                max_tokens=Config.MAX_TOKENS,
                system=system_prompt,
                messages=self.conversation_history
            )

            # Track token usage
            token_tracker.add_usage(
                response.usage.input_tokens,
                response.usage.output_tokens
            )
            logger.debug(f"Chat API call: {response.usage.input_tokens} in, {response.usage.output_tokens} out")

            assistant_message = response.content[0].text

            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except Exception as e:
            logger.error(f"Chat error: {e}", exc_info=True)
            raise


# ==================== DOCUMENTATION AGENT ====================

class DocumentationAgent:
    """Generates SOPs, landing pages, CTAs, and technical docs."""

    def __init__(self, client):
        self.client = client

    def _call_claude(self, prompt: str, max_tokens: int = 4096) -> str:
        """Make a Claude API call with rate limiting and token tracking."""
        anthropic_limiter.wait_if_needed()

        response = self.client.messages.create(
            model=Config.CLAUDE_MODEL,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )

        token_tracker.add_usage(
            response.usage.input_tokens,
            response.usage.output_tokens
        )
        logger.debug(f"DocumentationAgent API call: {response.usage.input_tokens} in, {response.usage.output_tokens} out")

        return response.content[0].text

    def generate_sop(self, topic: str, target_audience: str = "team") -> str:
        """Generate Standard Operating Procedure."""
        logger.info(f"Generating SOP for: {topic}")

        prompt = f"""Create a detailed SOP for: {topic}

Target Audience: {target_audience}

Include:
1. Purpose and Scope
2. Step-by-step procedures
3. Screenshots/visual references needed (note locations)
4. Common issues and troubleshooting
5. Success criteria

Format as markdown with clear headings and numbered steps."""

        return self._call_claude(prompt)

    def generate_landing_page(self, industry: str, service: str, pain_points: List[str]) -> Dict:
        """Generate landing page copy and structure."""
        logger.info(f"Generating landing page for: {industry} - {service}")

        prompt = f"""Create a high-converting landing page for:

Industry: {industry}
Service: {service}
Pain Points: {', '.join(pain_points)}

Provide:
1. Compelling headline (with 3 variations)
2. Subheadline
3. Hero section copy
4. Benefits (5-7 bullet points)
5. Social proof section (what to include)
6. CTA (3 variations - primary, secondary, urgent)
7. FAQ section (top 5 questions)
8. Technical specs (form fields, tracking pixels needed)

Return as JSON structure."""

        return self._call_claude(prompt)

    def generate_cta_variations(self, context: str, goal: str) -> List[str]:
        """Generate CTA button variations."""
        logger.info(f"Generating CTA variations for goal: {goal}")

        prompt = f"""Generate 10 high-converting CTA button variations for:

Context: {context}
Goal: {goal}

Requirements:
- Action-oriented
- Create urgency
- Clear value proposition
- Mix of short (2-3 words) and longer (4-7 words)
- Consider different psychological triggers (urgency, curiosity, benefit, social proof)

Return as a numbered list."""

        return self._call_claude(prompt, max_tokens=2048)


# ==================== CRM ANALYZER ====================

class CRMAnalyzer:
    """Analyzes Go High Level CRM infrastructure."""

    def __init__(self, client):
        self.client = client
        self.api_key = Config.GHL_API_KEY
        self.location_id = Config.GHL_LOCATION_ID
        self.base_url = Config.GHL_BASE_URL
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Version': Config.GHL_API_VERSION,
            'Content-Type': 'application/json'
        }

    def _call_claude(self, prompt: str, max_tokens: int = 4096) -> str:
        """Make a Claude API call with rate limiting and token tracking."""
        anthropic_limiter.wait_if_needed()

        response = self.client.messages.create(
            model=Config.CLAUDE_MODEL,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )

        token_tracker.add_usage(
            response.usage.input_tokens,
            response.usage.output_tokens
        )

        return response.content[0].text

    def analyze_infrastructure(self) -> CRMAnalysis:
        """Comprehensive GHL infrastructure analysis."""
        logger.info("Starting CRM infrastructure analysis")

        # Get CRM data
        crm_data = self._fetch_ghl_data()

        # Analyze with AI
        analysis_prompt = f"""Analyze this Go High Level CRM infrastructure and provide recommendations:

CRM Data:
{json.dumps(crm_data, indent=2, default=str)}

Provide:
1. Key metrics summary
2. Infrastructure gaps (missing pipelines, automations, etc.)
3. Quick wins (easy improvements with high impact)
4. Long-term recommendations
5. Automation opportunities
6. Lead flow optimization

Return as JSON with these fields:
- recommendations: [list of actionable items]
- quick_wins: [list of quick improvements]
- infrastructure_gaps: [list of missing components]"""

        analysis_text = self._call_claude(analysis_prompt)

        return CRMAnalysis(
            total_contacts=crm_data.get('contact_count', 0),
            active_pipelines=crm_data.get('pipeline_count', 0),
            automation_count=crm_data.get('workflow_count', 0),
            conversion_rate=crm_data.get('conversion_rate', 0.0),
            recommendations=self._extract_recommendations(analysis_text),
            quick_wins=self._extract_quick_wins(analysis_text),
            infrastructure_gaps=self._extract_gaps(analysis_text),
            timestamp=datetime.now().isoformat()
        )

    def _fetch_ghl_data(self) -> Dict:
        """Fetch data from GHL API with pagination."""
        if not self.api_key or not self.location_id:
            logger.warning("GHL API key or Location ID not configured")
            return {
                'contact_count': 0,
                'pipeline_count': 0,
                'workflow_count': 0,
                'conversion_rate': 0.0,
                'note': 'GHL API key or Location ID not configured'
            }

        result = {
            'contact_count': 0,
            'pipeline_count': 0,
            'workflow_count': 0,
            'conversion_rate': 0.0,
            'contacts': [],
            'pipelines': [],
            'workflows': []
        }

        try:
            # Fetch ALL contacts with pagination
            logger.info("Fetching contacts from GHL API...")
            all_contacts = self._fetch_all_contacts()
            result['contacts'] = all_contacts[:50]  # Store first 50 for analysis
            result['contact_count'] = len(all_contacts)
            logger.info(f"Fetched {len(all_contacts)} total contacts")

            # Fetch pipelines
            logger.info("Fetching pipelines from GHL API...")
            pipelines = self._fetch_pipelines()
            result['pipelines'] = pipelines
            result['pipeline_count'] = len(pipelines)
            logger.info(f"Fetched {len(pipelines)} pipelines")

            # Fetch workflows
            logger.info("Fetching workflows from GHL API...")
            workflows = self._fetch_workflows()
            result['workflows'] = workflows
            result['workflow_count'] = len(workflows)
            logger.info(f"Fetched {len(workflows)} workflows")

            # Calculate conversion rate if we have pipeline data
            if pipelines and all_contacts:
                # This is a simplified calculation
                result['conversion_rate'] = self._calculate_conversion_rate(all_contacts, pipelines)

        except Exception as e:
            logger.error(f"GHL API error: {e}", exc_info=True)
            result['error'] = str(e)

        return result

    def _fetch_all_contacts(self) -> List[Dict]:
        """Fetch all contacts with pagination."""
        all_contacts = []
        start_after = None
        page = 1
        max_pages = 50  # Safety limit

        while page <= max_pages:
            ghl_limiter.wait_if_needed()

            url = f"{self.base_url}/contacts/"
            params = {
                'locationId': self.location_id,
                'limit': Config.GHL_PAGE_LIMIT
            }

            if start_after:
                params['startAfter'] = start_after

            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()

                contacts = data.get('contacts', [])
                if not contacts:
                    break

                all_contacts.extend(contacts)
                logger.debug(f"Fetched page {page}: {len(contacts)} contacts (total: {len(all_contacts)})")

                # Check for next page
                meta = data.get('meta', {})
                start_after = meta.get('startAfter')

                if not start_after or len(contacts) < Config.GHL_PAGE_LIMIT:
                    break

                page += 1

            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching contacts page {page}: {e}")
                break

        return all_contacts

    def _fetch_pipelines(self) -> List[Dict]:
        """Fetch all pipelines."""
        ghl_limiter.wait_if_needed()

        url = f"{self.base_url}/opportunities/pipelines"
        params = {'locationId': self.location_id}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get('pipelines', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching pipelines: {e}")
            return []

    def _fetch_workflows(self) -> List[Dict]:
        """Fetch all workflows."""
        ghl_limiter.wait_if_needed()

        url = f"{self.base_url}/workflows/"
        params = {'locationId': self.location_id}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get('workflows', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching workflows: {e}")
            return []

    def _calculate_conversion_rate(self, contacts: List[Dict], pipelines: List[Dict]) -> float:
        """Calculate overall conversion rate."""
        # Simplified - in production would be more sophisticated
        if not contacts:
            return 0.0

        # Count contacts with opportunities
        contacts_with_opps = sum(1 for c in contacts if c.get('opportunities'))
        return (contacts_with_opps / len(contacts)) * 100 if contacts else 0.0

    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract recommendations from AI response."""
        lines = text.split('\n')
        recommendations = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(('-', '*', '•')) or (stripped and stripped[0].isdigit() and '.' in stripped[:3]):
                clean = stripped.lstrip('-*•0123456789. ')
                if len(clean) > 10:
                    recommendations.append(clean)
        return recommendations[:10]

    def _extract_quick_wins(self, text: str) -> List[str]:
        """Extract quick wins from AI response."""
        return self._extract_recommendations(text)[:5]

    def _extract_gaps(self, text: str) -> List[str]:
        """Extract infrastructure gaps from AI response."""
        return self._extract_recommendations(text)[:5]


# ==================== MARKET RESEARCHER ====================

class MarketResearcher:
    """Conducts market research and competitive analysis."""

    def __init__(self, client):
        self.client = client

    def _call_claude(self, prompt: str, max_tokens: int = 4096) -> str:
        """Make a Claude API call with rate limiting and token tracking."""
        anthropic_limiter.wait_if_needed()

        response = self.client.messages.create(
            model=Config.CLAUDE_MODEL,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )

        token_tracker.add_usage(
            response.usage.input_tokens,
            response.usage.output_tokens
        )

        return response.content[0].text

    def research_top_industries(self) -> List[MarketResearch]:
        """Research top industries for targeting."""
        results = []

        logger.info(f"Researching {len(Config.TARGET_INDUSTRIES[:3])} industries")

        for industry in Config.TARGET_INDUSTRIES[:3]:
            try:
                research = self.research_industry(industry)
                results.append(research)
                logger.info(f"Completed research for: {industry}")
            except Exception as e:
                logger.error(f"Failed to research {industry}: {e}", exc_info=True)
                # Continue with other industries instead of failing completely
                continue

        return results

    def research_industry(self, industry: str) -> MarketResearch:
        """Deep dive research on specific industry."""
        logger.info(f"Researching industry: {industry}")

        prompt = f"""Conduct comprehensive market research for: {industry}

As of January 2026, provide:

1. Market Size & Growth
   - Total addressable market
   - Growth rate (2025-2026)
   - Market trends

2. Client Economics
   - Average client lifetime value
   - Typical marketing budget
   - ROI expectations

3. Pain Points (top 5-7)
   - What keeps them up at night?
   - Current frustrations with marketing
   - Technology gaps

4. Competition Analysis
   - Competition level (Low/Medium/High)
   - What competitors are doing
   - Gaps in market

5. Pricing Strategy
   - Recommended pricing model (monthly retainer, project-based, performance-based)
   - Price range that converts
   - What services to bundle

6. Service Recommendations
   - Most needed services
   - Quick win services
   - Premium services

7. Go-to-Market Strategy
   - Best channels to reach them
   - Messaging that resonates
   - Objection handling

Return as detailed analysis with specific numbers and actionable insights."""

        analysis = self._call_claude(prompt)

        return MarketResearch(
            industry=industry,
            market_size=self._extract_market_size(analysis),
            avg_client_value=self._extract_client_value(analysis),
            competition_level=self._extract_competition(analysis),
            pain_points=self._extract_pain_points(analysis),
            best_pricing_model=self._extract_pricing(analysis),
            recommended_services=self._extract_services(analysis),
            go_to_market_strategy=self._extract_strategy(analysis),
            timestamp=datetime.now().isoformat()
        )

    def compare_industries(self, industries: List[str]) -> Dict:
        """Compare multiple industries head-to-head."""
        logger.info(f"Comparing industries: {industries}")

        prompt = f"""Compare these industries for a digital marketing agency:

Industries: {', '.join(industries)}

Create a comparison table with:
- Market attractiveness score (1-10)
- Ease of entry (1-10)
- Profit potential (1-10)
- Competition level (1-10)
- Time to first sale
- Recommended focus for January 2026

Provide final recommendation of top 2 industries to pursue NOW."""

        comparison = self._call_claude(prompt, max_tokens=3072)

        return {
            'comparison': comparison,
            'timestamp': datetime.now().isoformat()
        }

    def _extract_market_size(self, text: str) -> str:
        """Extract market size from research text."""
        import re
        if "billion" in text.lower():
            match = re.search(r'\$?(\d+\.?\d*)\s*billion', text, re.IGNORECASE)
            if match:
                return f"${match.group(1)}B"
        if "million" in text.lower():
            match = re.search(r'\$?(\d+\.?\d*)\s*million', text, re.IGNORECASE)
            if match:
                return f"${match.group(1)}M"
        return "Market size not specified"

    def _extract_client_value(self, text: str) -> float:
        """Extract average client value."""
        import re
        matches = re.findall(r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text)
        if matches:
            # Get the largest value found (likely the LTV)
            values = [float(m.replace(',', '')) for m in matches]
            return max(values) if values else 0.0
        return 0.0

    def _extract_competition(self, text: str) -> str:
        """Extract competition level."""
        text_lower = text.lower()
        if 'high competition' in text_lower or 'very competitive' in text_lower or 'highly competitive' in text_lower:
            return "High"
        elif 'low competition' in text_lower or 'less competitive' in text_lower:
            return "Low"
        return "Medium"

    def _extract_pain_points(self, text: str) -> List[str]:
        """Extract pain points."""
        lines = text.split('\n')
        pain_points = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(('-', '*', '•')) or (stripped and stripped[0].isdigit() and '.' in stripped[:3]):
                clean = stripped.lstrip('-*•0123456789. ')
                if 10 < len(clean) < 200:
                    pain_points.append(clean)
        return pain_points[:7]

    def _extract_pricing(self, text: str) -> str:
        """Extract pricing recommendation."""
        text_lower = text.lower()
        if 'monthly retainer' in text_lower:
            return "Monthly Retainer"
        elif 'performance' in text_lower and 'based' in text_lower:
            return "Performance-Based"
        elif 'project' in text_lower and 'based' in text_lower:
            return "Project-Based"
        return "Hybrid Model"

    def _extract_services(self, text: str) -> List[str]:
        """Extract recommended services."""
        return self._extract_pain_points(text)[:5]

    def _extract_strategy(self, text: str) -> str:
        """Extract go-to-market strategy."""
        paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 50]
        return '\n\n'.join(paragraphs[-2:]) if paragraphs else text[-500:]


# ==================== COST CONTROLLER ====================

class CostController:
    """Tracks costs, overhead, and identifies savings."""

    def __init__(self, client):
        self.client = client

    def _call_claude(self, prompt: str, max_tokens: int = 2048) -> str:
        """Make a Claude API call with rate limiting and token tracking."""
        anthropic_limiter.wait_if_needed()

        response = self.client.messages.create(
            model=Config.CLAUDE_MODEL,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )

        token_tracker.add_usage(
            response.usage.input_tokens,
            response.usage.output_tokens
        )

        return response.content[0].text

    def analyze_costs(self) -> CostAnalysis:
        """Analyze all costs and overhead."""
        logger.info("Starting cost analysis")

        monthly_costs = self._calculate_monthly_costs()

        # Add current session's API costs
        monthly_costs['Claude_API_Session'] = token_tracker.estimated_cost

        cost_prompt = f"""Analyze these monthly costs for a digital marketing agency:

Current Costs:
{json.dumps(monthly_costs, indent=2)}

Provide:
1. Cost optimization opportunities
2. Services that could be eliminated/consolidated
3. Alternative solutions that cost less
4. Warning signs of overspending
5. Benchmark comparison (are these costs normal for this business?)

Return actionable recommendations."""

        recommendations_text = self._call_claude(cost_prompt)

        return CostAnalysis(
            total_monthly_cost=sum(monthly_costs.values()),
            service_breakdown=monthly_costs,
            overhead_percentage=0.0,
            recommendations=self._extract_recommendations_from_text(recommendations_text),
            potential_savings=self._identify_savings(monthly_costs, recommendations_text),
            timestamp=datetime.now().isoformat()
        )

    def _calculate_monthly_costs(self) -> Dict[str, float]:
        """Calculate all monthly costs."""
        costs = {}

        for service, info in Config.KNOWN_SERVICES.items():
            costs[service] = info['base']

        return costs

    def _extract_recommendations_from_text(self, text: str) -> List[str]:
        """Extract cost recommendations."""
        lines = text.split('\n')
        recommendations = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(('-', '*', '•')) or (stripped and stripped[0].isdigit() and '.' in stripped[:3]):
                clean = stripped.lstrip('-*•0123456789. ')
                if len(clean) > 10:
                    recommendations.append(clean)
        return recommendations[:10]

    def _identify_savings(self, costs: Dict, analysis: str) -> List[Dict]:
        """Identify potential cost savings."""
        savings = []

        for service, cost in costs.items():
            if cost > 0 and service.lower() in analysis.lower():
                savings.append({
                    'service': service,
                    'current_cost': cost,
                    'potential_saving': 0,
                    'recommendation': f"Review {service} usage"
                })

        return savings

    def benchmark_salary(self, position: str, location: str = "Remote") -> Dict:
        """Research competitive salary for position."""
        logger.info(f"Researching salary benchmark for: {position}")

        prompt = f"""Research competitive compensation for: {position}

Location: {location}
Date: January 2026

Provide:
1. Salary Range (min-max annual)
2. Typical hourly rate (if contractor)
3. Commission/bonus structure (if sales)
4. Benefits package expectations
5. Market trends (up/down/stable)
6. Red flags in negotiations

Be specific with numbers."""

        analysis = self._call_claude(prompt)

        return {
            'position': position,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }


# ==================== BUSINESS STRATEGIST ====================

class BusinessStrategist:
    """Develops business strategy and recommendations."""

    def __init__(self, client):
        self.client = client

    def _call_claude(self, prompt: str, max_tokens: int = 8192) -> str:
        """Make a Claude API call with rate limiting and token tracking."""
        anthropic_limiter.wait_if_needed()

        response = self.client.messages.create(
            model=Config.CLAUDE_MODEL,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )

        token_tracker.add_usage(
            response.usage.input_tokens,
            response.usage.output_tokens
        )

        return response.content[0].text

    def generate_strategy(self, crm_data: Any, cost_data: CostAnalysis,
                         market_data: List[MarketResearch]) -> Dict:
        """Generate comprehensive business strategy."""
        logger.info("Generating business strategy")

        context = f"""
CRM State:
- Total Contacts: {crm_data.total_contacts if crm_data else 0}
- Active Pipelines: {crm_data.active_pipelines if crm_data else 0}
- Conversion Rate: {crm_data.conversion_rate if crm_data else 0}%

Cost Structure:
- Monthly Costs: ${cost_data.total_monthly_cost:.2f if cost_data else 0}
- Services: {', '.join(cost_data.service_breakdown.keys()) if cost_data else 'N/A'}

Market Research:
{self._summarize_market_data(market_data)}

Current Date: January 2026
"""

        prompt = f"""As Premier Lead Marketing's Operations & Business Development Manager,
create a comprehensive 30-60-90 day strategic plan.

Current Business State:
{context}

Provide:

1. IMMEDIATE ACTIONS (Next 7 Days)
   - Quick wins to generate revenue
   - Critical infrastructure fixes
   - Market opportunities to pursue NOW

2. SHORT-TERM STRATEGY (30 Days)
   - Industry focus and why
   - Service offering refinement
   - Pricing strategy
   - Marketing approach
   - Sales process improvements

3. MEDIUM-TERM STRATEGY (60 Days)
   - Team building (what roles, when)
   - Automation expansion
   - Client retention programs
   - New service launches

4. LONG-TERM VISION (90 Days)
   - Revenue targets and how to hit them
   - Market positioning
   - Scaling strategy
   - Risk mitigation

5. KEY METRICS TO TRACK
   - What to measure daily/weekly/monthly
   - Target numbers

Be specific, actionable, and focused on profitable growth."""

        strategy_text = self._call_claude(prompt)

        return {
            'strategy': strategy_text,
            'recommendations': self._extract_action_items(strategy_text),
            'priorities': self._extract_priorities(strategy_text),
            'metrics': self._extract_metrics(strategy_text),
            'timestamp': datetime.now().isoformat()
        }

    def _summarize_market_data(self, market_data: List[MarketResearch]) -> str:
        """Summarize market research findings."""
        if not market_data:
            return "No market data available"

        summary = []
        for research in market_data:
            summary.append(f"""
Industry: {research.industry}
- Market Size: {research.market_size}
- Competition: {research.competition_level}
- Avg Client Value: ${research.avg_client_value}
- Pricing Model: {research.best_pricing_model}
""")

        return '\n'.join(summary)

    def _extract_action_items(self, text: str) -> List[str]:
        """Extract action items from strategy."""
        lines = text.split('\n')
        actions = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(('-', '*', '•')) or (stripped and stripped[0].isdigit() and '.' in stripped[:3]):
                clean = stripped.lstrip('-*•0123456789. ')
                if len(clean) > 10:
                    actions.append(clean)
        return actions[:20]

    def _extract_priorities(self, text: str) -> List[str]:
        """Extract top priorities."""
        return self._extract_action_items(text)[:5]

    def _extract_metrics(self, text: str) -> List[str]:
        """Extract key metrics to track."""
        if "metrics" in text.lower():
            lines = text.lower().split('\n')
            metric_section_start = next(
                (i for i, line in enumerate(lines) if 'metrics' in line),
                -1
            )
            if metric_section_start >= 0:
                metric_lines = text.split('\n')[metric_section_start:metric_section_start + 10]
                return [
                    line.strip().lstrip('-*•')
                    for line in metric_lines
                    if line.strip().startswith(('-', '*', '•'))
                ]

        return []


# ==================== CLI INTERFACE ====================

def print_token_status():
    """Print current token usage status."""
    print(f"\n[Token Status] {token_tracker.get_summary()}")
    print(f"[Rate Limit] {anthropic_limiter.get_status()}")


def main():
    """Main CLI interface."""

    print("""
+-------------------------------------------------------------------------------+
|                                                                               |
|           Premier Lead Marketing - AI Operations Manager v1.1                 |
|                                                                               |
|     Your AI-powered Operations & Business Development Manager                 |
|                        (Fixed Edition with Full Features)                     |
|                                                                               |
+-------------------------------------------------------------------------------+
    """)

    # Validate configuration
    valid, issues = Config.validate()
    if issues:
        print("\n[CONFIG] Warnings:")
        for issue in issues:
            print(f"  - {issue}")

    if not valid:
        print("\n[ERROR] Critical configuration missing. Cannot continue.")
        print("Set your API key: set ANTHROPIC_API_KEY=your_key_here")
        return

    try:
        manager = AIOperationsManager()

        print("\n[OK] Initialized successfully!")
        print(f"[INFO] Logs: {Config.LOG_DIR}")
        print(f"[INFO] Output: {Config.OUTPUT_DIR}")

        print("\nAvailable Commands:")
        print("  1. Full Business Analysis")
        print("  2. Market Research (specific industry)")
        print("  3. CRM Infrastructure Review")
        print("  4. Cost Analysis & Optimization")
        print("  5. Generate SOP")
        print("  6. Generate Landing Page Copy")
        print("  7. Generate CTA Variations")
        print("  8. Salary Benchmarking")
        print("  9. Compare Industries")
        print(" 10. Chat with AI Ops Manager")
        print(" 11. Show Token Usage")
        print(" 12. Show Configuration")
        print("  0. Exit")

        while True:
            try:
                choice = input("\nSelect option (0-12): ").strip()

                if choice == '0':
                    print_token_status()
                    print("\nGoodbye!")
                    break

                elif choice == '1':
                    analysis = manager.analyze_business_state()
                    print("\n[OK] Full analysis complete. Check AI_Generated/Business_Analysis/")

                elif choice == '2':
                    industry = input("Industry to research: ").strip()
                    if not industry:
                        print("[WARN] Industry name required")
                        continue
                    research = manager.market_researcher.research_industry(industry)
                    print(f"\n[OK] Research complete for {industry}")
                    print(f"Competition: {research.competition_level}")
                    print(f"Pricing Model: {research.best_pricing_model}")
                    print_token_status()

                elif choice == '3':
                    analysis = manager.crm_analyzer.analyze_infrastructure()
                    print(f"\n[OK] CRM Analysis:")
                    print(f"  Contacts: {analysis.total_contacts}")
                    print(f"  Pipelines: {analysis.active_pipelines}")
                    print(f"  Workflows: {analysis.automation_count}")
                    print(f"  Quick Wins: {len(analysis.quick_wins)}")
                    print_token_status()

                elif choice == '4':
                    costs = manager.cost_controller.analyze_costs()
                    print(f"\n[OK] Cost Analysis:")
                    print(f"  Monthly Total: ${costs.total_monthly_cost:.2f}")
                    print(f"  Recommendations: {len(costs.recommendations)}")
                    print_token_status()

                elif choice == '5':
                    topic = input("SOP topic: ").strip()
                    if not topic:
                        print("[WARN] Topic required")
                        continue
                    sop = manager.doc_generator.generate_sop(topic)
                    print(f"\n[OK] SOP generated")
                    print(sop[:500] + "..." if len(sop) > 500 else sop)
                    print_token_status()

                elif choice == '6':
                    industry = input("Industry: ").strip()
                    service = input("Service: ").strip()
                    pain_points = input("Pain points (comma-separated): ").strip().split(',')
                    if not industry or not service:
                        print("[WARN] Industry and service required")
                        continue
                    landing_page = manager.doc_generator.generate_landing_page(
                        industry, service, [p.strip() for p in pain_points if p.strip()]
                    )
                    print(f"\n[OK] Landing page copy generated")
                    print(landing_page[:500] + "..." if len(landing_page) > 500 else landing_page)
                    print_token_status()

                elif choice == '7':
                    context = input("Context: ").strip()
                    goal = input("Goal: ").strip()
                    if not context or not goal:
                        print("[WARN] Context and goal required")
                        continue
                    ctas = manager.doc_generator.generate_cta_variations(context, goal)
                    print(f"\n[OK] CTA variations:")
                    print(ctas)
                    print_token_status()

                elif choice == '8':
                    position = input("Position title: ").strip()
                    if not position:
                        print("[WARN] Position title required")
                        continue
                    benchmark = manager.cost_controller.benchmark_salary(position)
                    print(f"\n[OK] Salary research for {position}:")
                    print(benchmark['analysis'])
                    print_token_status()

                elif choice == '9':
                    print(f"Industries: {', '.join(Config.TARGET_INDUSTRIES)}")
                    industries = input("Select industries (comma-separated): ").strip().split(',')
                    industries = [i.strip() for i in industries if i.strip()]
                    if not industries:
                        print("[WARN] At least one industry required")
                        continue
                    comparison = manager.market_researcher.compare_industries(industries)
                    print(f"\n[OK] Industry comparison:")
                    print(comparison['comparison'])
                    print_token_status()

                elif choice == '10':
                    print("\n[CHAT] Chat Mode (type 'exit' to return to menu)")
                    while True:
                        user_input = input("\nYou: ").strip()
                        if user_input.lower() == 'exit':
                            break
                        if not user_input:
                            continue
                        response = manager.chat(user_input)
                        print(f"\nAI Ops Manager: {response}")
                    print_token_status()

                elif choice == '11':
                    print_token_status()

                elif choice == '12':
                    Config.print_config()

                else:
                    print("[WARN] Invalid option. Try again (0-12).")

            except KeyboardInterrupt:
                print("\n\n[INFO] Use option 0 to exit properly.")
                continue
            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)
                print(f"\n[ERROR] {e}")
                continue

    except KeyboardInterrupt:
        print("\n\n[INFO] Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n[ERROR] Fatal error: {e}")
        print("Check logs for details.")


if __name__ == "__main__":
    main()
