# 南极海岸线数据处理项目

## 项目概述

本项目从Zenodo数据仓库下载了1997-2021年期间的南极海岸线数据，并将其转换为GeoJSON格式以便于地理信息系统分析和可视化。

## 数据来源

**数据集**: Antarctic Coastlines, 1997-2021  
**DOI**: https://doi.org/10.5281/zenodo.5903643  
**发布者**: NASA / Jet Propulsion Laboratory & Australian Antarctic Program Partnership  
**发布日期**: 2022年1月25日  
**版本**: 1.0  

### 数据描述

- **时间范围**: 1997.75 - 2021.2 (24个时间点)
- **坐标系统**: EPSG:3031 (Antarctic Polar Stereographic)
- **分辨率**: 240米
- **数据格式**: 原始数据为纯文本文件，包含东向和北向坐标
- **数据特点**: 时间演化的南极崩解前沿观测数据

## 项目结构

```
大汶河数据/
├── antarctic_coastlines_data/          # 原始下载的文本数据
│   ├── antarctic_coastline_1997.75.txt
│   ├── antarctic_coastline_2000.2.txt
│   ├── ...
│   └── antarctic_coastline_2021.2.txt
├── Greene/                             # 转换后的GeoJSON数据
│   ├── antarctic_coastline_1997.75.geojson
│   ├── antarctic_coastline_2000.2.geojson
│   ├── ...
│   └── antarctic_coastline_2021.2.geojson
├── download_antarctic_coastlines.py   # 数据下载脚本
├── convert_to_geojson.py              # 格式转换脚本
└── README.md                          # 项目说明文档
```

## 脚本说明

### 1. download_antarctic_coastlines.py

**功能**: 从Zenodo自动下载所有南极海岸线数据文件

**特点**:
- 支持断点续传，已存在的文件会跳过下载
- 显示下载进度
- 自动创建下载文件夹
- 包含错误处理和重试机制

**使用方法**:
```bash
python download_antarctic_coastlines.py
```

### 2. convert_to_geojson.py

**功能**: 将原始文本格式的海岸线数据转换为GeoJSON格式

**处理过程**:
1. 读取每个文本文件中的坐标数据
2. 解析EPSG:3031坐标系的东向和北向坐标
3. 处理NaN分隔符，将数据分组为独立的线段
4. 保持原始坐标系统(EPSG:3031)，不进行坐标转换
5. 生成MultiLineString类型的GeoJSON要素
6. 为每个年份创建独立的GeoJSON文件

**输出格式**:
- 坐标系统: EPSG:3031 (保持原始投影)
- 几何类型: MultiLineString
- 属性信息: 包含年份和描述信息

**使用方法**:
```bash
python convert_to_geojson.py
```

## 数据特征

### 坐标系统
- **EPSG:3031**: Antarctic Polar Stereographic (南极极地立体投影)
- **单位**: 米
- **适用范围**: 南极地区

### 数据结构
每个GeoJSON文件包含:
- **type**: "FeatureCollection"
- **features**: 包含一个Feature对象
  - **geometry**: MultiLineString类型，包含多个线段组
  - **properties**: 
    - year: 数据对应的年份
    - description: 数据描述

### 线段组特征
- 每个年份包含500-650个独立的线段组
- 每个线段组代表南极海岸线的一个连续部分
- 线段组之间由NaN值分隔
- 理论上所有线段组合起来形成南极大陆的完整海岸线轮廓

## 数据质量

- **完整性**: 成功处理了24个年份的所有数据文件
- **准确性**: 保持了原始数据的精度和坐标系统
- **一致性**: 所有文件使用相同的处理流程和格式标准

## 应用场景

1. **科学研究**: 分析南极冰架变化趋势
2. **气候研究**: 研究全球变暖对南极海岸线的影响
3. **GIS分析**: 在地理信息系统中进行空间分析
4. **数据可视化**: 创建交互式地图和时间序列动画
5. **海洋学研究**: 分析海冰边界变化

## 技术要求

### Python依赖包
- `requests`: HTTP请求库，用于数据下载
- `json`: JSON数据处理
- `os`: 文件系统操作
- `glob`: 文件路径匹配
- `numpy`: 数值计算(可选)

### 系统要求
- Python 3.6+
- 足够的磁盘空间(约200MB用于原始数据，约500MB用于GeoJSON文件)

## 数据引用

如果在研究中使用此数据，请引用原始数据源：

```
Greene, C. A., et al. (2022). Antarctic Coastlines, 1997-2021 [Data set]. 
Zenodo. https://doi.org/10.5281/zenodo.5903643
```

相关论文：
```
Greene, C. A., et al. (2022). Antarctic calving loss rivals ice-shelf thinning. 
Nature, 609, 948-953. https://doi.org/10.1038/s41586-022-05037-w
```

## 注意事项

1. **坐标系统**: 数据使用EPSG:3031投影，在某些GIS软件中可能需要手动设置坐标系
2. **文件大小**: GeoJSON文件相对较大，建议根据需要选择特定年份的数据
3. **数据精度**: 原始数据分辨率为240米，适合中等比例尺的分析
4. **时间间隔**: 数据时间点不均匀分布，使用时需注意时间间隔

## 更新日志

- **2024**: 项目创建，完成数据下载和格式转换
- 保持原始EPSG:3031坐标系统
- 生成独立的年份文件，便于按需使用

## 联系信息

如有问题或建议，请参考原始数据发布者的联系方式或相关论文作者信息。

---

*本项目仅用于数据处理和格式转换，原始数据版权归NASA/JPL和相关研究机构所有。*