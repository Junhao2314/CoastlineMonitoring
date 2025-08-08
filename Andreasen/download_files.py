import os
import sys
import requests

# Directory to save the downloaded files
DOWNLOAD_DIR = "zenodo_downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Function to download a file
def download_file(file_url, download_folder):
    # Extract filename from URL, handling query parameters
    filename = file_url.split('/')[-1].split('?')[0]
    local_filename = os.path.join(download_folder, filename)
    
    print(f"Downloading {file_url} to {local_filename}")
    with requests.get(file_url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Successfully downloaded {local_filename}")
    return local_filename

def main():
    # Check if a URL is provided as a command-line argument
    if len(sys.argv) > 1:
        file_url = sys.argv[1]
        try:
            download_file(file_url, DOWNLOAD_DIR)
        except Exception as e:
            print(f"Failed to download {file_url}. Error: {e}")
    else:
        # New logic: use a predefined list of files.
        filenames = [
            "Abbot_CalvingFronts.zip", "Amery_CalvingFronts.zip", "Bach_CalvingFronts.zip",
            "Baudouin_CalvingFronts.zip", "Brunt_CalvingFronts.zip", "Crosson_CalvingFronts.zip",
            "Dotson_CalvingFronts.zip", "Drygalski_CalvingFronts.zip", "Filchner_CalvingFronts.zip",
            "Fimbul_CalvingFronts.zip", "George_CalvingFronts.zip", "GetzEast_CalvingFronts.zip",
            "GetzWest_CalvingFronts.zip", "LarsA_CalvingFronts.zip", "LarsB_CalvingFronts.zip",
            "LarsC_CalvingFronts.zip", "Mertz_CalvingFronts.zip", "Moscow_CalvingFronts.zip",
            "Nansen_CalvingFronts.zip", "Ninnis_CalvingFronts.zip", "PineIsland_CalvingFronts.zip",
            "RiiserLarsen_CalvingFronts.zip", "Ronne_CalvingFronts.zip", "RossEast_CalvingFronts.zip",
            "RossWest_CalvingFronts.zip", "Shackleton_CalvingFronts.zip", "Stange_CalvingFronts.zip",
            "Sulzberger_CalvingFronts.zip", "Swinburne_CalvingFronts.zip", "Thwaites_CalvingFronts.zip",
            "Totten_CalvingFronts.zip", "West_CalvingFronts.zip", "Wilkins_CalvingFronts.zip",
            "Wordie_CalvingFronts.zip"
        ]
        
        base_url = "https://zenodo.org/records/7830051/files/"
        
        file_links = [f"{base_url}{fname}?download=1" for fname in filenames]

        if not file_links:
            print("No files to download.")
        else:
            print(f"Found {len(file_links)} files to download.")
            # Download each file
            for file_link in file_links:
                try:
                    download_file(file_link, DOWNLOAD_DIR)
                except Exception as e:
                    print(f"Failed to download {file_link}. Error: {e}")

    print("All downloads finished.")

if __name__ == "__main__":
    main()