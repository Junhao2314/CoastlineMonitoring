import requests
import os
from urllib.parse import urljoin
import time

def download_file(url, filename, folder_path):
    """下载单个文件"""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_path = os.path.join(folder_path, filename)
    
    # 检查文件是否已存在
    if os.path.exists(file_path):
        print(f"文件 {filename} 已存在，跳过下载")
        return True
    
    try:
        print(f"正在下载: {filename}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size > 0:
                        progress = (downloaded_size / total_size) * 100
                        print(f"\r下载进度: {progress:.1f}%", end='', flush=True)
        
        print(f"\n{filename} 下载完成")
        return True
        
    except Exception as e:
        print(f"\n下载 {filename} 失败: {str(e)}")
        if os.path.exists(file_path):
            os.remove(file_path)
        return False

def main():
    # Zenodo记录的基础URL
    base_url = "https://zenodo.org/records/5903643/files/"
    
    # 创建下载文件夹
    download_folder = "antarctic_coastlines_data"
    
    # 根据网页内容，生成所有年份的文件名
    files_to_download = []
    
    # 1997-2021年的文件列表（基于网页显示的文件）
    years_quarters = [
        "1997.75", "2000.2", "2000.75", "2001.2", "2002.2", "2003.2", 
        "2004.2", "2005.2", "2006.2", "2007.2", "2008.2", "2009.2", 
        "2010.2", "2011.2", "2012.2", "2013.2", "2014.2", "2015.2", 
        "2016.2", "2017.2", "2018.2", "2019.2", "2020.2", "2021.2"
    ]
    
    for year_quarter in years_quarters:
        filename = f"antarctic_coastline_{year_quarter}.txt"
        files_to_download.append(filename)
    
    print(f"准备下载 {len(files_to_download)} 个文件到文件夹: {download_folder}")
    print("文件列表:")
    for i, filename in enumerate(files_to_download, 1):
        print(f"{i:2d}. {filename}")
    
    # 开始下载
    successful_downloads = 0
    failed_downloads = 0
    
    for i, filename in enumerate(files_to_download, 1):
        print(f"\n[{i}/{len(files_to_download)}] ", end="")
        file_url = urljoin(base_url, filename)
        
        if download_file(file_url, filename, download_folder):
            successful_downloads += 1
        else:
            failed_downloads += 1
        
        # 添加延迟以避免过于频繁的请求
        time.sleep(1)
    
    print(f"\n\n下载完成!")
    print(f"成功下载: {successful_downloads} 个文件")
    print(f"下载失败: {failed_downloads} 个文件")
    print(f"文件保存在: {os.path.abspath(download_folder)}")

if __name__ == "__main__":
    main()