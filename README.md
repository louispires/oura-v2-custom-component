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
5. Add this repository URL: `https://github.com/louispires/oura-v2-custom-component`
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

- **Dashboards**: Display your sleep, readiness, and activity data with beautiful charts
- **Automations**: Trigger actions based on your Oura Ring data
- **Scripts**: Use sensor values in your scripts
- **Templates**: Create custom sensors based on Oura data

For dashboard examples using ApexCharts, see the [Dashboard Examples](#dashboard-examples) section below.

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

The integration polls the Oura API with a configurable update interval (default: 5 minutes). You can configure this interval:

1. Go to **Settings** → **Devices & Services**
2. Find "Oura Ring" and click **CONFIGURE**
3. Set your desired update interval (1-60 minutes)
4. Click **SUBMIT**

The integration will automatically reload with the new interval. The default 5-minute interval is optimized to:
- Provide timely updates
- Minimize API calls
- Respect Oura's rate limits

## Dashboard Examples

### Using ApexCharts Card

The [apexcharts-card](https://github.com/RomRider/apexcharts-card) is a highly customizable graphing card that works great with Oura data. Install it via HACS first.

#### Scores Overview Card

Track your sleep, readiness, and activity scores over the past week:

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Oura Scores
  show_states: true
  colorize_states: true
graph_span: 7d
span:
  end: day
all_series_config:
  type: column
  opacity: 0.7
  stroke_width: 2
  group_by:
    func: last
    duration: 1d
series:
  - entity: sensor.oura_sleep_score
    name: Sleep
    color: '#5E97F6'
  - entity: sensor.oura_readiness_score
    name: Readiness
    color: '#FFA600'
  - entity: sensor.oura_activity_score
    name: Activity
    color: '#00D9FF'
yaxis:
  - min: 0
    max: 100
    apex_config:
      tickAmount: 5
```

#### Sleep Analysis Card

Detailed sleep breakdown with durations:

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Sleep Analysis
  show_states: true
graph_span: 7d
span:
  end: day
all_series_config:
  type: column
  opacity: 0.8
  stroke_width: 0
  group_by:
    func: last
    duration: 1d
series:
  - entity: sensor.oura_deep_sleep_duration
    name: Deep
    color: '#5E97F6'
  - entity: sensor.oura_rem_sleep_duration
    name: REM
    color: '#9C27B0'
  - entity: sensor.oura_light_sleep_duration
    name: Light
    color: '#00D9FF'
  - entity: sensor.oura_awake_time
    name: Awake
    color: '#FF5252'
yaxis:
  - min: 0
    apex_config:
      tickAmount: 4
      decimalsInFloat: 1
```

#### Sleep Efficiency Trend

Monitor your sleep efficiency over time:

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Sleep Efficiency
  show_states: true
graph_span: 14d
span:
  end: day
series:
  - entity: sensor.oura_sleep_efficiency
    name: Efficiency
    color: '#4CAF50'
    stroke_width: 3
    type: line
    curve: smooth
    group_by:
      func: last
      duration: 1d
yaxis:
  - min: 0
    max: 100
    apex_config:
      tickAmount: 5
```

#### Heart Rate Monitoring

Track resting heart rate and HRV:

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Heart Health
  show_states: true
graph_span: 14d
span:
  end: day
series:
  - entity: sensor.oura_resting_heart_rate
    name: Resting HR
    color: '#E91E63'
    stroke_width: 2
    type: line
    curve: smooth
    group_by:
      func: last
      duration: 1d
    yaxis_id: hr
  - entity: sensor.oura_hrv_balance
    name: HRV Balance
    color: '#00BCD4'
    stroke_width: 2
    type: line
    curve: smooth
    group_by:
      func: last
      duration: 1d
    yaxis_id: hrv
yaxis:
  - id: hr
    min: 40
    max: 80
    apex_config:
      tickAmount: 4
      title:
        text: BPM
  - id: hrv
    opposite: true
    min: 0
    max: 100
    apex_config:
      tickAmount: 4
      title:
        text: HRV Score
```

#### Activity Summary

Daily steps and calories:

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Daily Activity
  show_states: true
graph_span: 7d
span:
  end: day
series:
  - entity: sensor.oura_steps
    name: Steps
    color: '#4CAF50'
    stroke_width: 2
    type: column
    opacity: 0.7
    group_by:
      func: last
      duration: 1d
    yaxis_id: steps
  - entity: sensor.oura_active_calories
    name: Calories
    color: '#FF9800'
    stroke_width: 2
    type: line
    curve: smooth
    group_by:
      func: last
      duration: 1d
    yaxis_id: calories
yaxis:
  - id: steps
    apex_config:
      tickAmount: 4
      title:
        text: Steps
  - id: calories
    opposite: true
    apex_config:
      tickAmount: 4
      title:
        text: Calories
```

#### Temperature Deviation

Track body temperature trends:

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Temperature Deviation
  show_states: true
graph_span: 30d
span:
  end: day
series:
  - entity: sensor.oura_temperature_deviation
    name: Deviation
    color: '#FF5722'
    stroke_width: 2
    type: line
    curve: smooth
    group_by:
      func: last
      duration: 1d
yaxis:
  - min: -2
    max: 2
    apex_config:
      tickAmount: 4
      decimalsInFloat: 1
```

### Simple Entity Cards

For a quick overview without ApexCharts:

```yaml
type: entities
title: Oura Ring Summary
entities:
  - entity: sensor.oura_sleep_score
    name: Sleep Score
  - entity: sensor.oura_readiness_score
    name: Readiness Score
  - entity: sensor.oura_activity_score
    name: Activity Score
  - type: divider
  - entity: sensor.oura_total_sleep_duration
    name: Total Sleep
  - entity: sensor.oura_deep_sleep_duration
    name: Deep Sleep
  - entity: sensor.oura_rem_sleep_duration
    name: REM Sleep
  - type: divider
  - entity: sensor.oura_steps
    name: Steps Today
  - entity: sensor.oura_active_calories
    name: Active Calories
```

### Gauge Cards

Visual representation of your scores:

```yaml
type: horizontal-stack
cards:
  - type: gauge
    entity: sensor.oura_sleep_score
    name: Sleep
    needle: true
    min: 0
    max: 100
    severity:
      green: 85
      yellow: 70
      red: 0
  - type: gauge
    entity: sensor.oura_readiness_score
    name: Readiness
    needle: true
    min: 0
    max: 100
    severity:
      green: 85
      yellow: 70
      red: 0
  - type: gauge
    entity: sensor.oura_activity_score
    name: Activity
    needle: true
    min: 0
    max: 100
    severity:
      green: 85
      yellow: 70
      red: 0
```

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

1. Check the [Issues](https://github.com/louispires/oura-v2-custom-component/issues) page
2. Create a new issue with detailed information
3. Include relevant logs from Home Assistant

## Disclaimer

This is an unofficial integration and is not affiliated with or endorsed by Oura Health Oy.
