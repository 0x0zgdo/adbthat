import subprocess
import sys
import os

def run_root_commands(commands):
    
    process = subprocess.Popen(
        ['adb', 'shell'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # I'm assuming you already have root access on the device :)
    command_sequence = 'su\n' + '\n'.join(commands) + '\nexit\nexit\n'
    stdout, stderr = process.communicate(command_sequence)
    return stdout, stderr, process.returncode

def extract_data_folder(package_name):
    try:
        data_path = f"/data/data/{package_name}"
        
        # Check if directory exists
        print("Checking if data directory exists...")
        commands = [
            f'cd {data_path}',
            'pwd'
        ]
        stdout, stderr, returncode = run_root_commands(commands)
        
        if data_path not in stdout:
            print(f"Data directory not found: {data_path}")
            sys.exit(1)
        
        print(f"Found data directory: {data_path}")
        
        # Create temporary archive on device
        temp_archive = f"/sdcard/{package_name}_data.tar.gz"
        print("Creating archive...")
        commands = [
            'cd /data/data',
            f'tar -czf {temp_archive} {package_name}',
            'echo "Archive created"'
        ]
        stdout, stderr, returncode = run_root_commands(commands)
        
        if 'Archive created' not in stdout:
            print(f"Error creating archive: {stderr}")
            sys.exit(1)
        
        # Pull archive to computer
        output_file = f"{package_name}_data.tar.gz"
        print("Downloading archive...")
        subprocess.run(['adb', 'pull', temp_archive, output_file], check=True)
        
        # Extract locally
        print("Extracting files...")
        subprocess.run(['tar', '-xzf', output_file], check=True)
        
        # Cleanup
        print("Cleaning up...")
        commands = [f'rm {temp_archive}']
        run_root_commands(commands)
        
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