# BAS南极海岸线

英国南极调查局（BAS）南极海岸线中分辨率数据的批量下载、格式转换和几何简化处理。

## 概述

处理BAS（British Antarctic Survey）提供的南极海岸线中分辨率线数据，涵盖了从v7.2到v7.10的多个版本，并将其转换为统一的GeoJSON格式，便于在各种GIS软件中使用。

## 工作

### 1. 数据下载

- **数据源**：英国南极调查局（BAS）南极数字数据库（ADD）
- **数据类型**：南极海岸线中分辨率线数据（GPKG格式）
- **版本范围**：v7.2 - v7.10（共9个版本）
- **下载工具**：`download_bas_gpkg.py`

#### 下载的数据版本：
- add_coastline_medium_res_line_v7_10.gpkg (7.29 MB)
- add_coastline_medium_res_line_v7_9.gpkg (7.21 MB)
- add_coastline_medium_res_line_v7_8.gpkg (7.17 MB)
- add_coastline_medium_res_line_v7_7.gpkg (6.30 MB)
- add_coastline_medium_res_line_v7_6.gpkg (6.32 MB)
- add_coastline_medium_res_line_v7_5.gpkg (6.31 MB)
- add_coastline_medium_res_line_v7_4.gpkg (6.30 MB)
- add_coastline_medium_res_line_v7_3.gpkg (6.77 MB)
- add_coastline_medium_res_line_v7_2.gpkg (6.83 MB)

**总下载大小**：60.50 MB

### 2. 格式转换

- **转换工具**：`convert_gpkg_to_geojson.py`
- **输入格式**：GPKG（GeoPackage）
- **输出格式**：GeoJSON
- **坐标系统一**：EPSG:3031（南极极地立体投影）
- **几何简化**：40米容差

#### 转换后的文件：
- add_coastline_medium_res_line_v7_10.geojson (15.33 MB)
- add_coastline_medium_res_line_v7_9.geojson (15.34 MB)
- add_coastline_medium_res_line_v7_8.geojson (14.74 MB)
- add_coastline_medium_res_line_v7_7.geojson (13.47 MB)
- add_coastline_medium_res_line_v7_6.geojson (14.12 MB)
- add_coastline_medium_res_line_v7_5.geojson (14.10 MB)
- add_coastline_medium_res_line_v7_4.geojson (14.23 MB)
- add_coastline_medium_res_line_v7_3.geojson (14.82 MB)
- add_coastline_medium_res_line_v7_2.geojson (15.20 MB)

**总文件大小**：约131 MB

## 技术特性

### 坐标系统一
- **目标坐标系**：EPSG:3031（南极极地立体投影）
- **优势**：适合南极地区的地理分析和测量
- **兼容性**：支持主流GIS软件

### 几何简化
- **简化容差**：40米
- **目的**：优化文件大小和处理性能
- **保持精度**：在保证数据质量的前提下减少冗余点

### 批量处理
- **自动化下载**：支持多版本数据的批量下载
- **批量转换**：一次性处理所有GPKG文件
- **进度监控**：实时显示下载和转换进度
- **错误处理**：完善的异常处理机制

## 目录结构

```
项目根目录/
├── temp/                          # 原始GPKG文件存储目录
│   ├── add_coastline_medium_res_line_v7_10.gpkg
│   ├── add_coastline_medium_res_line_v7_9.gpkg
│   ├── ...
│   └── add_coastline_medium_res_line_v7_2.gpkg
├── ADD/                           # 转换后的GeoJSON文件存储目录
│   ├── add_coastline_medium_res_line_v7_10.geojson
│   ├── add_coastline_medium_res_line_v7_9.geojson
│   ├── ...
│   └── add_coastline_medium_res_line_v7_2.geojson
├── download_bas_gpkg.py           # BAS数据下载脚本
├── convert_gpkg_to_geojson.py     # GPKG到GeoJSON转换脚本
└── README.md                      # 项目说明文档
```

## 使用方法

### 下载数据
```bash
python download_bas_gpkg.py
```

### 转换格式
```bash
python convert_gpkg_to_geojson.py
```

## 依赖库

- `geopandas`：地理数据处理
- `requests`：HTTP请求
- `pathlib`：路径操作
- `urllib.parse`：URL解析

## 数据来源

- **数据提供方**：英国南极调查局（British Antarctic Survey, BAS）
- **数据集名称**：SCAR南极数字数据库（Antarctic Digital Database, ADD）
- **数据类型**：南极海岸线中分辨率线数据
- **数据格式**：GeoPackage (.gpkg)
- **坐标系**：原始数据使用EPSG:3031

## 应用场景

- 南极地理信息系统（GIS）分析
- 南极海岸线变化研究
- 气候变化影响评估
- 科学研究和数据可视化
- 地图制作和空间分析

---

*本项目用于科学研究和教育目的，数据版权归英国南极调查局所有。*