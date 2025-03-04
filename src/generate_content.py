import os, shutil
from block_markdown import markdown_to_html_node, markdown_to_blocks, get_header_tag
BASEPATH = "src/main.py"

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if get_header_tag(block) == (1, "h1"):
            header = block.lstrip("#").strip()
            return header
        else:
            raise Exception("h1 level header is not found")

def generate_page(from_path, template_path, dest_path):
    # Don't modify the input parameters or iterate through directories
    # This function should handle a single file
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown content
    with open(from_path, "r") as markdown_file:
        markdown_content = markdown_file.read()
    
    # Read the template
    with open(template_path, "r") as template_file:
        template_html = template_file.read()
    
    # Convert markdown to HTML
    content_node = markdown_to_html_node(markdown_content)
    content_html = content_node.to_html()
    
    # Get the title
    title = extract_title(markdown_content)

    # Replace placeholders in template
    new_template_html = template_html.replace("{{ Title }}", title)
    new_template_html = new_template_html.replace("{{ Content }}", content_html)
    new_template_html = new_template_html.replace('href="/', f'href="{BASEPATH}')
    new_template_html = new_template_html.replace('src="/', f'src="{BASEPATH}')

    # Ensure the directory exists before writing the file
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the generated HTML
    with open(dest_path, "w") as dest_file:
        dest_file.write(new_template_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir_path, exist_ok=True)

    # List all content
    source_dir_content = os.listdir(dir_path_content) 
     
    for content in source_dir_content:
        from_path = os.path.join(dir_path_content, content)
        dest_path = os.path.join(dest_dir_path, content)

        if os.path.isdir(from_path):
            # Recursively process subdirectories
            generate_pages_recursive(from_path, template_path, dest_path)
            
        elif content.endswith(".md"):  
            # Convert .md files to .html using the template
            html_dest_path = dest_path.replace(".md", ".html")
            
            # Use generate_page function to handle the conversion
            generate_page(from_path, template_path, html_dest_path)
            print(f" * {from_path} -> {html_dest_path}")       
        else:
            # Copy other files directly
            shutil.copy(from_path, dest_path)
            print(f" * {from_path} -> {dest_path}")     
