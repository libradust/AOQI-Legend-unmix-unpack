import os
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
SEVEN_ZIP_EXE=r".\7z\7z.exe"

def unmix_function()->None:
    """通过7z解包.mix文件"""
    for filename in os.listdir(script_dir):
        if filename.lower().endswith('.mix'):
            mix_path = os.path.join(script_dir, filename)
            unmix_command=[SEVEN_ZIP_EXE, 'x', mix_path, '-o' + script_dir, '-y']
            try:
                subprocess.run(
                    unmix_command,
                    text=True,
                    check=True,
                    capture_output=True
                )  
            except subprocess.CalledProcessError as e:
                print(f"Error unpacking {filename}:\n{e.stderr}")
            else:
                print(f"Successfully unpacked {filename}\n")

if __name__ == "__main__":
    unmix_function()            
        