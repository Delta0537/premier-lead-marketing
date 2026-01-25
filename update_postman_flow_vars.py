"""
Update Postman Flow Configuration Variables
Updates environment/configuration variables in a Postman Flow via the Postman API
"""

import os
import requests
import json
from typing import Dict, Optional

class PostmanFlowUpdater:
    """Manages Postman Flow configuration variable updates."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Postman Flow Updater.
        
        Args:
            api_key: Postman API key. If not provided, will check POSTMAN_API_KEY env var.
        """
        self.api_key = api_key or os.getenv('POSTMAN_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Postman API key not found. Set POSTMAN_API_KEY environment variable or pass it to __init__"
            )
        
        self.base_url = "https://api.getpostman.com"
        self.headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def get_flow(self, flow_id: str) -> Dict:
        """Get flow details."""
        # Try different possible endpoints for Postman Flows
        endpoints = [
            f"{self.base_url}/flows/{flow_id}",
            f"{self.base_url}/v1/flows/{flow_id}",
            f"{self.base_url}/api/flows/{flow_id}",
        ]
        
        for url in endpoints:
            try:
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    return response.json()
            except:
                continue
        
        # If all endpoints fail, raise an error
        raise requests.exceptions.HTTPError(
            f"Flow not found. Postman Flows may not have a public API endpoint. "
            f"Please update variables manually in Postman UI."
        )
    
    def update_flow_configuration(self, flow_id: str, variable_updates: Dict[str, Dict]) -> Dict:
        """
        Update flow configuration variables.
        
        Args:
            flow_id: The Postman Flow ID
            variable_updates: Dict mapping variable IDs to their update data
                Example: {
                    "vq0LPMl6": {"value": "new-value", "type": "secret"},
                    "qDnQBK2f": {"value": "new-value", "type": "string"}
                }
        
        Returns:
            Updated flow configuration
        """
        # First, get the current flow to understand its structure
        flow = self.get_flow(flow_id)
        
        # Try different API endpoints for updating flow configurations
        endpoints_to_try = [
            f"{self.base_url}/flows/{flow_id}/configurations",
            f"{self.base_url}/flows/{flow_id}",
        ]
        
        # Build the update payload
        # Postman API typically expects configuration updates in a specific format
        update_payload = {
            "configurations": []
        }
        
        for var_id, var_data in variable_updates.items():
            update_payload["configurations"].append({
                "id": var_id,
                "value": var_data["value"],
                "type": var_data.get("type", "string")
            })
        
        # Try different possible endpoints for updating configurations
        endpoints = [
            f"{self.base_url}/flows/{flow_id}/configurations",
            f"{self.base_url}/v1/flows/{flow_id}/configurations",
            f"{self.base_url}/api/flows/{flow_id}/configurations",
        ]
        
        last_error = None
        for url in endpoints:
            try:
                response = requests.patch(url, headers=self.headers, json=update_payload)
                if response.status_code == 200:
                    return response.json()
            except requests.exceptions.HTTPError as e:
                last_error = e
                continue
        
        # If all endpoints fail, try updating the entire flow
        if last_error and hasattr(last_error, 'response') and last_error.response.status_code == 404:
            # If that fails, try updating the entire flow
            if response.status_code == 404:
                # Try updating the flow directly
                flow_data = flow.get("flow", {})
                configurations = flow_data.get("configurations", [])
                
                # Update configurations in the flow data
                for config in configurations:
                    if config.get("id") in variable_updates:
                        var_data = variable_updates[config["id"]]
                        config["value"] = var_data["value"]
                        if "type" in var_data:
                            config["type"] = var_data["type"]
                
                # Update the flow
                update_url = f"{self.base_url}/flows/{flow_id}"
                update_payload = {"flow": flow_data}
                response = requests.patch(update_url, headers=self.headers, json=update_payload)
                response.raise_for_status()
                return response.json()
            else:
                raise
    
    def update_variables(self, flow_id: str, variables: Dict[str, Dict]) -> bool:
        """
        Convenience method to update multiple variables.
        
        Args:
            flow_id: The Postman Flow ID
            variables: Dict mapping variable names to their values and types
                Example: {
                    "GHL_API_KEY": {"value": "pit-...", "type": "secret"},
                    "GHL_LOCATION_ID": {"value": "4X72...", "type": "string"}
                }
        
        Returns:
            True if successful
        """
        # First, get the flow to find variable IDs by name
        flow = self.get_flow(flow_id)
        flow_data = flow.get("flow", {})
        configurations = flow_data.get("configurations", [])
        
        # Map variable names to IDs
        name_to_id = {config.get("name"): config.get("id") for config in configurations}
        
        # Build update dict with variable IDs
        variable_updates = {}
        for var_name, var_data in variables.items():
            if var_name in name_to_id:
                variable_updates[name_to_id[var_name]] = var_data
            else:
                print(f"Warning: Variable '{var_name}' not found in flow configurations")
        
        if not variable_updates:
            print("No variables found to update")
            return False
        
        # Update the variables
        result = self.update_flow_configuration(flow_id, variable_updates)
        print(f"Successfully updated {len(variable_updates)} variables")
        return True


def main():
    """Main function to update Postman Flow variables."""
    import sys
    import io
    import sys
    
    # Fix Windows console encoding for emojis
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    # Flow ID from user
    FLOW_ID = "69755954010ddb0014f502dc"
    
    # Variables to update
    VARIABLES = {
        "GHL_API_KEY": {
            "value": "pit-81ca6da4-c48f-4d4d-887e-a6d35bca70a5",
            "type": "secret"
        },
        "GHL_LOCATION_ID": {
            "value": "4X72lI7IBpK9tJOdKwOf",
            "type": "string"
        }
    }
    
    # Alternative: Update by variable ID directly
    VARIABLE_UPDATES_BY_ID = {
        "vq0LPMl6": {  # GHL_API_KEY
            "value": "pit-81ca6da4-c48f-4d4d-887e-a6d35bca70a5",
            "type": "secret"
        },
        "qDnQBK2f": {  # GHL_LOCATION_ID
            "value": "4X72lI7IBpK9tJOdKwOf",
            "type": "string"
        }
    }
    
    print("=" * 60)
    print("POSTMAN FLOW CONFIGURATION VARIABLE UPDATER")
    print("=" * 60)
    print()
    
    # Check for API key
    api_key = os.getenv('POSTMAN_API_KEY')
    if not api_key:
        print("ERROR: POSTMAN_API_KEY not found in environment")
        print("\nTo set it:")
        print("  PowerShell: $env:POSTMAN_API_KEY='your-api-key'")
        print("  Permanent: [System.Environment]::SetEnvironmentVariable('POSTMAN_API_KEY', 'your-api-key', 'User')")
        print("\nGet your API key from: https://postman.com/settings/me/api-keys")
        return False
    
    try:
        updater = PostmanFlowUpdater(api_key=api_key)
        
        print(f"Flow ID: {FLOW_ID}")
        print(f"Variables to update: {len(VARIABLE_UPDATES_BY_ID)}")
        print()
        
        # Try updating by variable ID first (more direct)
        print("Attempting to update variables by ID...")
        try:
            result = updater.update_flow_configuration(FLOW_ID, VARIABLE_UPDATES_BY_ID)
            print("[SUCCESS] Successfully updated variables by ID!")
            print(f"Response: {json.dumps(result, indent=2)}")
            return True
        except Exception as e:
            print(f"[WARNING] Update by ID failed: {e}")
            print("\nTrying alternative method (by variable name)...")
            
            # Fallback: Try updating by variable name
            try:
                success = updater.update_variables(FLOW_ID, VARIABLES)
                if success:
                    print("✅ Successfully updated variables by name!")
                    return True
                else:
                    print("❌ Failed to update variables")
                    return False
            except Exception as e2:
                print(f"[ERROR] Alternative method also failed: {e2}")
                print("\n" + "=" * 60)
                print("MANUAL UPDATE INSTRUCTIONS")
                print("=" * 60)
                print("\nIf the API update fails, you can update manually:")
                print(f"1. Go to: https://postman.com/flows/{FLOW_ID}")
                print("2. Open the Flow")
                print("3. Click on the Configuration panel")
                print("4. Update the following variables:")
                print(f"   - GHL_API_KEY: pit-81ca6da4-c48f-4d4d-887e-a6d35bca70a5 (secret)")
                print(f"   - GHL_LOCATION_ID: 4X72lI7IBpK9tJOdKwOf (string)")
                return False
    
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        print("\nTroubleshooting:")
        print("1. Verify your Postman API key is correct")
        print("2. Check that the Flow ID is correct")
        print("3. Ensure you have permission to modify the flow")
        print("4. Check Postman API status: https://status.postman.com")
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
