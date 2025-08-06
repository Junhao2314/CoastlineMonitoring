import os
import glob
import geopandas as gpd
from shapely.geometry import LineString, MultiLineString
import pandas as pd

def read_coastline_file(file_path):
    """
    读取南极海岸线文件并解析坐标数据
    """
    coordinates_groups = []
    current_group = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # 跳过注释行
            if line.startswith('#') or line.startswith('"#'):
                continue
            
            # 检查是否为分隔行 (NaN NaN)
            if 'NaN' in line or line == '':
                if current_group:
                    coordinates_groups.append(current_group)
                    current_group = []
                continue
            
            # 解析坐标
            try:
                parts = line.split(',')
                if len(parts) == 2:
                    x, y = float(parts[0]), float(parts[1])
                    current_group.append([x, y])
            except ValueError:
                continue
    
    # 添加最后一组坐标
    if current_group:
        coordinates_groups.append(current_group)
    
    return coordinates_groups

def filter_coordinates(coordinates_groups):
    """
    过滤坐标组，保持原始EPSG:3031坐标系
    """
    filtered_groups = []
    for group in coordinates_groups:
        if len(group) >= 2:  # 只保留有效的线段
            filtered_groups.append(group)
    
    return filtered_groups

def create_geometry(coordinates_groups):
    """
    创建Shapely几何对象
    """
    if not coordinates_groups:
        return None
    
    # 如果只有一个坐标组，创建LineString
    if len(coordinates_groups) == 1:
        return LineString(coordinates_groups[0])
    else:
        # 多个坐标组，创建MultiLineString
        linestrings = []
        for coords in coordinates_groups:
            if len(coords) >= 2:
                linestrings.append(LineString(coords))
        
        if len(linestrings) == 1:
            return linestrings[0]
        elif len(linestrings) > 1:
            return MultiLineString(linestrings)
        else:
            return None

def process_all_files(input_folder, output_folder):
    """
    处理所有海岸线文件并转换为GPKG
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 获取所有txt文件
    txt_files = glob.glob(os.path.join(input_folder, '*.txt'))
    txt_files.sort()
    
    print(f"找到 {len(txt_files)} 个文件")
    
    all_data = []
    
    for file_path in txt_files:
        filename = os.path.basename(file_path)
        print(f"处理文件: {filename}")
        
        # 从文件名提取年份
        try:
            year_str = filename.replace('antarctic_coastline_', '').replace('.txt', '')
            year = float(year_str)
        except ValueError:
            print(f"无法解析年份: {filename}")
            continue
        
        # 读取坐标数据
        coordinates_groups = read_coastline_file(file_path)
        print(f"  读取到 {len(coordinates_groups)} 个坐标组")
        
        if not coordinates_groups:
            print(f"  警告: 文件 {filename} 没有有效坐标")
            continue
        
        # 过滤坐标组
        filtered_groups = filter_coordinates(coordinates_groups)
        print(f"  过滤后有 {len(filtered_groups)} 个有效坐标组")
        
        if not filtered_groups:
            print(f"  警告: 文件 {filename} 过滤后为空")
            continue
        
        # 创建几何对象
        geometry = create_geometry(filtered_groups)
        
        if geometry is None:
            print(f"  警告: 文件 {filename} 无法创建几何对象")
            continue
        
        # 添加到数据列表
        all_data.append({
            'year': year,
            'filename': filename,
            'description': f'Antarctic coastline for year {year}',
            'coord_groups': len(filtered_groups),
            'geometry': geometry
        })
        
        print(f"  成功处理年份: {year}")
    
    if not all_data:
        print("没有有效数据可以转换")
        return 0
    
    # 创建GeoDataFrame
    gdf = gpd.GeoDataFrame(all_data)
    
    # 设置坐标参考系统 (EPSG:3031 - Antarctic Polar Stereographic)
    gdf.crs = 'EPSG:3031'
    
    # 保存为GPKG文件
    output_path = os.path.join(output_folder, 'antarctic_coastlines.gpkg')
    gdf.to_file(output_path, driver='GPKG')
    
    print(f"\n总共处理了 {len(all_data)} 个年份的数据")
    print(f"GPKG文件保存为: {output_path}")
    
    # 保存每年的单独GPKG文件
    for _, row in gdf.iterrows():
        year = row['year']
        single_gdf = gpd.GeoDataFrame([row])
        single_gdf.crs = 'EPSG:3031'
        
        single_output_path = os.path.join(output_folder, f'antarctic_coastline_{year}.gpkg')
        single_gdf.to_file(single_output_path, driver='GPKG')
        print(f"  单独保存: antarctic_coastline_{year}.gpkg")
    
    return len(all_data)

def create_summary_info(output_folder):
    """
    创建数据摘要信息
    """
    gpkg_path = os.path.join(output_folder, 'antarctic_coastlines.gpkg')
    
    if not os.path.exists(gpkg_path):
        return
    
    # 读取GPKG文件
    gdf = gpd.read_file(gpkg_path)
    
    print("\n=" * 60)
    print("📊 GPKG数据摘要")
    print("=" * 60)
    print(f"总记录数: {len(gdf)}")
    print(f"坐标系: {gdf.crs}")
    print(f"年份范围: {gdf['year'].min()} - {gdf['year'].max()}")
    print(f"几何类型: {gdf.geometry.type.value_counts().to_dict()}")
    print(f"边界范围: {gdf.total_bounds}")
    
    # 保存摘要到文本文件
    summary_path = os.path.join(output_folder, 'data_summary.txt')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("南极海岸线GPKG数据摘要\n")
        f.write("=" * 40 + "\n")
        f.write(f"总记录数: {len(gdf)}\n")
        f.write(f"坐标系: {gdf.crs}\n")
        f.write(f"年份范围: {gdf['year'].min()} - {gdf['year'].max()}\n")
        f.write(f"几何类型: {gdf.geometry.type.value_counts().to_dict()}\n")
        f.write(f"边界范围: {gdf.total_bounds}\n")
        f.write("\n文件列表:\n")
        for year in sorted(gdf['year']):
            f.write(f"  antarctic_coastline_{year}.gpkg\n")
    
    print(f"摘要信息保存到: {summary_path}")

def main():
    input_folder = 'antarctic_coastlines_data'
    output_folder = 'antarctic_gpkg'
    
    print("开始转换南极海岸线数据为GPKG格式...")
    print(f"输入文件夹: {input_folder}")
    print(f"输出文件夹: {output_folder}")
    print()
    
    # 检查输入文件夹是否存在
    if not os.path.exists(input_folder):
        print(f"错误: 输入文件夹 '{input_folder}' 不存在")
        print("请确保南极海岸线数据文件夹存在")
        return
    
    try:
        processed_count = process_all_files(input_folder, output_folder)
        
        if processed_count > 0:
            print(f"\n转换完成! 成功处理了 {processed_count} 个文件")
            print(f"GPKG文件保存在: {os.path.abspath(output_folder)}")
            
            # 创建摘要信息
            create_summary_info(output_folder)
            
            print("\n📋 使用建议:")
            print("1. 使用QGIS打开GPKG文件进行可视化")
            print("2. 在Python中使用geopandas读取数据")
            print("3. 坐标系为EPSG:3031 (Antarctic Polar Stereographic)")
            print("4. 可以转换到其他坐标系进行分析")
        else:
            print("\n没有成功处理任何文件")
        
    except Exception as e:
        print(f"转换过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()