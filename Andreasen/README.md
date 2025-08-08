# 数据下载

本项目旨在从 [Zenodo](https://doi.org/10.5281/zenodo.7830051) 下载冰架前缘的年度数据集。整个流程包括数据下载、解压、格式转换、数据清洗和年度合并，最终生成按年份组织的GeoJSON文件。

## 数据来源

 **"Annual Antarctic calving front locations from 2009 to 2021"**，由 Andreasen, J.K. 等人发布在Zenodo上。该数据集包含了2009年至2021年间南极洲35个主要冰架的前缘位置，时间分辨率为逐年，数据格式为shapefile。

- **数据链接**: [https://doi.org/10.5281/zenodo.7830051](https://doi.org/10.5281/zenodo.7830051)
- **引用**: Andreasen, J.K., Hogg, A.E., Selley, H.L., & Cornford, S.L. (2023). Annual Antarctic calving front locations from 2009 to 2021 (Version 1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.7830051

## 项目结构

```
.
├── Andreasen/              # 存放最终生成的年度GeoJSON文件
├── zenodo_downloads/       # 存放从Zenodo下载的原始zip文件
├── download_files.py       # 用于下载数据的Python脚本
├── process_downloads.py    # 用于处理下载数据并生成GeoJSON的Python脚本
└── README.md               # 本文档
```

## 处理流程

整个工作流程由两个主要的Python脚本驱动：`download_files.py` 和 `process_downloads.py`。

### 步骤 1: 下载数据

通过运行 `download_files.py` 脚本，可以自动从Zenodo下载所有必需的 `.zip` 文件。

**如何运行:**
```bash
python download_files.py
```

该脚本会执行以下操作：
1.  读取一个预定义的Zenodo文件列表。
2.  循环下载列表中的每一个文件。
3.  将下载的 `.zip` 文件保存到 `zenodo_downloads` 目录中。

### 步骤 2: 处理数据并生成GeoJSON

下载完成后，运行 `process_downloads.py` 脚本来处理数据。

**如何运行:**
```bash
python process_downloads.py
```

该脚本会执行以下操作：
1.  遍历 `zenodo_downloads` 目录下的所有 `.zip` 文件。
2.  直接从zip文件中读取shapefile，无需手动解压。同时，脚本会智能地跳过macOS系统生成的 `__MACOSX` 文件夹。
3.  从每个shapefile的文件名中提取年份和区域名称。
4.  将区域名称作为一个新的属性列（`Name` 或 `source_name`）添加到数据中。
5.  在同一年度的数据合并成一个单一的GeoDataFrame。
6.  对合并后的数据进行清洗：
    - 如果数据中存在 `id` 列，则对其进行重新编号，以确保ID的唯一性和连续性。
    - 移除所有值均为空的列，以精简数据。
7.  将每年合并和清洗后的数据导出为一个GeoJSON文件，并保存在 `Andreasen` 目录中，以年份命名（例如 `2009.geojson`）。
