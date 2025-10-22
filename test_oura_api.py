"""Test script for Oura API v2."""
import asyncio
import aiohttp
from datetime import datetime, timedelta
import json


# Replace with your actual access token from Home Assistant
# You can find it in: .storage/application_credentials or in the logs
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"

API_BASE_URL = "https://api.ouraring.com/v2/usercollection"


async def test_oura_api():
    """Test Oura API endpoints."""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=1)
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }
    
    async with aiohttp.ClientSession() as session:
        # Test sleep endpoint
        print(f"\n{'='*60}")
        print("Testing Sleep Endpoint")
        print(f"{'='*60}")
        url = f"{API_BASE_URL}/daily_sleep"
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        print(f"URL: {url}")
        print(f"Params: {params}")
        
        async with session.get(url, headers=headers, params=params) as response:
            print(f"Status: {response.status}")
            sleep_data = await response.json()
            print(f"Response:\n{json.dumps(sleep_data, indent=2)}")
        
        # Test readiness endpoint
        print(f"\n{'='*60}")
        print("Testing Readiness Endpoint")
        print(f"{'='*60}")
        url = f"{API_BASE_URL}/daily_readiness"
        async with session.get(url, headers=headers, params=params) as response:
            print(f"Status: {response.status}")
            readiness_data = await response.json()
            print(f"Response:\n{json.dumps(readiness_data, indent=2)}")
        
        # Test activity endpoint
        print(f"\n{'='*60}")
        print("Testing Activity Endpoint")
        print(f"{'='*60}")
        url = f"{API_BASE_URL}/daily_activity"
        async with session.get(url, headers=headers, params=params) as response:
            print(f"Status: {response.status}")
            activity_data = await response.json()
            print(f"Response:\n{json.dumps(activity_data, indent=2)}")
        
        print(f"\n{'='*60}")
        print("Data Summary")
        print(f"{'='*60}")
        print(f"Sleep records: {len(sleep_data.get('data', []))}")
        print(f"Readiness records: {len(readiness_data.get('data', []))}")
        print(f"Activity records: {len(activity_data.get('data', []))}")


if __name__ == "__main__":
    print("Oura API v2 Test Script")
    print("="*60)
    
    if ACCESS_TOKEN == "YOUR_ACCESS_TOKEN_HERE":
        print("\nERROR: Please replace ACCESS_TOKEN with your actual token")
        print("\nTo get your token:")
        print("1. In Home Assistant, enable debug logging for oura")
        print("2. Check logs after the integration fetches data")
        print("3. Look for the Bearer token in the Authorization header")
        print("\nOr check: /config/.storage/application_credentials")
        exit(1)
    
    asyncio.run(test_oura_api())
