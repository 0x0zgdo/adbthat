#!/usr/bin/env python3
import subprocess
import sys

def extract_base_apk(package_name):
    try:
        # Get all APK paths
        result = subprocess.run(
            ['adb', 'shell', f'su -c \'pm path {package_name}\''],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Filter for base.apk :)
        base_apk = None
        for line in result.stdout.strip().split('\n'):
            if 'base.apk' in line:
                base_apk = line.split(':')[1].strip()
                break
        
        if not base_apk:
            print(f"base.apk not found for package: {package_name}")
            print("This might be a non-split APK or system app")
            sys.exit(1)
        
        print(f"Found base APK: {base_apk}")
        
        # Copy to /sdcard
        output_path = f"/sdcard/{package_name}_base.apk"
        subprocess.run(
            ['adb', 'shell', f'su -c \'cp {base_apk} {output_path} && chmod 644 {output_path}\''],
            check=True
        )
        
        print(f"✓ base.apk extracted to: {output_path}")
        
    except subprocess.CalledProcessError:
        print(f"Error: Package not found or root access denied")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <package_name>")
        sys.exit(1)
    
    extract_base_apk(sys.argv[1])
