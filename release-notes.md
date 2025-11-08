## 🎉 Welcome to Oura Ring v2 Integration v1.2.0!

This release adds **comprehensive stress, resilience, SpO2, fitness, and sleep optimization sensors** for deeper health insights, plus **Home Assistant 2025.11 modernization** for improved device grouping and entity naming!

## ✨ NEW FEATURES IN v1.2.0

### 🧬 Code Quality & Maintainability Improvements

#### Phase 4: Logging & Token Handling
- **Cleaner Logs:** Removed excessive debug logging for production-ready output
- **Simplified Token Handling:** Streamlined OAuth2 token management in API client
- **Essential Logging Only:** Kept only critical info/error messages for operations
- **Graceful 401 Handling:** Silent handling of unavailable features (SpO2, VO2 Max, etc.)
- **Reduced Noise:** Removed redundant success/progress messages during normal operation

#### Phase 3: Coordinator Refactoring
- **Code Simplification:** Refactored `coordinator.py` from 252 to 241 lines (4.4% reduction)
- **Method Extraction:** Split 162-line `_process_data` method into 12 focused methods for better maintainability
- **Separation of Concerns:** Each data type now has its own processing method:
  - Sleep scores, sleep details, readiness, activity, heart rate
  - Stress, resilience, SpO2, VO2 Max, cardiovascular age, sleep time
- **Testing:** Added 13 comprehensive unit tests for all data processing methods
- **Orchestration:** Main `_process_data` method now delegates to specialized processors

#### Phase 2: Statistics Module Refactoring
- **Code Reduction:** Reduced `statistics.py` from 896 to 435 lines (51.5% reduction)
- **Configuration-Driven Design:** Replaced 11 duplicated functions with single generic processor
- **Helper Functions:** Added 4 reusable utility functions for data transformations
- **Testing:** Added 6 unit tests covering all transformation logic

#### Phase 1: Device Registry & Modern Entity Naming
- **Single Device Entry**: All 43 sensors now properly grouped under one "Oura Ring" device
- **Modern Entity Naming**: Follows HA 2025.11 standards with `has_entity_name=True`
- **Full Translation Support**: Entity names properly translated (currently English)
- **Entry-Scoped Unique IDs**: Prevents conflicts with multiple Oura accounts
- **Testing:** Added 7 unit tests and Docker-based test infrastructure

### 🏠 Home Assistant 2025.11 Modernization
- **Single Device Entry**: All 43 sensors now properly grouped under one "Oura Ring" device
- **Modern Entity Naming**: Follows HA 2025.11 naming standards with `has_entity_name=True`
- **Full Translation Support**: Entity names properly translated (currently English)
- **Entry-Scoped Unique IDs**: Prevents conflicts when using multiple Oura accounts
- **Docker Test Infrastructure**: Automated testing with Home Assistant Docker image

### 🧠 Stress & Recovery Tracking
- **Stress High Duration**: Minutes of elevated stress during the day
- **Recovery High Duration**: Minutes of elevated recovery (low stress)
- **Stress Day Summary**: Daily stress assessment (good/bad/unknown)

### 💪 Resilience & Adaptation
- **Resilience Level**: Your ability to adapt (limited/adequate/solid/strong/exceptional)
- **Sleep Recovery Score**: How well you recovered overnight
- **Daytime Recovery Score**: Your recovery throughout the day
- **Stress Resilience Score**: Your capacity to handle stress

### 🫁 Blood Oxygen Sensing (SpO2) - Gen3 & Oura Ring 4 Only
- **SpO2 Average**: Your average blood oxygen saturation percentage
- **Breathing Disturbance Index**: Indicators of sleep breathing quality

### 💓 Advanced Fitness Metrics
- **VO2 Max**: Your aerobic capacity in ml/kg/min
- **Cardiovascular Age**: Your biological cardiovascular age in years

### 😴 Sleep Optimization
- **Optimal Bedtime Start**: Recommended bedtime window start
- **Optimal Bedtime End**: Recommended bedtime window end

## 📊 SENSOR EXPANSION
- **Previous version**: 30 sensors
- **This version**: 43 sensors (+13 new sensors)
- All new sensors support long-term statistics for historical tracking
- SpO2 and Cardiovascular Age features exclusive to Gen3 and Oura Ring 4

## ⚡ IMPROVEMENTS
- Extended API coverage for all Oura Ring v2 endpoints
- Better health insights with stress and resilience data
- Sleep optimization recommendations built-in
- Fitness tracking capabilities expanded
- All new sensors integrate seamlessly with existing home automation
- **Modern Device Architecture**: All sensors properly group under a single device entry in Home Assistant
- **Improved Entity Names**: Cleaner entity names following HA 2025.11 conventions (e.g., "Sleep Score" instead of "Oura Sleep Score")
- **Translation Framework**: Entity names now support localization through strings.json
- **Better Multi-Account Support**: Entry-scoped unique IDs prevent conflicts with multiple Oura accounts
- **Corrected OAuth Scopes**: Fixed scope names to match Oura's actual API requirements
  - Changed `spo2Daily` → `spo2` (correct scope name)
  - Added `stress` scope (required for stress data endpoints)
  - Added `ring_configuration` scope (for ring configuration data)
  - Added `tag` scope (for user tags)
- **Graceful Error Handling**: 401 errors for unsupported features are handled silently
  - No ERROR log spam for features your ring doesn't support
  - Sensors for unsupported features show as "unavailable"
  - Core functionality (sleep, readiness, activity) unaffected
- **Better Debugging**: Added helpful debug messages explaining when features aren't available
- **Comprehensive Documentation**: Updated all scope references and added troubleshooting guides

## ⚠️ IMPORTANT: Re-authorization Required
To access all new features, users must re-authorize the integration:
1. Remove the Oura Ring integration from Home Assistant
2. Re-add it and complete the OAuth flow with the updated scopes
3. All new sensors and features will then be available

## 📚 COMPLETE SENSOR COUNT BY CATEGORY
- Sleep: 13 sensors
- Readiness: 4 sensors
- Activity: 8 sensors
- Heart Rate: 3 sensors
- **NEW - Stress:** 3 sensors
- **NEW - Resilience:** 4 sensors
- **NEW - SpO2:** 2 sensors (Gen3/Gen4 only)
- **NEW - Fitness:** 2 sensors
- **NEW - Sleep Optimization:** 2 sensors
- **Total:** 43 sensors

---

## ✨ NEW FEATURES IN v1.1.0!

This release adds **historical data loading with Long-Term Statistics** to populate your dashboards from day one!

## ✨ NEW FEATURES IN v1.1.0

### 📜 Historical Data Loading with Long-Term Statistics
- **Automatic historical data fetch** on first setup (default: 30 days)
- **Long-Term Statistics import**: All historical data properly stored with timestamps
- **Instant dashboard population**: Works immediately with ApexCharts, History Graph, and Statistics Graph
- **Configurable timeframe**: Choose 7-90 days of historical data
- **One-time fetch**: Historical data only loaded during initial setup
- **Efficient updates**: After initial load, only fetches new data

### 🎛️ Enhanced Configuration
- New option to configure historical data days (7-90 days)
- Historical data setting available in integration options
- Smart detection of first-time setup vs. ongoing updates

### � Long-Term Statistics Support
All 30 sensors now support long-term statistics:
- **Sleep metrics**: All 13 sleep sensors with historical data
- **Readiness metrics**: All 4 readiness sensors with historical data
- **Activity metrics**: All 8 activity sensors with historical data
- **Heart rate**: Daily average heart rate statistics
- **HRV**: Sleep HRV with historical trends

### 🎯 Benefits
- ✅ **Immediate insights**: See 30 days of trends from installation
- ✅ **Proper timestamps**: Each data point has the correct historical date
- ✅ **Database efficiency**: Uses HA's optimized statistics storage
- ✅ **Dashboard ready**: Works with all history visualization cards
- ✅ **API efficient**: Bulk load once, then incremental daily updates

## �🔧 IMPROVEMENTS
- Better logging for historical data loading and statistics import
- More efficient API usage pattern (initial bulk load + incremental updates)
- Follows Oura API best practices for data access
- Statistics database integration for long-term data storage

## 📚 TECHNICAL DETAILS
- New `statistics.py` module for handling long-term statistics
- Automatic import of historical data points with proper timestamps
- Support for both mean and sum statistics where appropriate
- Comprehensive metadata for all sensor types

---

## Previous Release: v1.0.0

This was the **first official release** of the modern Oura Ring custom integration for Home Assistant, built from the ground up using the Oura API v2 with OAuth2 authentication.

## ✨ KEY FEATURES

### Comprehensive Health Tracking - 30 Sensors
- **Sleep Monitoring** (13 sensors): Sleep score, durations for all sleep stages, awake time, time in bed, efficiency, restfulness, latency, timing, and stage percentages
- **Readiness Tracking** (4 sensors): Readiness score, temperature deviation, resting heart rate score, HRV balance score
- **Activity Metrics** (8 sensors): Activity score, steps, calories, and activity time by intensity
- **Heart Rate Data** (4 sensors): Current, average, minimum, and maximum heart rate
- **HRV Monitoring** (1 sensor): Average sleep HRV for recovery tracking

### Modern Architecture
- **OAuth2 Authentication**: Secure authentication using Home Assistant's application credentials system
- **Efficient Data Fetching**: Parallel fetching of 5 Oura API v2 endpoints
- **DataUpdateCoordinator**: Optimal data management following Home Assistant best practices
- **Configurable Updates**: Refresh interval configurable from 1-60 minutes (default: 5 minutes)
- **Type-Safe**: Full type hint coverage for reliability
- **Async Throughout**: All operations are asynchronous for performance

### HACS Compatible
- Easy installation through HACS custom repositories
- Automatic updates when new versions are released
- Custom branding with Oura Ring icon

### Accurate Data Interpretation
- Sleep durations from actual measurements (not contribution scores)
- Activity times from actual MET minutes
- Clear distinction between scores and measured values
- Proper handling of null values for optional metrics

## 📊 COMPLETE SENSOR LIST

### Sleep Sensors (13)
1. Sleep Score
2. Total Sleep Duration (hours)
3. Deep Sleep Duration (hours)
4. REM Sleep Duration (hours)
5. Light Sleep Duration (hours)
6. Awake Time (hours)
7. Sleep Efficiency (%)
8. Restfulness (%)
9. Sleep Latency (minutes)
10. Sleep Timing (score)
11. Deep Sleep Percentage (%)
12. REM Sleep Percentage (%)
13. Time in Bed (hours)

### Readiness Sensors (4)
1. Readiness Score
2. Temperature Deviation (°C)
3. Resting Heart Rate Score (contribution score 1-100)
4. HRV Balance Score (contribution score 1-100)

### Activity Sensors (8)
1. Activity Score
2. Steps
3. Active Calories (kcal)
4. Total Calories (kcal)
5. Target Calories (kcal)
6. High Activity Time (minutes)
7. Medium Activity Time (minutes)
8. Low Activity Time (minutes)

### Heart Rate Sensors (4)
1. Current Heart Rate (bpm)
2. Average Heart Rate (bpm)
3. Minimum Heart Rate (bpm)
4. Maximum Heart Rate (bpm)

### HRV Sensors (1)
1. Average Sleep HRV (ms)

## 🚀 GETTING STARTED

### Installation via HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to Integrations
3. Click the three dots → Custom repositories
4. Add: `https://github.com/louispires/oura-v2-custom-component`
5. Category: Integration
6. Install "Oura Ring"
7. Restart Home Assistant

### Configuration

1. **Create Oura Application**
   - Go to [Oura Cloud](https://cloud.ouraring.com/applications)
   - Create a new application
   - Save your Client ID and Client Secret

2. **Add Application Credentials**
   - Settings → Devices & Services → Application Credentials
   - Add your Oura Client ID and Secret

3. **Add Integration**
   - Settings → Devices & Services → Add Integration
   - Search for "Oura Ring"
   - Follow the OAuth2 authentication flow

## 📚 DOCUMENTATION

Complete documentation is available in the repository:
- [Installation Guide](https://github.com/louispires/oura-v2-custom-component/blob/main/docs/INSTALLATION.md)
- [Quick Reference](https://github.com/louispires/oura-v2-custom-component/blob/main/docs/QUICKREF.md)
- [Troubleshooting](https://github.com/louispires/oura-v2-custom-component/blob/main/docs/TROUBLESHOOTING.md)
- [Dashboard Examples](https://github.com/louispires/oura-v2-custom-component/blob/main/README.md#dashboard-examples)

## 🎯 WHAT MAKES THIS INTEGRATION SPECIAL

- **Built for Oura API v2**: Uses the latest API with all modern features
- **OAuth2 Security**: Leverages Home Assistant's secure credential system
- **Accurate Data**: Correctly interprets all API fields and data types
- **Well Documented**: Comprehensive guides and dashboard examples
- **Actively Maintained**: Built with modern HA standards (2025)

## 🎯 WHAT MAKES THIS INTEGRATION SPECIAL

- **Built for Oura API v2**: Uses the latest API with all modern features
- **OAuth2 Security**: Leverages Home Assistant's secure credential system
- **Accurate Data**: Correctly interprets all API fields and data types
- **Well Documented**: Comprehensive guides and dashboard examples
- **Actively Maintained**: Built with modern HA standards (2025)

## 💬 SUPPORT

- **Issues**: [GitHub Issues](https://github.com/louispires/oura-v2-custom-component/issues)
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Documentation**: Full guides available in the repository

## 🙏 CREDITS

- Original Oura Component: [nitobuendia/oura-custom-component](https://github.com/nitobuendia/oura-custom-component)
- Oura Ring API: [Oura Cloud API Documentation](https://cloud.ouraring.com/v2/docs)
- Development assisted by: Claude Sonnet 4 (Anthropic AI)

---

**Enjoy tracking your health data with Home Assistant!** 💪
