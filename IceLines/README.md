# Icelines 数据下载器

## 项目简介

本项目是一个用于下载南极主要冰架前缘数据的Python工具。Icelines数据来自堪萨斯大学雷达系统与遥感实验室（CReSIS），包含了南极主要冰架前缘变化数据，对于研究南极冰川动态、气候变化等具有重要价值。

## 数据来源

- **数据源**：https://icelines.cresis.ku.edu/data/
- **数据格式**：GPKG（GeoPackage）格式的地理空间数据
- **覆盖范围**：南极洲51个主要冰架区域
- **时间分辨率**：包含日度（daily）、月度（monthly）、季度（quarterly）和年度（annual）数据

## 功能特点

### 🚀 高效并发下载
- 支持多线程并发下载，显著提升下载速度
- 可配置并发线程数，默认为4个线程以平衡速度与服务器稳定性
- 智能重试机制，自动处理网络错误和服务器临时故障

### 📁 灵活的文件夹控制
- 支持选择性下载不同时间分辨率的数据
- 可配置跳过特定类型文件夹（daily、monthly、quarterly、annual）
- 智能跳过已存在文件，支持断点续传

### 🛡️ 稳定性保障
- 线程安全的输出显示
- 完善的错误处理和异常捕获
- 实时进度显示和状态反馈

## 安装要求

### Python环境
- Python 3.6 或更高版本

### 依赖库
```bash
pip install requests beautifulsoup4
```

## 使用方法

### 1. 基本使用

直接运行脚本开始下载：

```bash
python download_icelines.py
```

### 2. 配置选项

在脚本开头的配置部分，您可以根据需要调整以下参数：

```python
# 配置选项
max_workers = 4        # 并发下载线程数
skip_daily = True      # 跳过daily文件夹下载
skip_monthly = False   # 跳过monthly文件夹下载
skip_annual = False    # 跳过annual文件夹下载
skip_quarterly = False # 跳过quarterly文件夹下载
```

#### 配置说明：

- **max_workers**：并发线程数
  - 建议值：2-8
  - 过高可能导致服务器返回503错误
  - 过低会影响下载速度

- **skip_*选项**：控制跳过特定类型的文件夹
  - `True`：跳过该类型文件夹
  - `False`：下载该类型文件夹
  - 建议根据研究需求选择合适的时间分辨率

### 3. 输出目录结构

下载的数据将保存在 `data/` 目录下，结构如下：

```
data/
├── icelines_antarctic_coastline_2018.zip
├── icelines_auxiliary_v1.zip
├── Abbot1/
│   ├── annual/
│   ├── monthly/
│   ├── quarterly/
│   └── daily/ (如果未跳过)
├── Abbot2/
├── Amery/
└── ... (其他51个冰架区域)
```

### 4. 运行示例

启动脚本后，您将看到类似以下的输出：

```
=== Icelines 数据并发下载器 ===
CPU 核心数: 12
并发下载线程数: 4 (限制以避免服务器过载)
跳过daily文件夹: 是
跳过monthly文件夹: 否
跳过annual文件夹: 否
跳过quarterly文件夹: 否
目标目录: F:\...\data
========================================
开始下载zip文件...
  跳过已存在: icelines_antarctic_coastline_2018.zip
  跳过已存在: icelines_auxiliary_v1.zip

开始并发递归下载文件夹...

[1/51] 处理文件夹: Abbot1
处理目录: Abbot1/ (并发数: 4)
  跳过daily文件夹: Abbot1/daily/
处理目录: Abbot1/annual/ (并发数: 4)
  开始并发下载 9 个文件...
  ✓ 成功: 2015noQ1_mean-Abbot1.gpkg
  ✓ 成功: 2016noQ1_mean-Abbot1.gpkg
  ...
```

## 注意事项

### ⚠️ 网络和服务器
- 下载过程需要稳定的网络连接
- 服务器可能会限制并发请求，建议不要设置过高的并发数
- 如遇到大量503错误，请降低 `max_workers` 值

### 💾 存储空间
- 完整数据集较大，请确保有足够的磁盘空间
- 建议根据研究需求选择性下载特定时间分辨率的数据

### 🔄 断点续传
- 脚本支持断点续传，重新运行会自动跳过已下载的文件
- 如需重新下载某个文件，请先删除对应的本地文件

## 故障排除

### 常见问题

1. **503 Service Unavailable 错误**
   - 降低 `max_workers` 值（建议2-4）
   - 等待一段时间后重新运行

2. **网络连接超时**
   - 检查网络连接
   - 脚本会自动重试，请耐心等待

3. **磁盘空间不足**
   - 清理磁盘空间
   - 或选择性下载部分数据类型

## 许可证

本项目仅用于学术研究目的。数据版权归堪萨斯大学雷达系统与遥感实验室所有。

## 联系方式

如有问题或建议，请通过相关渠道联系项目维护者。