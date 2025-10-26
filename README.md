﻿# Oura Ring v2 Custom Component for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![Validate](https://github.com/louispires/oura-v2-custom-component/actions/workflows/validate.yml/badge.svg)](https://github.com/louispires/oura-v2-custom-component/actions/workflows/validate.yml)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-yellow.svg)](https://buymeacoffee.com/louispires)

A modern Home Assistant custom integration for Oura Ring using the v2 API with OAuth2 authentication.

## Features

- **OAuth2 Authentication**: Secure authentication using Home Assistant's application credentials
- **Comprehensive Data**: Access all Oura Ring data including sleep, readiness, and activity metrics
- **HACS Compatible**: Easy installation and updates via HACS
- **Modern Architecture**: Built following the latest Home Assistant standards (2025)
- **Efficient Updates**: Uses DataUpdateCoordinator for optimal data fetching

## Available Sensors

### Sleep Sensors (13)
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
- Deep Sleep Percentage
- REM Sleep Percentage
- Time in Bed

### Readiness Sensors (4)
- Readiness Score
- Temperature Deviation
- Resting Heart Rate Score (contribution score, not actual BPM)*
- HRV Balance Score (contribution score, not actual HRV)*

**Note**: Sensors marked with * may be unavailable if Oura doesn't have sufficient data to calculate the contributor score.

### Activity Sensors (8)
- Activity Score
- Steps
- Active Calories
- Total Calories
- Target Calories
- High Activity Time
- Medium Activity Time
- Low Activity Time

### Heart Rate Sensors (4)
- Current Heart Rate (latest reading)
- Average Heart Rate (from recent readings)
- Minimum Heart Rate (from recent readings)
- Maximum Heart Rate (from recent readings)

### HRV Sensors (1)
- Average Sleep HRV (heart rate variability during sleep)

**Total: 30 sensors**

## Installation

### HACS Installation (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=louispires&repository=oura-v2-custom-component&category=integration)

**Click the button above** to add this repository to HACS, or follow these manual steps:

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
<img width="947" height="804" alt="image" src="https://github.com/user-attachments/assets/13fafd56-db90-40a5-9f3f-99c12ee74707" />
<details>
<summary>yaml</summary>
   
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
  stroke_width: 8
  group_by:
    func: last
    duration: 1d
series:
  - entity: sensor.oura_sleep_score
    name: Sleep
    color: "#5E97F6"
  - entity: sensor.oura_readiness_score
    name: Readiness
    color: "#FFA600"
  - entity: sensor.oura_activity_score
    name: Activity
    color: "#00D9FF"
yaxis:
  - min: 0
    max: 100
    apex_config:
      tickAmount: 5
```
</details>

#### Sleep Analysis Card

Detailed sleep breakdown with durations:
<img width="2904" height="1243" alt="image" src="https://github.com/user-attachments/assets/a9731cbe-41f9-4d83-8648-98befd82f344" />
<details>
<summary>yaml</summary>

```yaml
type: custom:apexcharts-card
graph_span: 7d
header:
  show: true
  show_states: true
  colorize_states: true
  title: Sleep
  standard_format: true
yaxis:
  - id: left
    opposite: false
    min: 0
    max: 10
    apex_config:
      title:
        text: Total Sleep
  - id: right
    opposite: true
    min: 0
    max: 8
    apex_config:
      title:
        text: Breakdown
series:
  - entity: sensor.oura_sleep_score
    name: Score
    show:
      in_chart: false
    color: white
  - entity: sensor.oura_average_heart_rate
    name: Avg HR
    show:
      in_chart: false
  - entity: sensor.oura_minimum_heart_rate
    name: Lowest HR
    show:
      in_chart: false
  - entity: sensor.oura_time_in_bed
    name: In Bed
    color: grey
    type: area
    show:
      in_chart: true
      in_header: false
    yaxis_id: left
    group_by:
      duration: 1d
      func: last
  - entity: sensor.oura_total_sleep_duration
    name: Total Sleep
    color: purple
    type: area
    show:
      in_chart: true
      in_header: false
    yaxis_id: left
    group_by:
      duration: 1d
      func: last
  - entity: sensor.oura_rem_sleep_duration
    name: REM
    color: "#20bf6b"
    type: column
    show:
      in_chart: true
      in_header: false
    yaxis_id: right
    group_by:
      duration: 1d
      func: last
  - entity: sensor.oura_deep_sleep_duration
    name: Deep
    color: "#45aaf2"
    type: column
    show:
      in_chart: true
      in_header: false
    yaxis_id: right
    group_by:
      duration: 1d
      func: last
  - entity: sensor.oura_light_sleep_duration
    name: Light
    color: "#fed330"
    type: column
    show:
      in_chart: true
      in_header: false
    yaxis_id: right
    group_by:
      duration: 1d
      func: last
  - entity: sensor.oura_awake_time
    name: Awake
    color: "#fc5c65"
    type: column
    show:
      in_chart: true
      in_header: false
    yaxis_id: right
    group_by:
      duration: 1d
      func: last
```
</details>

#### Sleep Efficiency Trend

Monitor your sleep efficiency over time:
<img width="945" height="797" alt="image" src="https://github.com/user-attachments/assets/23d9d8cd-44ce-4944-8d21-292829208123" />
<details>
<summary>yaml</summary>
   
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
</details>

#### Heart Rate Monitoring

Track heart rate scores and HRV:
<img width="947" height="800" alt="image" src="https://github.com/user-attachments/assets/57401ffc-988c-4912-a71a-a81f686739f5" />
<details>
<summary>yaml</summary>
   
```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Heart Health
  show_states: true
graph_span: 7d
span:
  end: day
series:
  - entity: sensor.oura_resting_heart_rate
    name: Resting HR
    color: "#E91E63"
    stroke_width: 2
    type: line
    curve: smooth
    group_by:
      func: last
      duration: 1d
    yaxis_id: hr
  - entity: sensor.oura_hrv_balance
    name: HRV Balance
    color: "#00BCD4"
    stroke_width: 2
    type: line
    curve: smooth
    group_by:
      func: last
      duration: 1d
    yaxis_id: hrv
  - entity: sensor.oura_average_sleep_hrv
    name: Sleep HRV
    color: "#287233"
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
        text: HRV
```
</details>

#### Activity Summary

Daily steps and calories:
<img width="938" height="803" alt="image" src="https://github.com/user-attachments/assets/675d862e-47dd-4772-a1c9-dab482d145ce" />
<details>
<summary>yaml</summary>
   
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
</details>

#### Temperature Deviation

Track body temperature trends:
<img width="942" height="800" alt="image" src="https://github.com/user-attachments/assets/bb79c360-90c9-45b0-ac33-a96f7cc2ae9c" />
<details>
<summary>yaml</summary>
   
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
</details>

### Simple Entity Cards

For a quick overview without ApexCharts:
<img width="946" height="1471" alt="image" src="https://github.com/user-attachments/assets/ac3462db-f6a0-417d-b1f4-cca43335e4cd" />
<details>
<summary>yaml</summary>
   
```yaml
type: entities
title: Oura Ring Summary
entities:
  - entity: sensor.oura_sleep_score
    secondary_info: last-changed
    name: Sleep Score
  - entity: sensor.oura_readiness_score
    secondary_info: last-changed
    name: Readiness Score
  - entity: sensor.oura_activity_score
    secondary_info: last-changed
    name: Activity Score
  - type: divider
  - entity: sensor.oura_total_sleep_duration
    secondary_info: last-changed
    name: Total Sleep
  - entity: sensor.oura_time_in_bed
    name: Time in Bed
    secondary_info: last-changed
  - entity: sensor.oura_deep_sleep_duration
    secondary_info: last-changed
    name: Deep Sleep
  - entity: sensor.oura_rem_sleep_duration
    secondary_info: last-changed
    name: REM Sleep
  - type: divider
  - entity: sensor.oura_steps
    secondary_info: last-changed
    name: Steps Today
  - entity: sensor.oura_active_calories
    secondary_info: last-changed
    name: Active Calories
  - entity: sensor.oura_current_heart_rate
    secondary_info: last-changed
  - entity: sensor.oura_average_heart_rate
    secondary_info: last-changed
  - entity: sensor.oura_minimum_heart_rate
    secondary_info: last-changed
  - entity: sensor.oura_maximum_heart_rate
    secondary_info: last-changed
```
</details>

### Gauge Cards

Visual representation of your scores:
<img width="905" height="228" alt="image" src="https://github.com/user-attachments/assets/bc8666fd-856c-4fd5-b05e-68e587b6b2ce" />
<details>
<summary>yaml</summary>
   
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
</details>

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
3. Wait for the next update cycle (default: 5 minutes)
4. Check Home Assistant logs for errors

### Unavailable Sensors

Some sensors may show as "unavailable" when Oura doesn't have sufficient data:

- **Resting Heart Rate Score**: Requires sufficient heart rate measurements during rest periods
- **HRV Balance Score**: Requires sufficient HRV data collection (usually from sleep)

This is normal behavior, especially:
- In the first few days of wearing your ring
- After periods of not wearing the ring
- If you haven't had sufficient sleep for HRV measurements
- During data processing delays

These sensors will automatically become available once Oura collects and processes the necessary data.

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

Contributions are welcome! Please read our [Contributing Guide](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions
- **[Quick Reference](docs/QUICKREF.md)** - Quick reference for common tasks
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Redirect URI Fix](docs/FIXING_REDIRECT_URI.md)** - OAuth redirect URI troubleshooting
- **[Project Summary](docs/PROJECT_SUMMARY.md)** - Technical overview and architecture

## License

This project is licensed under the MIT License.

## Credits

- Original Oura Component: [nitobuendia/oura-custom-component](https://github.com/nitobuendia/oura-custom-component)
- Oura Ring API: [Oura Cloud API Documentation](https://cloud.ouraring.com/v2/docs)
- Development assisted by: Claude Sonnet 4.5 (Anthropic AI)

## Sponsoring

If this integration is helpful, feel free to [Buy Me a Coffee](https://buymeacoffee.com/louispires); or check other options on the Github ❤️ Sponsor link on the top of this page.

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/louispires)

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/louispires/oura-v2-custom-component/issues) page
2. Create a new issue with detailed information
3. Include relevant logs from Home Assistant

## Disclaimer

This is an unofficial integration and is not affiliated with or endorsed by Oura Health Oy.
