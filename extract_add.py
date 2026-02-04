# Extract Application Data Directory

import subprocess
import sys
import os

def extract_data_folder(package_name):
    try:
        data_path = f"/data/data/{package_name}"
        
       
        result = subprocess.run(
            ['adb', 'shell', f'su -c \'test -d {data_path} && echo yes || echo no\''],
            capture_output=True,
            text=True,
            check=True
        )
        
        if 'yes' not in result.stdout:
            print(f"Data directory not found: {data_path}")
            sys.exit(1)
        
        print(f"Found data directory: {data_path}")
        
      
        temp_archive = f"/sdcard/{package_name}_data.tar.gz"
        print("Creating archive...")
        subprocess.run(
            ['adb', 'shell', f'su -c \'cd /data/data && tar -czf {temp_archive} {package_name}\''],
            check=True
        )
        
      
        output_file = f"{package_name}_data.tar.gz"
        print("Downloading archive...")
        subprocess.run(['adb', 'pull', temp_archive, output_file], check=True)
        
       
        print("Extracting files...")
        subprocess.run(['tar', '-xzf', output_file], check=True)
        
       
        subprocess.run(['adb', 'shell', f'rm {temp_archive}'], check=True)
        
        print(f"✓ Data extracted to: ./{package_name}/")
        print(f"✓ Archive saved as: {output_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <package_name>")
        sys.exit(1)
    
    extract_data_folder(sys.argv[1])