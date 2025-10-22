# Quick Reference Guide

## Configuration URLs

- **Oura Cloud Dashboard**: https://cloud.ouraring.com
- **OAuth Applications**: https://cloud.ouraring.com/applications
- **API Documentation**: https://cloud.ouraring.com/v2/docs

## Home Assistant Paths

- **Application Credentials**: Settings  Devices & Services  Application Credentials
- **Add Integration**: Settings  Devices & Services  Add Integration
- **Logs**: Settings  System  Logs
- **Developer Tools**: Developer Tools  States

## Redirect URI Format

```
https://YOUR-HA-URL/auth/external/callback
```

### Examples:

- **Nabu Casa**: `https://abcdef12345.ui.nabu.casa/auth/external/callback`
- **DuckDNS**: `https://yourdomain.duckdns.org/auth/external/callback`
- **Local**: `http://192.168.1.100:8123/auth/external/callback`
- **Custom Domain**: `https://home.example.com/auth/external/callback`

## Required OAuth Scopes

When creating the Oura application, select these scopes:
- `daily` - Daily sleep, activity, and readiness data
- `heartrate` - Heart rate data
- `workout` - Workout sessions
- `session` - Session data
- `personal` - Personal information

## Sensor Entity IDs

### Sleep Sensors
```
sensor.oura_sleep_score
sensor.oura_total_sleep_duration
sensor.oura_deep_sleep_duration
sensor.oura_rem_sleep_duration
sensor.oura_light_sleep_duration
sensor.oura_awake_time
sensor.oura_sleep_efficiency
sensor.oura_restfulness
sensor.oura_sleep_latency
sensor.oura_sleep_timing
```

### Readiness Sensors
```
sensor.oura_readiness_score
sensor.oura_temperature_deviation
sensor.oura_resting_heart_rate
sensor.oura_hrv_balance
```

### Activity Sensors
```
sensor.oura_activity_score
sensor.oura_steps
sensor.oura_active_calories
sensor.oura_total_calories
sensor.oura_target_calories
sensor.oura_high_activity_time
sensor.oura_medium_activity_time
sensor.oura_low_activity_time
```

### Heart Rate Sensors
```
sensor.oura_current_heart_rate
sensor.oura_average_heart_rate
sensor.oura_min_heart_rate
sensor.oura_max_heart_rate
```

## Common Tasks

### Reload Integration

1. Settings  Devices & Services
2. Find "Oura Ring"
3. Click  (three dots)
4. Select "Reload"

### Remove Integration

1. Settings  Devices & Services
2. Find "Oura Ring"
3. Click  (three dots)
4. Select "Delete"

### Enable Debug Logging

Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.oura: debug
```

Then restart Home Assistant.

### View Sensor History

1. Go to any dashboard
2. Click on a sensor entity
3. View the history graph
4. Or use: Developer Tools  States  Select entity  History

## Update Schedule

- **Default Interval**: 5 minutes (configurable)
- **First Update**: Within 5 minutes of setup
- **Change Interval**: Settings → Devices & Services → Oura Ring → CONFIGURE
- **Range**: 1-60 minutes

## API Endpoints Used

The integration fetches data from these Oura v2 API endpoints:

- `https://api.ouraring.com/v2/usercollection/daily_sleep`
- `https://api.ouraring.com/v2/usercollection/daily_readiness`
- `https://api.ouraring.com/v2/usercollection/daily_activity`

## File Locations

### HACS Installation
```
config/
  custom_components/
    oura/
      __init__.py
      api.py
      application_credentials.py
      config_flow.py
      const.py
      coordinator.py
      manifest.json
      sensor.py
      strings.json
      translations/
        en.json
```

### Configuration Storage
```
config/
  .storage/
    core.config_entries
    application_credentials
```

## Troubleshooting Quick Checks

1.  Integration installed in `config/custom_components/oura/`
2.  Home Assistant restarted after installation
3.  OAuth app created in Oura Cloud
4.  Client ID and Secret added to Application Credentials
5.  Redirect URI matches exactly in both places
6.  All required scopes selected in Oura Cloud
7.  Oura Ring synced with mobile app
8.  Recent data available in Oura mobile app

## Useful YAML Snippets

### Dashboard Card - Entities
```yaml
type: entities
title: Oura Ring
entities:
  - entity: sensor.oura_sleep_score
    name: Sleep Score
  - entity: sensor.oura_readiness_score
    name: Readiness Score
  - entity: sensor.oura_activity_score
    name: Activity Score
  - entity: sensor.oura_steps
    name: Steps Today
  - entity: sensor.oura_total_sleep_duration
    name: Sleep Duration
```

### Dashboard Card - Glance
```yaml
type: glance
title: Oura Scores
entities:
  - entity: sensor.oura_sleep_score
    name: Sleep
  - entity: sensor.oura_readiness_score
    name: Readiness
  - entity: sensor.oura_activity_score
    name: Activity
```

### Automation - Low Sleep Alert
```yaml
automation:
  - alias: "Oura - Low Sleep Alert"
    trigger:
      - platform: state
        entity_id: sensor.oura_sleep_score
    condition:
      - condition: numeric_state
        entity_id: sensor.oura_sleep_score
        below: 70
    action:
      - service: notify.mobile_app
        data:
          title: "Sleep Alert"
          message: "Your sleep score is {{ states('sensor.oura_sleep_score') }}. Consider taking it easy today."
```

### Automation - Activity Goal Met
```yaml
automation:
  - alias: "Oura - Activity Goal Met"
    trigger:
      - platform: numeric_state
        entity_id: sensor.oura_steps
        above: 10000
    action:
      - service: notify.mobile_app
        data:
          title: "Great Job!"
          message: "You've reached your step goal with {{ states('sensor.oura_steps') }} steps!"
```

### Template Sensor - Sleep Quality
```yaml
template:
  - sensor:
      - name: "Oura Sleep Quality"
        unique_id: oura_sleep_quality
        state: >
          {% set score = states('sensor.oura_sleep_score') | int(0) %}
          {% if score >= 85 %}
            Excellent
          {% elif score >= 70 %}
            Good
          {% elif score >= 55 %}
            Fair
          {% else %}
            Poor
          {% endif %}
        icon: mdi:sleep
```

## Support Resources

- **Installation Guide**: [INSTALLATION.md](INSTALLATION.md)
- **Full README**: [README.md](../README.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **GitHub Issues**: https://github.com/louispires/oura-v2-custom-component/issues
- **Home Assistant Docs**: https://www.home-assistant.io/integrations/
- **Oura API Docs**: https://cloud.ouraring.com/v2/docs

## Version Information

- **Integration Version**: 1.0.0
- **Minimum HA Version**: 2024.1.0
- **API Version**: v2
- **Python Version**: 3.11+

---

**Quick Tip**: Bookmark this page for easy reference!
