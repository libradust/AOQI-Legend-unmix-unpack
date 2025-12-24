"""
这个脚本的 拆分图集 功能依赖于 foxsugar 开发的 unpack_atlas 项目
unpack_atlas 项目地址 https://github.com/foxsugar/unpack_atlas
该项目遵循 [MIT License] 开源协议。
"""


import os,shutil,time
import PIL.Image as Image
import unpack
import unmix

script_dir = os.path.dirname(os.path.abspath(__file__))



def atlas_function()->str:
    """转换atlas文件中的后缀"""
    for filename in os.listdir(script_dir):
        if filename.lower().endswith('.atlas'):
            atlas_path = os.path.join(script_dir, filename)
            atlas_base_name,atlas_extension=os.path.splitext(filename)
            with open(atlas_path, 'r') as file:
                content = file.read()
            content = content.replace('.webp', '.png')
            with open(atlas_path, 'w') as file:
                file.write(content)
    return atlas_base_name

def webp_function(atlas_base_name)->None:
    """转换webp为png"""
    for filename in os.listdir(script_dir):
        if filename.lower().endswith('.webp'):
            webp_path = os.path.join(script_dir, filename)
            new_filename=atlas_base_name+'.png'
            new_png_path=os.path.join(script_dir,new_filename)
            with Image.open(webp_path) as img:
                img.save(new_png_path,'PNG')
            os.remove(webp_path)

def _check_content_ready() -> bool:
    """检查需要的文件"""
    atlas_found=False
    webp_found=False
    try:
        while True:
            for filename in os.listdir(script_dir):
                if filename.lower().endswith('.atlas'):
                    atlas_found=True
                if filename.lower().endswith('.webp'):
                    webp_found=True
                if atlas_found and webp_found:
                    return True
    except FileNotFoundError:
        print("文件未找到，稍后重试...")
    time.sleep(0.5)

if __name__ == "__main__":

    # 使用unmix.py中的unmix_function函数解包.mix文件
    unmix.unmix_function()

    # 解压检查
    ready=_check_content_ready()
    
    if ready:
        # 使用atlas_function和webp_function转换atlas文件和webp图片
        atlas_base_name=atlas_function()
        webp_function(atlas_base_name)

        # 使用unpack.py拆分图集
        dir1 = os.getcwd()
        unpack.unpack(dir1)

        # 清理多余文件
        shutil.rmtree(os.path.join(script_dir,'__pycache__'))
        os.remove(os.path.join(script_dir, "__names__.txt"))
       
    
