from django.shortcuts import render, get_object_or_404
from .models import Blog, Project



def home(request):
    project = Project.objects.all()
    return render(request,'index.html', {'projects': project})

def blog(request):
    blogs = Blog.objects.all()
    print(blogs)  
    return render(request, 'blog.html', {'blogs': blogs})

def blog_details(request, post_id):
    blog = get_object_or_404(Blog, id=post_id)
    return render(request, 'blog-details.html', {'blog': blog})

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blogs.html', {'blogs': blogs})