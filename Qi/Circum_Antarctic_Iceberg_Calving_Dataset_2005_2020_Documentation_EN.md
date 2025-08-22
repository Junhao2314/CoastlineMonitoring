# 15-Year Circum-Antarctic Iceberg Calving Dataset – Documentation

## Dataset Overview

- Dataset Title: Annual Iceberg Calving Dataset of the Antarctic Ice Shelves (2005–2020)
- Temporal Coverage: August 2005 – August 2020 (15 consecutive years)
- Spatial Coverage: All Antarctic ice shelves (circum-Antarctic)
- Data Format: Shapefile
- DOI: https://doi.org/10.11888/Glacio.tpdc.271250
- Data Provider: National Tibetan Plateau Data Center (TPDC)

## Research Background

Iceberg calving is a key process by which ice sheets lose mass to the ocean, accounting for about half of the Antarctic Ice Sheet’s mass loss. High-resolution monitoring of calving variability helps reveal underlying mechanisms and identify how climate change, through ice-shelf buttressing effects, influences the major processes driving global sea-level change.

## Key Features

### 1) Data Sources
- Satellite data: Derived from 15 years of continuous multi-source optical and SAR imagery
- Main sensors:
  - Envisat ASAR (wide-swath) imagery (2005–2011)
  - MODIS 250 m calibrated radiance products (2012–2014)
  - Landsat 8 OLI composite imagery (since 2013)

### 2) Data Content
- Annual iceberg calving events: Event-level records per year
- Geometric attributes: Area, perimeter, major axis, minor axis
- Physical attributes: Mass, mean thickness
- Spatiotemporal info: Calving location, time, ice-shelf affiliation
- Calving types: Classification of different iceberg types

### 3) Data Quality
- Spatial resolution: High-resolution satellite observations
- Temporal continuity: 15 years without interruption
- Coverage: All major Antarctic ice shelves
- Accuracy: Subject to stringent quality control and validation

## Main Findings

### 1) Calving Rate Statistics
- Small calving events (< 1 km²): Mean annual mass loss 18.4 ± 6.7 Gt/year
- Marine-terminating glaciers: Calving rate 166.7 ± 15.2 Gt/year

### 2) Spatiotemporal Variability
- Significant interannual variability in calving events
- Distinct calving patterns across different ice shelves
- Clear influence of climate variability on calving frequency and magnitude

## Data Access

### 1) Download
- Official site: http://data.tpdc.ac.cn/en/
- DOI landing page: https://doi.org/10.11888/Glacio.tpdc.271250
- Format: Shapefile (.shp, .shx, .dbf, .prj)

### 2) Usage Requirements
- Open and free for use
- Proper citation of the data source is required
- It is recommended to contact the provider for the latest version

## Citation

- Article citation:
  Qi, M., Liu, Y., Liu, J., Cheng, X., Lin, Y., Feng, Q., Shen, Q., and Yu, Z.: A 15-year circum-Antarctic iceberg calving dataset derived from continuous satellite observations, Earth Syst. Sci. Data, 13, 4583–4596, https://doi.org/10.5194/essd-13-4583-2021, 2021.

- Dataset citation:
  Qi, M., Liu, Y., Cheng, X., Hui, F., and Chen, Z.: Annual Iceberg Calving Dataset of the Antarctic Ice Shelves (2005–2020), National Tibetan Plateau Data Center, https://doi.org/10.11888/Glacio.tpdc.271250, 2021.

## Data Fields / Attribute Dictionary

- ID (integer): Unique identifier for each calving polygon/event.
- YEAR (string): The year or year span of the event (e.g., "2019-2020" for cross-year records; analyses typically use the starting year).
- Perimtr_KM (float, km): Polygon perimeter in kilometers.
- AREA_KM (float, km²): Polygon area in square kilometers.
- SCALE (integer): Scale flag used in data generation (1 denotes base scale).
- THICKNES_M (float, m): Mean ice thickness in meters.
- VOLUME_KM (float, km³): Estimated ice volume in cubic kilometers.
- MASS_GT (float, Gt): Estimated ice mass in gigatons, consistent with the dataset’s mass accounting.
- RECURRANCE (string): Recurrence interval category (e.g., "3-4", "5-6", ">8" years).
- UA_KM (float, km²): Area uncertainty in square kilometers.
- UH_M (float, m): Thickness uncertainty in meters.
- UC_KM (float, km): Uncertainty of planimetric metrics/boundary length in kilometers.
- REGION (string): Regional classification (e.g., East, West, Peninsula).
- ICESHELF (string): Name of the ice shelf where the event occurred.
- geometry (Polygon, EPSG:3031): Polygon geometry in Antarctic Polar Stereographic projection (EPSG:3031).

## Contact

- Data provider: National Tibetan Plateau Data Center (TPDC)
- Website: http://data.tpdc.ac.cn/
- Technical support: Contact via the official site’s web form

---

Last updated: August 2025
Document version: v1.0