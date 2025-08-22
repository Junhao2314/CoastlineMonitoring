# 15年环南极冰山崩解数据集（2005–2020）—说明文档（中文译本）

## 数据集概述

- 数据集名称：Annual Iceberg Calving Dataset of the Antarctic Ice Shelves (2005–2020)
- 时间范围：2005年8月—2020年8月（连续15年）
- 空间范围：环南极所有冰架
- 数据格式：Shapefile
- DOI：https://doi.org/10.11888/Glacio.tpdc.271250
- 数据提供方：国家青藏高原科学数据中心（TPDC）

## 研究背景

冰山崩解是冰盖向海洋损失质量的关键过程，约占南极冰盖质量损失的一半。对崩解变化进行高分辨率、连续监测，有助于揭示其机制，并识别气候变化通过冰架支撑效应影响全球海平面变化的关键过程。

## 数据集特点

### 1）数据来源
- 卫星数据：基于多源光学与合成孔径雷达（SAR）影像的连续15年观测
- 主要传感器：
  - Envisat ASAR 宽幅影像（2005–2011）
  - MODIS 250 m 校准辐射产品（2012–2014）
  - Landsat 8 OLI 合成影像（2013年起）

### 2）数据内容
- 年度冰山崩解事件：逐事件记录
- 几何属性：面积、周长、长轴、短轴
- 物理属性：质量、平均厚度
- 时空信息：崩解位置、时间、所属冰架
- 崩解类型：不同类型冰山的分类信息

### 3）数据质量
- 空间分辨率：高分辨率卫星观测
- 时间连续性：15年无间断
- 覆盖范围：覆盖所有主要南极冰架
- 质量控制：严格质量控制与验证

## 主要发现

### 1）崩解速率统计
- 小型崩解事件（< 1 km²）：年均质量损失 18.4 ± 6.7 Gt/年
- 海洋末端冰川：崩解速率 166.7 ± 15.2 Gt/年

### 2）时空变化特征
- 年际变化显著
- 不同冰架的崩解模式存在差异
- 气候变化对崩解频率与强度有显著影响

## 数据获取

### 1）下载
- 官网（英文）：http://data.tpdc.ac.cn/en/
- DOI页面：https://doi.org/10.11888/Glacio.tpdc.271250
- 格式：Shapefile（.shp, .shx, .dbf, .prj）

### 2）使用要求
- 对公众开放免费使用
- 使用时需正确引用数据来源
- 建议联系数据提供方获取最新版本

## 引用

- 论文引用：
  Qi, M., Liu, Y., Liu, J., Cheng, X., Lin, Y., Feng, Q., Shen, Q., and Yu, Z.: A 15-year circum-Antarctic iceberg calving dataset derived from continuous satellite observations, Earth Syst. Sci. Data, 13, 4583–4596, https://doi.org/10.5194/essd-13-4583-2021, 2021.

- 数据引用：
  Qi, M., Liu, Y., Cheng, X., Hui, F., and Chen, Z.: Annual Iceberg Calving Dataset of the Antarctic Ice Shelves (2005–2020), National Tibetan Plateau Data Center, https://doi.org/10.11888/Glacio.tpdc.271250, 2021.

## 数据字段 / 属性字典

- ID（整数）：冰山崩解多边形/事件的唯一标识符。
- YEAR（字符串）：事件发生的年度（例如“2019-2020”表示记录跨两年，分析时通常取起始年）。
- Perimtr_KM（浮点，km）：多边形周长（千米）。
- AREA_KM（浮点，km²）：多边形面积（平方千米）。
- SCALE（整数）：数据生成中的比例尺/合成尺度标志（1 表示基础尺度）。
- THICKNES_M（浮点，m）：平均冰厚（米）。
- VOLUME_KM（浮点，km³）：冰体体积估计（立方千米）。
- MASS_GT（浮点，Gt）：冰体质量估计（吉吨，Gt），与数据集的质量核算一致。
- RECURRANCE（字符串）：崩解复现间隔分档（例如 “3-4”、“5-6”、“>8” 年）。
- UA_KM（浮点，km²）：面积不确定度（平方千米）。
- UH_M（浮点，m）：厚度不确定度（米）。
- UC_KM（浮点，km）：平面尺度/边界长度等相关指标的不确定度（千米）。
- REGION（字符串）：区域分类（如 East、West、Peninsula）。
- ICESHELF（字符串）：事件所属冰架名称。
- geometry（Polygon，EPSG:3031）：南极极地立体投影（EPSG:3031）下的多边形几何。

## 联系方式

- 数据提供方：国家青藏高原科学数据中心（TPDC）
- 网站：http://data.tpdc.ac.cn/
- 技术支持：通过官网联系表单获取支持

---

最后更新：2025年8月  
文档版本：v1.0