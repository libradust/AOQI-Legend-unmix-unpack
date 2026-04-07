import os
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
SEVEN_ZIP_EXE = r".\7z\7z.exe"

def unmix_function()->None:
    """解包.mix文件"""
    for filename in os.listdir(script_dir):
        if filename.lower().endswith('.mix'):
            mix_path = os.path.join(script_dir, filename)
            
            # 解压前的文件列表
            before_files = set(os.listdir(script_dir))

            unmix_command = [SEVEN_ZIP_EXE, 'x', mix_path, '-o' + script_dir, '-y']
            try:
                subprocess.run(
                    unmix_command,
                    text=True,
                    check=True,
                    capture_output=True
                )  
            except subprocess.CalledProcessError as e:
                print(f"错误解包 {filename}:\n{e.stderr}")
            else:
                # 输出解包后的内容
                after_files = set(os.listdir(script_dir))
                new_files = after_files - before_files
                print(f"✅ 成功解包：{filename}")
                print("📂 解出的文件：")
                for f in new_files:
                    if f == "__names__.txt":
                        print(f"  - {f} (无用)")
                    else:
                        print(f"  - {f}")

if __name__ == "__main__":
    unmix_function()            