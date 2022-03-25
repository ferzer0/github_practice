from email import contentmanager
from pdb import post_mortem
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.http import HttpResponse
from blogs.models import Blog, Blog_Comments
from .forms import BlogForm, CommentForm


class IndexView(TemplateView):
    template_name = "blogs/index.html"


    def get(self, request):
        context = Blog.objects.order_by('-date_added') 
        return render(request, self.template_name, {'blogsmain': context})
    

class DetailView(TemplateView):
    template_name = "blogs/details.html"

    def get(self, request, **kwargs):        
        context = {}
        #import pdb; pdb.set_trace() debugging
        context['blog'] = Blog.objects.get(pk=self.kwargs.get('pk'))
        return render(request, self.template_name, context)
            

class AddView(TemplateView):
    template_name = "blogs/add.html"

    def get(self, request):
        form = BlogForm()
        context = {'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):  
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()

        return redirect('blogs:index')
      
class CommentView(TemplateView):
    template_name = "blogs/details.html"
    slug_feild = "slug"
    count_hit = True

    def get(self, request):
        form = CommentForm()
        content = Blog_Comments.objects.order_by('-date_added')
        context = {'form': form,
                   'content':content,
                  }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = BlogForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.content = self.slug_feild
            comment.save()
        else:
            form = BlogForm()
        
        return redirect('blogs:detail')