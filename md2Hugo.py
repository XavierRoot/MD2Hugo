import os  
import re  
import sys  
import time  
  
#Hugo_Server_Post = '/Hugo-Blog/content/posts/'
Hugo_Server_Post = 'output/'  # Change Hre


def TorF(input):
    if 'no'==input.lower() or 'n'== input.lower():
        return 'false'
    else:
        return 'true'


def gen_metadata(input_file):
    #input_file = './input/test1.md'  # 请替换为你的文件路径  
    file_mtime = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.path.getmtime(input_file)))
    title = input("  请输入标题: ")  
    author = input("  请输入作者: ")  
    description = input("  请输入描述: ")  
    draft = TorF(input("  是否是草稿, y(yes)/n(no): "))
    
    categories = '- draft\n' if 'true'== draft else ''
    cate_tmp = input("  请输入文章分类，逗号分割：")
    cate_tmp = re.sub(r'[，,]', '\n- ', cate_tmp.strip()) 
    categories = categories if ''==cate_tmp else categories+'- '+cate_tmp
    #print(categories)

    tags = '- draft\n' if 'true'== draft else ''
    tag_tmp = input("  请输入文章tag，逗号分割：")
    tag_tmp = re.sub(r'[，,]', '\n- ', tag_tmp.strip()) 
    tags = tags if ''==tag_tmp else tags+'- '+tag_tmp
    #print(tags)

    
    metadata = f'---\n' \
           f'title: "{title}"\n' \
           f'subtitle: ""\n' \
           f'date: {file_mtime}\n' \
           f'draft: {draft}\n' \
           f'author: "{author}"\n' \
           f'authorLink: ""\n' \
           f'authorEmail: ""\n' \
           f'description: "{description}"\n' \
           f'keywords: ""\n' \
           f'license: ""\n' \
           f'comment: false\n' \
           f'weight: 0\n\n' \
           f'tags:\n' \
           f'{tags}\n' \
           f'categories:\n' \
           f'{categories}\n\n' \
           f'hiddenFromHomePage: false\n' \
           f'hiddenFromSearch: false\n' \
           f'summary: ""\n' \
           f'resources:\n' \
           f'- name: featured-image\n' \
           f'  src: featured-image.jpg\n' \
           f'- name: featured-image-preview\n' \
           f'  src: featured-image-preview.jpg\n\n' \
           f'toc:\n' \
           f'  enable: true\n' \
           f'math:\n' \
           f'  enable: false\n' \
           f'lightgallery: false\n' \
           f'seo:\n' \
           f'  images: []\n' \
           f'repost:\n\n' \
           f'  enable: false\n' \
           f'  url: ""\n' \
           f'---\n\n'  
    
    #print(metadata)
    return metadata

# 弃用
def replaceImg(content):
    print('替换图片链接ing\n')
    pattern = r'!\[(.*?)\]\((.*?)\)'  
    replacement = r'![\1](/\2)'  
    content = re.sub(pattern, replacement, content)
    return content

def convert_markdown_to_hugo(input_file, output_file):  
    with open(input_file, 'r', encoding='utf-8') as f:  
        content = f.read()  
      
    # 手动添加 YAML 元数据  
    print('\n[~] 生成YAML元数据：')
    metadata = gen_metadata(input_file)
    #metadata = ''
      
    # 将纯文本和元数据写入输出文件  
    with open(output_file, 'w', encoding='utf-8') as f:  
        f.write(metadata)  
        f.write(content)  
  
if __name__ == '__main__':  
    print("[~] Hugo Server Path: " + Hugo_Server_Post)

    if len(sys.argv) != 3:  
        print("Usage: python convert_markdown.py <input_file.md> <output_file.md>")  
        sys.exit(1)  
    
    input_file = sys.argv[1]  
    output_file = Hugo_Server_Post + sys.argv[2]  

    #print(output_file)
    # 这部分有问题，但是实际遇到的情况比较少，所以懒得改了
    if os.path.exists(output_file):
        if 'y' == input('[!] 文件已存在，是否覆盖？(y/n) '):
            print('    覆盖中……')
            os.rmdir(output_file)
            os.makedirs(output_file)
        else:
            sys.exit(1)
    else:
        os.makedirs(output_file)

    output_file = output_file+'/index.md'
  
    if not os.path.exists(input_file):  
        print(f"Error: Input file {input_file} does not exist.")  
        sys.exit(1)  
  
    if not input_file.endswith('.md'):  
        print(f"Warning: Input file {input_file} does not have a .md extension. Proceeding anyway.")  
  
    try:  
        convert_markdown_to_hugo(input_file, output_file)  
        print(f"Success: Converted {input_file} to Hugo format and saved as: \n\t{output_file}")  
    except KeyboardInterrupt:
        print("\n用户中断了程序运行.\n")
    except Exception as e:  
        print(f"Error: An error occurred while converting the file: {e}")