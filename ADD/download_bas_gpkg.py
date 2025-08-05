#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载BAS南极海岸线中分辨率GPKG数据
"""

import os
import requests
from urllib.parse import urlparse

def download_file(url, save_dir, filename=None):
    """
    下载文件到指定目录
    
    Args:
        url (str): 下载链接
        save_dir (str): 保存目录
        filename (str): 指定文件名，如果为None则从URL中提取
    
    Returns:
        str: 下载的文件路径，如果失败返回None
    """
    try:
        # 确保目录存在
        os.makedirs(save_dir, exist_ok=True)
        
        # 确定文件名
        if filename is None:
            # 从URL中提取文件名
            if 'v7_10' in url:
                filename = "add_coastline_medium_res_line_v7_10.gpkg"
            elif 'v7_9' in url:
                filename = "add_coastline_medium_res_line_v7_9.gpkg"
            elif 'v7_8' in url:
                filename = "add_coastline_medium_res_line_v7_8.gpkg"
            elif 'v7_7' in url:
                filename = "add_coastline_medium_res_line_v7_7.gpkg"
            elif 'v7_6' in url:
                filename = "add_coastline_medium_res_line_v7_6.gpkg"
            elif 'v7_5' in url:
                filename = "add_coastline_medium_res_line_v7_5.gpkg"
            elif 'v7_4' in url:
                filename = "add_coastline_medium_res_line_v7_4.gpkg"
            elif 'v7.3' in url:
                filename = "add_coastline_medium_res_line_v7_3.gpkg"
            elif 'v7.2' in url:
                filename = "add_coastline_medium_res_line_v7_2.gpkg"
            else:
                # 尝试从URL路径中提取
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                if not filename or not filename.endswith('.gpkg'):
                    filename = "coastline_data.gpkg"
        
        file_path = os.path.join(save_dir, filename)
        
        # 检查文件是否已存在
        if os.path.exists(file_path):
            print(f"文件已存在: {file_path}")
            file_size = os.path.getsize(file_path)
            print(f"现有文件大小: {file_size / (1024*1024):.2f} MB")
            return file_path
        
        print(f"正在下载: {url}")
        print(f"保存到: {file_path}")
        
        # 发送请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        response.raise_for_status()
        
        # 获取文件大小
        total_size = int(response.headers.get('content-length', 0))
        
        # 下载文件
        downloaded_size = 0
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    
                    # 显示进度
                    if total_size > 0:
                        progress = (downloaded_size / total_size) * 100
                        print(f"\r下载进度: {progress:.1f}%", end='', flush=True)
        
        print(f"\n下载完成: {file_path}")
        print(f"文件大小: {downloaded_size / (1024*1024):.2f} MB")
        
        return file_path
        
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")
        return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None

def main():
    """
    主函数
    """
    # BAS GPKG下载链接列表
    datasets = [
        {
            'name': 'ADD海岸线中分辨率线数据 v7.10',
            'url': 'https://ramadda.data.bas.ac.uk/repository/entry/get/add_coastline_medium_res_line_v7_10.gpkg?entryid=synth%3Abc81931c-4e8e-439a-b3c9-d3d1fdb109df%3AL2FkZF9jb2FzdGxpbmVfbWVkaXVtX3Jlc19saW5lX3Y3XzEwLmdwa2c%3D'
        },
        {
            'name': 'ADD海岸线中分辨率线数据 v7.9',
            'url': 'https://ramadda.data.bas.ac.uk/repository/entry/get/add_coastline_medium_res_line_v7_9.gpkg?entryid=synth%3Af2792d06-1e9d-4e00-a5c6-37d43bee5297%3AL2FkZF9jb2FzdGxpbmVfbWVkaXVtX3Jlc19saW5lX3Y3XzkuZ3BrZw%3D%3D'
        },
        {
            'name': 'ADD海岸线中分辨率线数据 v7.8',
            'url': 'https://ramadda.data.bas.ac.uk/repository/entry/get/add_coastline_medium_res_line_v7_8.gpkg?entryid=synth%3Acddac04f-ea6e-439f-9e54-36db0d8c843f%3AL2FkZF9jb2FzdGxpbmVfbWVkaXVtX3Jlc19saW5lX3Y3XzguZ3BrZw%3D%3D'
        },
        {
            'name': 'ADD海岸线中分辨率线数据 v7.7',
            'url': 'https://ramadda.data.bas.ac.uk/repository/entry/get/add_coastline_medium_res_line_v7_7.gpkg?entryid=synth%3A480d9361-4254-4250-9c3f-3342fbdabe5e%3AL2FkZF9jb2FzdGxpbmVfbWVkaXVtX3Jlc19saW5lX3Y3XzcuZ3BrZw%3D%3D'
        },
        {
            'name': 'ADD海岸线中分辨率线数据 v7.6',
            'url': 'https://ramadda.data.bas.ac.uk/repository/entry/get/add_coastline_medium_res_line_v7_6.gpkg?entryid=synth%3A1db7f188-6c3e-46cf-a3bf-e39dbd77e14c%3AL2FkZF9jb2FzdGxpbmVfbWVkaXVtX3Jlc19saW5lX3Y3XzYuZ3BrZw%3D%3D'
        },
        {
            'name': 'ADD海岸线中分辨率线数据 v7.5',
            'url': 'https://ramadda.data.bas.ac.uk/repository/entry/get/add_coastline_medium_res_line_v7_5.application/geopackage+sqlite3?entryid=synth%3A4e09c5d9-edf4-448e-aea7-2e56e9376aae%3AL2FkZF9jb2FzdGxpbmVfbWVkaXVtX3Jlc19saW5lX3Y3XzUuZ3BrZw%3D%3D'
        },
        {
            'name': 'ADD海岸线中分辨率线数据 v7.4',
            'url': 'https://ramadda.data.bas.ac.uk/repository/entry/get/add_coastline_medium_res_line_v7_4.application/geopackage+sqlite3?entryid=synth%3A824b5350-763e-4933-bb76-09f5d24cb033%3AL2FkZF9jb2FzdGxpbmVfbWVkaXVtX3Jlc19saW5lX3Y3XzQuZ3BrZw%3D%3D'
        },
        {
            'name': 'ADD海岸线中分辨率线数据 v7.3',
            'url': 'https://ramadda.data.bas.ac.uk/repository/entry/get/add_coastline_medium_res_line_v7.3.application/geopackage+sqlite3?entryid=synth%3A38f95030-09dd-4097-a97a-745fbbe27891%3AL2FkZF9jb2FzdGxpbmVfbWVkaXVtX3Jlc19saW5lX3Y3LjMuZ3BrZw%3D%3D'
        },
        {
            'name': 'ADD海岸线中分辨率线数据 v7.2',
            'url': 'https://ramadda.data.bas.ac.uk/repository/entry/get/add_coastline_medium_res_line_v7.2.application/geopackage+sqlite3?entryid=synth%3A3e2dee3a-8e15-4145-a3e2-68d532bd40d1%3AL2FkZF9jb2FzdGxpbmVfbWVkaXVtX3Jlc19saW5lX3Y3LjIuZ3BrZw%3D%3D'
        }
    ]
    
    # 保存目录
    save_dir = "temp"
    
    print("开始下载BAS南极海岸线中分辨率数据...")
    print(f"共有 {len(datasets)} 个数据集需要下载\n")
    
    successful_downloads = []
    failed_downloads = []
    
    # 下载所有数据集
    for i, dataset in enumerate(datasets, 1):
        print(f"[{i}/{len(datasets)}] 处理数据集: {dataset['name']}")
        
        result = download_file(dataset['url'], save_dir)
        
        if result:
            successful_downloads.append({
                'name': dataset['name'],
                'path': result,
                'size': os.path.getsize(result)
            })
            print(f"✓ 下载成功: {os.path.basename(result)}\n")
        else:
            failed_downloads.append(dataset['name'])
            print(f"✗ 下载失败: {dataset['name']}\n")
    
    # 输出总结
    print("="*60)
    print("下载完成总结:")
    print(f"成功下载: {len(successful_downloads)} 个数据集")
    print(f"下载失败: {len(failed_downloads)} 个数据集")
    
    if successful_downloads:
        print("\n成功下载的文件:")
        total_size = 0
        for item in successful_downloads:
            size_mb = item['size'] / (1024*1024)
            total_size += size_mb
            print(f"  - {os.path.basename(item['path'])} ({size_mb:.2f} MB)")
        print(f"\n总下载大小: {total_size:.2f} MB")
        print(f"文件保存目录: {os.path.abspath(save_dir)}")
    
    if failed_downloads:
        print("\n下载失败的数据集:")
        for name in failed_downloads:
            print(f"  - {name}")

if __name__ == "__main__":
    main()