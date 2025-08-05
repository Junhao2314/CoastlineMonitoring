#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将GPKG文件转换为GeoJSON格式
支持几何简化功能
"""

import os
import geopandas as gpd
from pathlib import Path
import json

def convert_gpkg_to_geojson(input_dir="temp", output_dir="ADD", simplify_tolerance=10):
    """
    将GPKG文件转换为GeoJSON格式
    
    Args:
        input_dir: 输入目录（包含GPKG文件）
        output_dir: 输出目录（保存GeoJSON文件）
        simplify_tolerance: 简化容差（米），默认10米
    """
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # 获取所有GPKG文件
    input_path = Path(input_dir)
    gpkg_files = list(input_path.glob("*.gpkg"))
    
    if not gpkg_files:
        print(f"在 {input_dir} 目录中未找到GPKG文件")
        return
    
    print(f"找到 {len(gpkg_files)} 个GPKG文件")
    print(f"简化容差: {simplify_tolerance} 米")
    print("="*60)
    
    success_count = 0
    failed_count = 0
    
    for gpkg_file in gpkg_files:
        try:
            print(f"\n处理文件: {gpkg_file.name}")
            
            # 读取GPKG文件
            gdf = gpd.read_file(gpkg_file)
            print(f"  - 原始要素数量: {len(gdf)}")
            print(f"  - 坐标系: {gdf.crs}")
            
            # 转换到南极极地立体投影坐标系 EPSG:3031
            print("  - 转换坐标系到 EPSG:3031 (南极极地立体投影)...")
            gdf = gdf.to_crs('EPSG:3031')
            
            # 几何简化
            if simplify_tolerance > 0:
                print(f"  - 简化几何 (容差: {simplify_tolerance}m)...")
                gdf['geometry'] = gdf['geometry'].simplify(tolerance=simplify_tolerance)
                print(f"  - 简化后要素数量: {len(gdf)}")
            
            # 生成输出文件名
            output_filename = gpkg_file.stem + ".geojson"
            output_file = output_path / output_filename
            
            # 保存为GeoJSON
            print(f"  - 保存到: {output_file}")
            gdf.to_file(output_file, driver='GeoJSON')
            
            # 获取文件大小
            file_size = output_file.stat().st_size / (1024 * 1024)  # MB
            print(f"  - 文件大小: {file_size:.2f} MB")
            print(f"  ✓ 转换成功")
            
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ 转换失败: {str(e)}")
            failed_count += 1
    
    # 输出总结
    print("\n" + "="*60)
    print("转换完成总结:")
    print(f"成功转换: {success_count} 个文件")
    print(f"转换失败: {failed_count} 个文件")
    
    if success_count > 0:
        print(f"\n成功转换的文件保存在: {output_path.absolute()}")
        
        # 列出转换后的文件
        geojson_files = list(output_path.glob("*.geojson"))
        if geojson_files:
            print("\n转换后的GeoJSON文件:")
            for geojson_file in sorted(geojson_files):
                file_size = geojson_file.stat().st_size / (1024 * 1024)  # MB
                print(f"  - {geojson_file.name} ({file_size:.2f} MB)")

def main():
    """
    主函数
    """
    print("BAS南极海岸线数据 GPKG转GeoJSON工具")
    print("="*60)
    
    # 检查输入目录
    if not os.path.exists("temp"):
        print("错误: temp目录不存在")
        return
    
    # 执行转换
    convert_gpkg_to_geojson(
        input_dir="temp",
        output_dir="ADD", 
        simplify_tolerance=100  # 默认简化40米
    )

if __name__ == "__main__":
    main()