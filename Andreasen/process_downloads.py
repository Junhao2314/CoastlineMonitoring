import geopandas as gpd
import os
import zipfile
from collections import defaultdict

def process_downloaded_files(download_dir, output_dir):
    """Reads shapefiles directly from zip archives, merges by year, and exports to GeoJSON."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已创建输出目录: {output_dir}")

    yearly_data = defaultdict(list)

    for zip_filename in os.listdir(download_dir):
        if not zip_filename.endswith('.zip'):
            continue

        zip_path = os.path.join(download_dir, zip_filename)
        print(f"\n--- 正在处理: {zip_path} ---")

        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                # Find all shapefiles within the zip file, ignoring the __MACOSX directory
                shp_files = [f for f in z.namelist() if f.endswith('.shp') and not f.startswith('__MACOSX/')]
                
                for shp_in_zip in shp_files:
                    # Construct the special path for geopandas
                    uri = f"zip://{zip_path}!/{shp_in_zip}"
                    print(f"正在读取: {uri}")
                    
                    try:
                        gdf = gpd.read_file(uri)
                        
                        # Extract year and region name from the shapefile name
                        shp_filename_only = os.path.basename(shp_in_zip)
                        parts = os.path.splitext(shp_filename_only)[0].split('_')
                        year = parts[-1]
                        region_name = "_".join(parts[:-1])

                        # Add attributes
                        prop_name = 'Name'
                        if prop_name in gdf.columns:
                            prop_name = 'source_name'
                            i = 1
                            while prop_name in gdf.columns:
                                prop_name = f'source_name_{i}'
                                i += 1
                        gdf[prop_name] = region_name

                        yearly_data[year].append(gdf)
                        print(f"已处理并添加 {len(gdf)} 个要素到 {year} 年的数据中。")

                    except Exception as e:
                        print(f"处理文件 '{shp_in_zip}' 时出错: {e}")
        except zipfile.BadZipFile:
            print(f"错误: '{zip_filename}' 不是一个有效的zip文件，已跳过。")
        except Exception as e:
            print(f"处理zip文件 '{zip_filename}' 时发生未知错误: {e}")

    print("\n--- 正在合并和导出年度数据 ---")
    for year, gdfs in yearly_data.items():
        if not gdfs:
            continue
        
        print(f"正在合并 {year} 年的数据...")
        # Use concat from geopandas's pd
        merged_gdf = gpd.pd.concat(gdfs, ignore_index=True)
        
        # Ensure the CRS is consistent, taking the CRS from the first GeoDataFrame
        if gdfs:
            merged_gdf.crs = gdfs[0].crs

        # Clean up columns and re-index if 'id' column exists
        if 'id' in merged_gdf.columns:
            merged_gdf['id'] = range(len(merged_gdf))
            print(f"已为 {year} 年的数据重新编号 'id' 列。")

        # Drop columns where all values are null
        for col in merged_gdf.columns:
            if merged_gdf[col].isnull().all():
                merged_gdf = merged_gdf.drop(columns=[col])
                print(f"已移除全空的列 '{col}' 从 {year} 年的数据中。")

        output_filename = f"{year}.geojson"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"正在导出到: {output_path}")
        merged_gdf.to_file(output_path, driver='GeoJSON')

    print("\n--- 所有文件处理完成！ ---")

if __name__ == "__main__":
    download_directory = 'zenodo_downloads'
    output_directory = 'Andreasen'
    
    if not os.path.isdir(download_directory):
        print(f"错误：下载目录不存在 -> {download_directory}")
    else:
        process_downloaded_files(download_directory, output_directory)