"""
Deploy Postman Flow via MCP Router
Triggers a Postman Flow execution through the MCP Router API
"""

import os
import requests
import json
from typing import Dict, Optional
from datetime import datetime

class PostmanFlowMCPDeployer:
    """Deploys and triggers Postman Flows via MCP Router."""
    
    def __init__(self, mcp_router_url: Optional[str] = None, mcp_api_key: Optional[str] = None):
        """
        Initialize the MCP Router deployer.
        
        Args:
            mcp_router_url: MCP Router base URL. Defaults to Railway deployment.
            mcp_api_key: MCP Router API key. If not provided, checks MCP_API_KEY env var.
        """
        self.mcp_router_url = mcp_router_url or os.getenv(
            'MCP_ROUTER_URL',
            'https://mcp-router-production.up.railway.app'
        )
        self.mcp_api_key = mcp_api_key or os.getenv('MCP_API_KEY')
        
        if not self.mcp_api_key:
            print("Warning: MCP_API_KEY not set. Some endpoints may require authentication.")
        
        self.headers = {
            "Content-Type": "application/json"
        }
        
        if self.mcp_api_key:
            self.headers["X-API-Key"] = self.mcp_api_key
    
    def health_check(self) -> bool:
        """Check if MCP Router is available."""
        try:
            url = f"{self.mcp_router_url}/health"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Health check failed: {e}")
            return False
    
    def trigger_postman_flow(self, flow_id: str, trigger_data: Optional[Dict] = None) -> Dict:
        """
        Trigger a Postman Flow execution.
        
        Note: This assumes the MCP Router has an endpoint to trigger Postman Flows.
        If not, this would need to be implemented in the MCP Router.
        
        Args:
            flow_id: The Postman Flow ID to trigger
            trigger_data: Optional data to pass to the flow
        
        Returns:
            Response from the MCP Router
        """
        # This endpoint would need to be implemented in MCP Router
        # For now, we'll create a generic webhook trigger endpoint
        url = f"{self.mcp_router_url}/webhooks/postman-flow/{flow_id}"
        
        payload = {
            "flow_id": flow_id,
            "timestamp": datetime.now().isoformat(),
            "data": trigger_data or {}
        }
        
        response = requests.post(url, headers=self.headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def test_ghl_integration(self, flow_id: str) -> Dict:
        """
        Test the GHL integration flow.
        
        This sends a test request to verify the flow is working with updated variables.
        """
        print(f"Testing Postman Flow: {flow_id}")
        print("This will trigger the flow with test data...")
        
        test_data = {
            "test": True,
            "contact_id": os.getenv('GHL_TEST_CONTACT_ID', 'test-contact'),
            "message": "Test message from MCP Router deployment"
        }
        
        return self.trigger_postman_flow(flow_id, test_data)


def create_mcp_router_webhook_handler():
    """
    Create a webhook handler script for MCP Router to handle Postman Flow triggers.
    
    This would be added to the MCP Router codebase to handle Postman Flow webhooks.
    """
    handler_code = '''
"""
MCP Router Webhook Handler for Postman Flows
Add this to your MCP Router main.py or create a new routes file
"""

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
import requests
import os

router = APIRouter()

class PostmanFlowTrigger(BaseModel):
    flow_id: str
    data: Optional[dict] = None

@router.post("/webhooks/postman-flow/{flow_id}")
async def trigger_postman_flow(
    flow_id: str,
    trigger: PostmanFlowTrigger,
    x_api_key: Optional[str] = Header(None)
):
    """
    Trigger a Postman Flow via webhook.
    
    This endpoint receives webhook calls and forwards them to Postman Flow API.
    """
    # Verify API key if required
    expected_key = os.getenv('MCP_API_KEY')
    if expected_key and x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Get Postman API key
    postman_api_key = os.getenv('POSTMAN_API_KEY')
    if not postman_api_key:
        raise HTTPException(
            status_code=500,
            detail="Postman API key not configured"
        )
    
    # Trigger the Postman Flow
    # Note: Postman Flows API may require different endpoints
    # This is a placeholder - adjust based on actual Postman Flow API
    postman_url = f"https://api.getpostman.com/flows/{flow_id}/run"
    
    headers = {
        "X-Api-Key": postman_api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            postman_url,
            headers=headers,
            json=trigger.data or {},
            timeout=30
        )
        response.raise_for_status()
        return {
            "success": True,
            "flow_id": flow_id,
            "response": response.json()
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to trigger Postman Flow: {str(e)}"
        )
'''
    
    return handler_code


def main():
    """Main deployment function."""
    print("=" * 60)
    print("POSTMAN FLOW MCP ROUTER DEPLOYMENT")
    print("=" * 60)
    print()
    
    FLOW_ID = "69755954010ddb0014f502dc"
    
    deployer = PostmanFlowMCPDeployer()
    
    # Check MCP Router health
    print("Checking MCP Router health...")
    if not deployer.health_check():
        print("❌ MCP Router is not available")
        print(f"   URL: {deployer.mcp_router_url}")
        print("\nTroubleshooting:")
        print("1. Verify MCP Router is deployed and running")
        print("2. Check the MCP_ROUTER_URL environment variable")
        print("3. Verify network connectivity")
        return False
    
    print("✅ MCP Router is available")
    print()
    
    # Test the flow
    print("Testing Postman Flow integration...")
    try:
        result = deployer.test_ghl_integration(FLOW_ID)
        print("✅ Flow triggered successfully!")
        print(f"Response: {json.dumps(result, indent=2)}")
        return True
    except Exception as e:
        print(f"⚠️  Flow trigger test failed: {e}")
        print("\nNote: The webhook endpoint may need to be implemented in MCP Router.")
        print("See create_mcp_router_webhook_handler() for implementation code.")
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
