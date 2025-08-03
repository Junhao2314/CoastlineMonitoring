#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载Icelines数据的Python脚本
"""

# 配置选项
max_workers = 4        # 并发下载线程数
skip_daily = True      # 跳过daily文件夹下载
skip_monthly = False   # 跳过monthly文件夹下载
skip_annual = False    # 跳过annual文件夹下载
skip_quarterly = False # 跳过quarterly文件夹下载

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from multiprocessing import cpu_count

# 线程安全的打印锁
print_lock = threading.Lock()

def safe_print(message):
    """线程安全的打印函数"""
    with print_lock:
        print(message)

def create_directory(path):
    """创建目录"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"创建目录: {path}")

def download_file(url, local_path, max_retries=3):
    """下载单个文件，支持重试和跳过已存在文件"""
    # 检查文件是否已存在
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        safe_print(f"  跳过已存在: {os.path.basename(local_path)}")
        return True
    
    safe_print(f"  下载文件: {os.path.basename(local_path)}")
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # 创建临时文件
            temp_path = local_path + '.tmp'
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # 下载完成后重命名
            os.rename(temp_path, local_path)
            safe_print(f"    ✓ 成功: {os.path.basename(local_path)}")
            return True
            
        except Exception as e:
            if attempt < max_retries - 1:
                safe_print(f"    ⚠ 重试 {attempt + 1}/{max_retries}: {os.path.basename(local_path)} - {str(e)}")
                time.sleep(2 ** attempt)  # 指数退避
                # 清理可能的临时文件
                temp_path = local_path + '.tmp'
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            else:
                safe_print(f"    ✗ 失败: {os.path.basename(local_path)} - {str(e)}")
                # 清理可能的临时文件
                temp_path = local_path + '.tmp'
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return False
    
    return False

def get_directory_links(url):
    """获取目录中的所有链接"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        
        # 查找所有的链接
        for link in soup.find_all('a', href=True):
            href = link['href']
            # 跳过父目录、排序链接和绝对URL
            if (href == '../' or 
                href.startswith('?') or 
                href.startswith('http://') or 
                href.startswith('https://') or
                href.startswith('mailto:') or
                href.startswith('ftp://') or
                '://' in href or
                href.startswith('/')):
                continue
            # 只保留相对路径的文件和目录
            if href and not href.startswith('#'):
                links.append(href)
        
        return links
    except Exception as e:
        safe_print(f"无法访问目录: {url} - {str(e)}")
        return []

def download_file_task(file_info):
    """单个文件下载任务"""
    file_url, local_file_path = file_info
    return download_file(file_url, local_file_path)

def download_directory_recursive(base_url, relative_path, local_base_path, max_workers=None):
    """递归下载目录中的所有内容，支持并发下载"""
    if max_workers is None:
        max_workers = 4  # 限制并发数为4，避免服务器过载
    
    current_url = urljoin(base_url, relative_path)
    current_local_path = os.path.join(local_base_path, relative_path.strip('/'))
    
    safe_print(f"处理目录: {relative_path} (并发数: {max_workers})")
    create_directory(current_local_path)
    
    links = get_directory_links(current_url)
    
    # 分离文件和目录
    files_to_download = []
    subdirectories = []
    
    for link in links:
        if link.endswith('/'):
            # 这是一个子目录
            folder_name = link.rstrip('/')
            # 检查是否需要跳过特定类型的文件夹
            if skip_daily and folder_name == 'daily':
                safe_print(f"  跳过daily文件夹: {relative_path}{link}")
                continue
            elif skip_monthly and folder_name == 'monthly':
                safe_print(f"  跳过monthly文件夹: {relative_path}{link}")
                continue
            elif skip_annual and folder_name == 'annual':
                safe_print(f"  跳过annual文件夹: {relative_path}{link}")
                continue
            elif skip_quarterly and folder_name == 'quarterly':
                safe_print(f"  跳过quarterly文件夹: {relative_path}{link}")
                continue
            subdirectories.append(link)
        else:
            # 这是一个文件
            file_url = urljoin(current_url, link)
            local_file_path = os.path.join(current_local_path, link)
            files_to_download.append((file_url, local_file_path))
    
    # 并发下载当前目录中的所有文件
    if files_to_download:
        safe_print(f"  开始并发下载 {len(files_to_download)} 个文件...")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {executor.submit(download_file_task, file_info): file_info for file_info in files_to_download}
            
            completed = 0
            for future in as_completed(future_to_file):
                file_info = future_to_file[future]
                try:
                    result = future.result()
                    completed += 1
                    if completed % 10 == 0:  # 每10个文件报告一次进度
                        safe_print(f"  已完成: {completed}/{len(files_to_download)} 个文件")
                except Exception as exc:
                    safe_print(f"  文件下载异常: {file_info[1]} - {exc}")
        
        safe_print(f"  目录 {relative_path} 中的文件下载完成: {len(files_to_download)} 个")
    
    # 递归处理子目录
    for subdir in subdirectories:
        sub_relative_path = relative_path + subdir
        download_directory_recursive(base_url, sub_relative_path, local_base_path, max_workers)

def main():
    """主函数"""
    base_url = "https://download.geoservice.dlr.de/icelines/files/"
    data_dir = "data"
    
    # 显示系统信息
    cpu_cores = cpu_count()
    safe_print(f"=== Icelines 数据并发下载器 ===")
    safe_print(f"CPU 核心数: {cpu_cores}")
    safe_print(f"并发下载线程数: {max_workers} (限制以避免服务器过载)")
    safe_print(f"跳过daily文件夹: {'是' if skip_daily else '否'}")
    safe_print(f"跳过monthly文件夹: {'是' if skip_monthly else '否'}")
    safe_print(f"跳过annual文件夹: {'是' if skip_annual else '否'}")
    safe_print(f"跳过quarterly文件夹: {'是' if skip_quarterly else '否'}")
    safe_print(f"目标目录: {os.path.abspath(data_dir)}")
    safe_print("="*40)
    
    # 创建数据目录
    create_directory(data_dir)
    
    # 定义所有文件夹名称
    folders = [
        "Abbot1", "Abbot2", "Amery", "Bach", "Baudouin1", "Baudouin2", "Baudouin3",
        "Brunt1", "Brunt2", "Cook", "Cosgrove", "Crosson", "David", "Denman",
        "Dotson", "Ekstromisen", "Filchner", "Fimbul1", "Fimbul2", "Fimbul3",
        "GeorgeNorth", "GeorgeSouth", "Getz1", "Getz2", "Getz3", "Holmes",
        "Jelbart", "LarsenC", "Lazarev", "Mertz", "Moskow", "Nickerson",
        "PineIsland", "Quarisen", "Riiser1", "Riiser2", "Ronne1", "Ronne2",
        "Ross1", "Ross2", "Ross3", "Shackleton", "Stange", "Sulzberger",
        "Thwaites1", "Thwaites2", "Totten", "Venable", "West1", "West2", "Wilkins"
    ]
    
    # 定义zip文件
    zip_files = [
        "icelines_antarctic_coastline_2018.zip",
        "icelines_auxiliary_v1.zip"
    ]
    
    # 下载zip文件
    safe_print("开始下载zip文件...")
    for zip_file in zip_files:
        zip_url = urljoin(base_url, zip_file)
        local_zip_path = os.path.join(data_dir, zip_file)
        download_file(zip_url, local_zip_path)
    
    # 递归下载所有文件夹
    safe_print("\n开始并发递归下载文件夹...")
    for i, folder in enumerate(folders, 1):
        folder_relative_path = folder + "/"
        safe_print(f"\n[{i}/{len(folders)}] 处理文件夹: {folder}")
        download_directory_recursive(base_url, folder_relative_path, data_dir)
        safe_print(f"✓ 完成文件夹: {folder}")
    
    safe_print("\n🎉 所有下载任务完成！")
    safe_print(f"所有数据已保存到: {os.path.abspath(data_dir)}")

if __name__ == "__main__":
    main()