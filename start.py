"""
这个脚本的 拆分图集 功能来自 foxsugar 的 unpack_atlas 项目
LINK:   https://github.com/foxsugar/unpack_atlas
该项目遵循 [MIT License]
"""


import os,shutil,time
import PIL.Image as Image
import unpack
import unmix

script_dir = os.path.dirname(os.path.abspath(__file__))



def atlas_function()->str:
    """修改atlas文件中的对应图片"""
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

def resave_img_function(atlas_base_name)->None:
    """转换非png的图集为png"""
    for filename in os.listdir(script_dir):
        if filename.lower().endswith(('.webp','.jpg','.jpeg')):
            img_path = os.path.join(script_dir, filename)
            new_filename=atlas_base_name+'.png'
            new_png_path=os.path.join(script_dir,new_filename)
            with Image.open(img_path) as img:
                img.save(new_png_path,'PNG')
            os.remove(img_path)

def _check_content_ready():
    """检查需要的文件"""
    atlas_found=False
    img_found=False
    try:
        for filename in os.listdir(script_dir):
            if filename.lower().endswith('.atlas'):
                atlas_found=True
                atlas_name=filename
                
            if filename.lower().endswith(('.webp','.png','.jpg','.jpeg')):
                img_found=True
                img_name=filename
                
            if atlas_found and img_found:
                return True, atlas_name, img_name
            
        print("文件未全部找到，确保目录下只有一个atlas文件和一个图集\n"
            "支持的图集格式包括: .webp, .png, .jpg, .jpeg\n")
        return False, None, None

    except Exception as e:
        print("检查文件时发生错误: " + str(e))
        return False, None, None

def _delete_temp_files():
    """清理多余文件"""
    try:
        shutil.rmtree(os.path.join(script_dir,'__pycache__'))
        os.remove(os.path.join(script_dir, "__names__.txt"))
    except Exception as e:
        pass

if __name__ == "__main__":

    # 使用unmix.py中的unmix_function函数解包.mix文件
    unmix.unmix_function()
    _delete_temp_files()
    
    
    # 解压与文件检查
    ready, atlas_name, img_name = _check_content_ready()    
    if ready:
        user_input = input(f"已找到当前目录下的atlas和图集,确定以下文件为输入?(只允许1个atlas和1个图集)\n"
                           f"atlas: {atlas_name}\n"
                           f"图集: {img_name}\n"
                           f"输入y以继续，输入n以退出\n")
        if user_input.lower() == 'y':
            # 使用atlas_function和resave_img_function转换atlas文件和图集
            atlas_base_name=atlas_function()
            resave_img_function(atlas_base_name)
            # 使用unpack.py拆分图集
            dir1 = os.getcwd()
            unpack.unpack(dir1)
            _delete_temp_files()
        if user_input.lower() == 'n':
            print("选择退出，程序将在2秒后退出")
            _delete_temp_files()
            time.sleep(2)
            exit(0)
    else:
        print("未找到需要的atlas和图集，程序将在3秒后退出")
        _delete_temp_files()
        time.sleep(3)
        exit(1)


       
    
