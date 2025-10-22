# CRITICAL FIX: Redirect URI Mismatch

## The Problem

Home Assistant is sending:
- redirect_uri: https://my.home-assistant.io/redirect/oauth

But your Oura application only has:
- redirect_uri: https://homeassistant.mydomain.com/auth/external/callback

When you access Home Assistant through https://my.home-assistant.io, it uses the My Home Assistant redirect service.

## The Solution

You need to add BOTH redirect URIs to your Oura application:

### Step 1: Update Your Oura Application

1. Go to: https://cloud.ouraring.com/applications
2. Find your Home Assistant application
3. Click Edit
4. Update the Redirect URI field to include BOTH:

**Option A: If it allows multiple URIs (comma or space separated):**
`
https://homeassistant.mydomain.com/auth/external/callback
https://my.home-assistant.io/redirect/oauth
`

**Option B: If it only allows one URI, use:**
`
https://my.home-assistant.io/redirect/oauth
`

This is the recommended option because it works from anywhere.

### Step 2: How to Access Your Home Assistant

When configuring the integration, make sure you're accessing Home Assistant via:

**Option A: Direct URL (if you added both URIs)**
- Access HA at: https://homeassistant.mydomain.com
- This will use: https://homeassistant.mydomain.com/auth/external/callback

**Option B: My Home Assistant (recommended)**
- Access HA at: https://my.home-assistant.io
- This will use: https://my.home-assistant.io/redirect/oauth
- This works from anywhere, even outside your network

### Step 3: In Your Oura Application Settings

Your Oura application should look like this:

**Application Name:** Home Assistant

**Website URL:** https://homeassistant.mydomain.com

**Redirect URI:** 
- If multiple allowed: Both URLs above
- If single only: https://my.home-assistant.io/redirect/oauth

**Scopes:** Select all:
-  email
-  personal  
-  daily
-  heartrate
-  workout
-  session
-  tag (optional)
-  spo2 (optional)
-  ring_configuration (optional)
-  stress (optional)

### Step 4: After Updating Oura

1. Save your changes in Oura Cloud
2. Go back to Home Assistant
3. Settings  Devices & Services
4. Try adding the Oura Ring integration again
5. It should now redirect properly

## Alternative: Access HA Directly

If you want to use your direct URL instead of my.home-assistant.io:

1. Make sure Oura has: https://homeassistant.mydomain.com/auth/external/callback
2. Access Home Assistant at: https://homeassistant.mydomain.com (NOT through my.home-assistant.io)
3. Then add the integration

## Which Method to Choose?

**Use my.home-assistant.io redirect** if:
-  You access HA from different networks
-  You want it to work everywhere
-  You use Nabu Casa

**Use direct URL** if:
-  You only access HA from home network
-  You have a stable external URL
-  You prefer direct connection

**Best Practice:** Add BOTH redirect URIs to Oura so it works either way!
