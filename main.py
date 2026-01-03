import re
import os
import glob
import yaml

def define_env(env):
    
    # List projects where the metadata pin is true
    
    @env.macro
    def list_pinned_projects():
        print("[list_pinned_projects] Searching for pinned projects")
        pinned_projects = []
        
        # Each project is stored in a category folder (hardware/hobbies/software) so use **
        valid_filepaths = glob.glob(os.path.join("docs", "projects", "**", "*.md"))
        
        for filepath in valid_filepaths:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # YAML
            if content.startswith('---'):
                
                _, front_matter, markdown_body = content.split('---', 2)
                data:dict = yaml.safe_load(front_matter)
                
                # Check if pin is set to True
                if data.get('pin') is True:
                    title = os.path.basename(filepath)[:-3]
                    
                    # URL is based on filepath without the .md ends with "/"
                    # Remove docs and projects
                    split_path = filepath.split(os.sep)
                    path_without_docs = "/".join(split_path[2:]) 
                    url = path_without_docs[:-3]
                    
                    tags = data.get('tags', [])
                    if isinstance(tags, str):
                        tags = [tags] # Handle case where user puts a single string

                    description = data.get('description', '')

                    # Store data for the card
                    pinned_projects.append({
                        'title': title,
                        'description': description,
                        'tags': tags,
                        'url': url,
                    })

        for proj in pinned_projects:
            print(f"[list_pinned_projects] Pinning {proj}")
        
        return pinned_projects