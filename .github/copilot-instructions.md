# Oura Ring v2 Custom Component for Home Assistant

This is a modern Home Assistant custom integration for Oura Ring using the v2 API with OAuth2 authentication.

## Project Type
Home Assistant Custom Integration (Python)

## Key Requirements
- OAuth2 authentication using Home Assistant's application credentials
- Support for Oura Ring API v2 endpoints
- HACS compatible
- Follow latest Home Assistant integration standards (2025)
- Sensor entities for sleep, readiness, activity data

## Development Guidelines
- Use DataUpdateCoordinator for data fetching
- Implement proper OAuth2 flow with refresh tokens
- Follow Home Assistant coding standards
- Use type hints and proper error handling
- Support async operations throughout
