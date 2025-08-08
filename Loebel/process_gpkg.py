import geopandas as gpd
import os

# --- 配置 ---
# 输入文件
input_gpkg = 'coastlines_all_glaciers.gpkg'
# 输出目录
output_directory = 'Loebel'

# --- 脚本执行 ---

def extract_year_from_landsat_id(landsat_id):
    """从LANDSAT_ID中提取年份。"""
    try:
        # 示例: LC08_L1GT_217105_20140109_20201016_02_T2 -> 2014
        return landsat_id.split('_')[3][:4]
    except IndexError:
        return None

def process_gpkg_by_year(gpkg_file, out_dir):
    """按年份处理gpkg文件并导出为GeoJSON。"""
    # 确保输出目录存在
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        print(f"已创建输出目录: {out_dir}")

    # 检查输入文件是否存在
    if not os.path.exists(gpkg_file):
        print(f"错误：输入文件不存在 -> {gpkg_file}")
        return

    print(f"--- 开始处理文件: {gpkg_file} ---")
    try:
        # 读取gpkg文件
        gdf = gpd.read_file(gpkg_file)

        # 检查 'LANDSAT_ID' 字段是否存在
        if 'LANDSAT_ID' not in gdf.columns:
            print(f"错误：文件中缺少 'LANDSAT_ID' 字段。")
            return

        print("正在提取年份...")
        # 提取年份并创建一个新列
        gdf['year'] = gdf['LANDSAT_ID'].apply(extract_year_from_landsat_id)

        # 过滤掉没有年份的数据
        gdf = gdf.dropna(subset=['year'])

        # 按年份分组
        grouped = gdf.groupby('year')

        print("按年份导出为 GeoJSON 文件...")
        for year, group in grouped:
            output_filename = f"{year}.geojson"
            output_path = os.path.join(out_dir, output_filename)
            print(f"正在导出到: {output_path}")
            # 导出为GeoJSON文件
            group.to_file(output_path, driver='GeoJSON')

        print("--- 文件处理完成！ ---")

    except Exception as e:
        print(f"处理文件 '{gpkg_file}' 时发生错误: {e}")

if __name__ == "__main__":
    process_gpkg_by_year(input_gpkg, output_directory)