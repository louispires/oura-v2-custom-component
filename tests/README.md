# Test Suite Documentation

This directory contains the comprehensive test suite for the Oura Ring Home Assistant integration.

## Test Structure

The test suite is organized into focused test modules:

### Unit Tests

- **`test_sensor.py`** (7 tests)
  - Device info configuration
  - Modern entity naming with `has_entity_name=True`
  - Translation keys
  - Entity availability logic
  - Unique ID generation

- **`test_statistics.py`** (6 tests)
  - Statistics metadata completeness
  - Data source configuration structure
  - Timestamp parsing functions
  - Value transformation helpers
  - Nested value extraction

- **`test_coordinator.py`** (13 tests)
  - Individual processing methods for each data type
  - Sleep score and detail processing
  - Readiness, activity, and heart rate handling
  - Stress, resilience, SpO2, VO2 Max processing
  - Overall data orchestration
  - Empty data handling

- **`test_entity_categories.py`** (6 tests)
  - Entity category assignments
  - State class improvements (`total`, `total_increasing`)
  - Measurement vs diagnostic categories
  - Text sensor handling
  - Primary sensors not marked as diagnostic

### Integration Tests

- **`test_integration_setup.py`** (7 tests)
  - Fixture validation tests
  - Config entry setup
  - OAuth2 session mocking
  - API client mocking
  - Coordinator mocking

## Test Fixtures (`conftest.py`)

The `conftest.py` file provides reusable pytest fixtures for all tests:

### Core Fixtures

- **`mock_config_entry`**: Fully configured ConfigEntry with OAuth2 token data
- **`mock_hass`**: Mocked HomeAssistant instance with proper spec
- **`mock_oura_api_client`**: AsyncMock API client with sample response data
- **`mock_oauth2_session`**: Mocked OAuth2 session with token refresh
- **`mock_coordinator_with_data`**: Coordinator with pre-populated data

### Data Fixtures

- **`mock_oura_api_data`**: Complete sample API response with all data types
- **`mock_empty_api_response`**: Empty API response for unavailable sensor testing

## Running Tests

### Using Docker (Recommended)

Run all tests:
```bash
docker-compose -f docker-compose.test.yml run --rm test pytest tests/ -v
```

Run a specific test file:
```bash
docker-compose -f docker-compose.test.yml run --rm test pytest tests/test_sensor.py -v
```

Run a specific test:
```bash
docker-compose -f docker-compose.test.yml run --rm test pytest tests/test_sensor.py::test_sensor_device_info -v
```

### Using Local Python Environment

If you have the Home Assistant dependencies installed locally:
```bash
pytest tests/ -v
```

## Test Coverage

Current test coverage:

- **Total Tests**: 39
- **Passing**: 39 (100%)
- **Coverage Areas**:
  - ✅ Sensor entity configuration
  - ✅ Statistics module helpers
  - ✅ Coordinator data processing
  - ✅ Entity categories and state classes
  - ✅ Test fixtures and infrastructure

## Adding New Tests

When adding new tests:

1. **Use Existing Fixtures**: Leverage fixtures from `conftest.py` to reduce boilerplate
2. **Follow Naming Conventions**: Test files should start with `test_`, test functions should start with `test_`
3. **Keep Tests Focused**: Each test should verify a single behavior
4. **Use Descriptive Names**: Test names should clearly describe what they're testing
5. **Add Docstrings**: Brief description of what the test validates

### Example Test Structure

```python
def test_sensor_behavior(mock_coordinator_with_data, mock_config_entry):
    """Test that sensor behaves correctly with valid data."""
    # Arrange
    sensor = OuraSensor(mock_coordinator_with_data, "sleep_score")
    
    # Act
    result = sensor.native_value
    
    # Assert
    assert result == 85
```

## Continuous Integration

Tests are designed to run in CI environments:

- Uses Docker for consistent test environment
- Home Assistant 2025.11 base image
- No native dependencies required
- Fast execution (~0.15s for all tests)

## Future Enhancements

Potential test improvements:

- Add async integration tests for full setup/teardown flow
- Add config flow tests for OAuth2 authentication
- Add API client tests with real request/response mocking
- Increase test coverage for error handling paths
- Add performance benchmarking tests
