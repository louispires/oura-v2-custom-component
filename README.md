# Oura Ring v2 Custom Component for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A modern Home Assistant custom integration for Oura Ring using the v2 API with OAuth2 authentication.

## Features

- **OAuth2 Authentication**: Secure authentication using Home Assistant's application credentials
- **Comprehensive Data**: Access all Oura Ring data including sleep, readiness, and activity metrics
- **HACS Compatible**: Easy installation and updates via HACS
- **Modern Architecture**: Built following the latest Home Assistant standards (2025)
- **Efficient Updates**: Uses DataUpdateCoordinator for optimal data fetching

## Available Sensors

### Sleep Sensors
- Sleep Score
- Total Sleep Duration
- Deep Sleep Duration
- REM Sleep Duration
- Light Sleep Duration
- Awake Time
- Sleep Efficiency
- Restfulness
- Sleep Latency
- Sleep Timing

### Readiness Sensors
- Readiness Score
- Temperature Deviation
- Resting Heart Rate
- HRV Balance

### Activity Sensors
- Activity Score
- Steps
- Active Calories
- Total Calories
- Target Calories
- High Activity Time
- Medium Activity Time
- Low Activity Time

## Installation

### HACS Installation (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/yourusername/oura-v2-custom-component`
6. Select category: "Integration"
7. Click "Add"
8. Find "Oura Ring" in the integration list and click "Download"
9. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/oura` directory to your `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

### Step 1: Create Oura Application

1. Go to [Oura Cloud](https://cloud.ouraring.com/applications)
2. Sign in with your Oura account
3. Click "Create a New Application"
4. Fill in the application details:
   - **Application Name**: Home Assistant
   - **Application Website**: Your Home Assistant URL
   - **Redirect URI**: `https://your-home-assistant-url/auth/external/callback`
5. Save the **Client ID** and **Client Secret**

### Step 2: Configure Application Credentials in Home Assistant

1. In Home Assistant, go to **Settings** → **Devices & Services**
2. Click on **Application Credentials** (in the top menu)
3. Click **Add Application Credential**
4. **Note**: You may see either a dropdown to select "Oura Ring" OR a generic form - both work!
5. Enter your **Client ID** and **Client Secret** from Step 1
6. Click **Create**

**Important**: Application Credentials is just for storing OAuth credentials. You won't see Oura Ring listed as an active integration here.

### Step 3: Add Oura Ring Integration

**Now** you can add the actual integration:

1. In Home Assistant, go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Oura Ring" - **you should see it here!**
4. Click on it and follow the OAuth2 authentication flow
5. You'll be redirected to Oura's website to authorize the integration
6. After authorization, you'll be redirected back to Home Assistant
7. The integration will be configured and sensors will start appearing

## Usage

Once configured, sensors will appear under the Oura Ring integration. You can use these sensors in:

- **Dashboards**: Display your sleep, readiness, and activity data
- **Automations**: Trigger actions based on your Oura Ring data
- **Scripts**: Use sensor values in your scripts
- **Templates**: Create custom sensors based on Oura data

### Example Dashboard Card

```yaml
type: entities
title: Oura Ring
entities:
  - entity: sensor.oura_sleep_score
  - entity: sensor.oura_readiness_score
  - entity: sensor.oura_activity_score
  - entity: sensor.oura_total_sleep_duration
  - entity: sensor.oura_steps
```

### Example Automation

```yaml
automation:
  - alias: "Low Sleep Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.oura_sleep_score
        below: 70
    action:
      - service: notify.mobile_app
        data:
          message: "Your sleep score is low. Consider resting today."
```

## Data Update Frequency

The integration polls the Oura API every 30 minutes to fetch the latest data. This interval is optimized to:
- Minimize API calls
- Provide timely updates
- Respect Oura's rate limits

## Troubleshooting

### Authentication Issues

If you encounter authentication issues:

1. Verify your Client ID and Client Secret are correct
2. Ensure the Redirect URI matches exactly in both Oura Cloud and Home Assistant
3. Check Home Assistant logs for specific error messages
4. Try removing and re-adding the integration

### Missing Sensors

If some sensors are not appearing:

1. Ensure your Oura Ring is synced with the Oura app
2. Check that you have recent data in the Oura app
3. Wait for the next update cycle (30 minutes)
4. Check Home Assistant logs for errors

### API Rate Limiting

If you see rate limiting errors:

- The integration is designed to respect Oura's API limits
- Avoid manually triggering updates too frequently
- Check if you have other integrations also accessing the Oura API

## Development

This integration is built using modern Home Assistant patterns:

- **OAuth2 Flow**: Uses Home Assistant's built-in OAuth2 implementation
- **DataUpdateCoordinator**: Efficient data fetching and update management
- **Type Hints**: Full type hint coverage for better code quality
- **Async**: All operations are asynchronous
- **Error Handling**: Comprehensive error handling and logging

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Credits

- Original Oura Component: [johro897/oura-custom-component](https://github.com/johro897/oura-custom-component)
- Oura Ring API: [Oura Cloud API Documentation](https://cloud.ouraring.com/v2/docs)

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/oura-v2-custom-component/issues) page
2. Create a new issue with detailed information
3. Include relevant logs from Home Assistant

## Disclaimer

This is an unofficial integration and is not affiliated with or endorsed by Oura Health Oy.
