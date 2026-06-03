import os
import shutil
import django
import subprocess

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.test import Client
from django.conf import settings
from app.models import Blog

def build():
    client = Client()
    output_dir = os.path.join(settings.BASE_DIR, 'docs')

    # Clean previous build
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    def save_page(url, relative_path):
        print(f"Exporting {url} -> {relative_path}")
        response = client.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url} (status {response.status_code})")
            return
        
        # Ensure directories exist
        path = os.path.join(output_dir, relative_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'wb') as f:
            f.write(response.content)

    # 1. Save static pages
    save_page('/', 'index.html')
    save_page('/blog/', 'blog/index.html')

    # 2. Save dynamic blog details pages
    for blog in Blog.objects.all():
        save_page(f'/blogdetails/{blog.id}/', f'blogdetails/{blog.id}/index.html')

    # 3. Collect static files
    print("Collecting static files...")
    # Make sure we're in the project directory when running collectstatic
    project_dir = settings.BASE_DIR
    subprocess.run(['python', 'manage.py', 'collectstatic', '--noinput'], cwd=project_dir)
    
    # Copy static files to docs/static
    if os.path.exists(settings.STATIC_ROOT):
        static_dest = os.path.join(output_dir, 'static')
        if not os.path.exists(static_dest):
            shutil.copytree(settings.STATIC_ROOT, static_dest)
            print("Copied static files.")

    # Copy media files to docs/media
    if os.path.exists(settings.MEDIA_ROOT):
        media_dest = os.path.join(output_dir, 'media')
        if not os.path.exists(media_dest):
            shutil.copytree(settings.MEDIA_ROOT, media_dest)
            print("Copied media files.")

    # Add a .nojekyll file to prevent GitHub pages from ignoring folders starting with underscore
    with open(os.path.join(output_dir, '.nojekyll'), 'w') as f:
        pass
    
    print(f"Successfully built static site in {output_dir}")

if __name__ == '__main__':
    build()
