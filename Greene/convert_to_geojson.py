import os
import json
import numpy as np
import glob

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

def create_geojson_feature(coordinates_groups, year, properties=None):
    """
    创建GeoJSON要素
    """
    if properties is None:
        properties = {}
    
    properties['year'] = year
    properties['description'] = f'Antarctic coastline for year {year}'
    
    # 如果只有一个坐标组，创建LineString
    if len(coordinates_groups) == 1:
        geometry = {
            "type": "LineString",
            "coordinates": coordinates_groups[0]
        }
    else:
        # 多个坐标组，创建MultiLineString
        geometry = {
            "type": "MultiLineString",
            "coordinates": coordinates_groups
        }
    
    feature = {
        "type": "Feature",
        "properties": properties,
        "geometry": geometry
    }
    
    return feature

def process_all_files(input_folder, output_folder):
    """
    处理所有海岸线文件并转换为GeoJSON
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 获取所有txt文件
    txt_files = glob.glob(os.path.join(input_folder, '*.txt'))
    txt_files.sort()
    
    print(f"找到 {len(txt_files)} 个文件")
    
    all_features = []
    
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
        
        # 创建GeoJSON要素
        feature = create_geojson_feature(filtered_groups, year)
        all_features.append(feature)
        
        # 保存单个文件的GeoJSON
        single_geojson = {
            "type": "FeatureCollection",
            "features": [feature]
        }
        
        output_filename = filename.replace('.txt', '.geojson')
        output_path = os.path.join(output_folder, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(single_geojson, f, indent=2, ensure_ascii=False)
        
        print(f"  保存到: {output_filename}")
    
    print(f"\n总共处理了 {len(all_features)} 个年份的数据")
    
    return len(all_features)

def main():
    input_folder = 'antarctic_coastlines_data'
    output_folder = 'Greene'
    
    print("开始转换南极海岸线数据为GeoJSON格式...")
    print(f"输入文件夹: {input_folder}")
    print(f"输出文件夹: {output_folder}")
    print()
    
    try:
        processed_count = process_all_files(input_folder, output_folder)
        print(f"\n转换完成! 成功处理了 {processed_count} 个文件")
        print(f"GeoJSON文件保存在: {os.path.abspath(output_folder)}")
        
    except Exception as e:
        print(f"转换过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()