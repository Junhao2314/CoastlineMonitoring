import os
import json
import glob
from pathlib import Path
import geopandas as gpd
import pandas as pd
from collections import defaultdict
import re

# 输出格式参数：支持 'shp', 'geojson', 'gpkg'
output_format = 'geojson'

# 几何简化容差参数
tolerance = 100

def geom_simplify(gdf, tolerance=100):
    """
    简化几何图形
    """
    gdf_simplified = gdf.copy()
    gdf_simplified['geometry'] = gdf_simplified['geometry'].simplify(tolerance)
    return gdf_simplified

def extract_time_info(filename, time_period):
    """
    从文件名中提取时间信息
    """
    if time_period == 'annual':
        # 提取年份，如 2015noQ1_mean-Abbot1.gpkg -> 2015noQ1
        match = re.search(r'(\d{4}noQ\d)', filename)
        return match.group(1) if match else None
    elif time_period == 'monthly':
        # 提取年月，如 201501_mean-Abbot1.gpkg -> 201501
        match = re.search(r'(\d{6})', filename)
        return match.group(1) if match else None
    elif time_period == 'quarterly':
        # 提取年季度，如 2015Q1_mean-Abbot1.gpkg -> 2015Q1
        match = re.search(r'(\d{4}Q\d)', filename)
        return match.group(1) if match else None
    return None

def merge_gpkg_files(time_period, output_format='geojson'):
    """
    合并指定时间维度的所有gpkg文件，按时间分组输出
    time_period: 'annual', 'monthly', 'quarterly'
    """
    data_dir = Path('./data')
    output_dir = Path(f'./Icelines/{time_period}')
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 按时间分组存储数据
    time_groups = defaultdict(list)
    
    # 遍历所有冰架文件夹
    for ice_shelf_dir in data_dir.iterdir():
        if ice_shelf_dir.is_dir() and ice_shelf_dir.name not in ['icelines_antarctic_coastline_2018.zip', 'icelines_auxiliary_v1.zip']:
            ice_shelf_name = ice_shelf_dir.name
            time_dir = ice_shelf_dir / time_period
            
            if time_dir.exists():
                # 查找fronts和fronts-eliminated文件夹
                for sub_dir in ['fronts', 'fronts-eliminated']:
                    fronts_dir = time_dir / sub_dir
                    if fronts_dir.exists():
                        # 查找所有gpkg文件
                        gpkg_files = list(fronts_dir.glob('*.gpkg'))
                        
                        for gpkg_file in gpkg_files:
                            try:
                                # 提取时间信息
                                time_info = extract_time_info(gpkg_file.name, time_period)
                                if not time_info:
                                    print(f"无法提取时间信息: {gpkg_file}")
                                    continue
                                
                                # 读取gpkg文件
                                gdf = gpd.read_file(gpkg_file)
                                
                                # 添加额外的属性字段
                                gdf['name'] = ice_shelf_name
                                gdf['source_file'] = gpkg_file.name
                                gdf['sub_category'] = sub_dir
                                gdf['time_period'] = time_info
                                
                                # 按时间分组
                                time_groups[time_info].append(gdf)
                                        
                                print(f"处理文件: {gpkg_file} (冰架: {ice_shelf_name}, 时间: {time_info}, 记录数: {len(gdf)})")
                                
                            except Exception as e:
                                print(f"处理文件 {gpkg_file} 时出错: {e}")
    
    # 为每个时间组创建合并文件
    total_files = 0
    for time_info, gdfs in time_groups.items():
        if gdfs:
            # 合并同一时间的所有数据
            merged_gdf = pd.concat(gdfs, ignore_index=True)
            
            # 简化几何图形
            merged_gdf = geom_simplify(merged_gdf, tolerance=tolerance)
            
            # 根据输出格式保存文件
            if output_format.lower() == 'shp':
                output_file = output_dir / f'{time_info}.shp'
                merged_gdf.to_file(output_file, driver='ESRI Shapefile')
            elif output_format.lower() == 'geojson':
                output_file = output_dir / f'{time_info}.geojson'
                merged_gdf.to_file(output_file, driver='GeoJSON')
            elif output_format.lower() == 'gpkg':
                output_file = output_dir / f'{time_info}.gpkg'
                merged_gdf.to_file(output_file, driver='GPKG')
            else:
                raise ValueError(f"不支持的输出格式: {output_format}")
            
            print(f"保存文件: {output_file} (记录数: {len(merged_gdf)}, 已简化几何, 格式: {output_format.upper()})")
            total_files += 1
    
    print(f"\n{time_period} 数据合并完成!")
    print(f"总共生成了 {total_files} 个文件")
    
    return total_files

def main():
    print(f"开始处理冰架数据整合... (输出格式: {output_format.upper()})")
    
    # 处理三个时间维度
    time_periods = ['annual', 'monthly', 'quarterly']
    
    for period in time_periods:
        print(f"\n正在处理 {period} 数据...")
        file_count = merge_gpkg_files(period, output_format)
        print(f"{period} 处理完成，共生成 {file_count} 个 {output_format.upper()} 文件")
    
    print("\n所有数据整合完成!")

if __name__ == "__main__":
    main()