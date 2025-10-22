# Oura Ring v2 Integration

A modern Home Assistant custom integration for Oura Ring using the v2 API with OAuth2 authentication.

## Features

✅ **OAuth2 Authentication** - Secure authentication using Home Assistant's application credentials
✅ **Comprehensive Data** - Access all Oura Ring data including sleep, readiness, and activity metrics
✅ **Configurable Updates** - Data refresh interval configurable from 1-60 minutes (default: 5 minutes)
✅ **Modern Architecture** - Built following the latest Home Assistant standards
✅ **Custom Branding** - Includes Oura Ring icon for visual identification

## Quick Start

After installation:

1. **Create Oura Application**
   - Go to [Oura Cloud](https://cloud.ouraring.com/applications)
   - Create a new application
   - Save your Client ID and Client Secret

2. **Configure Application Credentials**
   - In Home Assistant: Settings  Devices & Services  Application Credentials
   - Add your Oura credentials

3. **Add Integration**
   - Settings  Devices & Services  Add Integration
   - Search for "Oura Ring"
   - Follow the OAuth flow

## Available Sensors

### Sleep (10 sensors)
Sleep Score, Total/Deep/REM/Light Sleep Duration, Awake Time, Sleep Efficiency, Restfulness, Latency, Timing

### Readiness (4 sensors)
Readiness Score, Temperature Deviation, Resting Heart Rate, HRV Balance

### Activity (8 sensors)
Activity Score, Steps, Active/Total/Target Calories, High/Medium/Low Activity Time

## Support

For issues, questions, or feature requests, please visit the [GitHub repository](https://github.com/louispires/oura-v2-custom-component/issues).
