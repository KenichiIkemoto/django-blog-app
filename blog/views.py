from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404
from django.db.models import Count,Q
from django.urls import reverse_lazy,reverse

from django.views.generic import ListView,DetailView,CreateView,DeleteView
from blog.models import Post,Category,Tag,Comment,Reply
from blog.form import CommentForm,ReplyForm

class PostListView(ListView):
    model=Post
    template_name="blog/post_list.html"
    paginate_by=3

    def get_queryset(self):
 
        posts=super().get_queryset()
        return posts.order_by("-updated_at")



class PostDetailView(DetailView):
    
    model=Post
    template_name="blog/post_detail.html"
    paginate_by=3

    def get_object(self, queryset=None):
        print("★"*30)
        print(vars(self))
        print("★"*30)
        post=super().get_object(queryset)
        

        if post.is_published or self.request.user.is_authenticated:
  
            return post
        else:
            return Http404

class CategoryPostListView(ListView):
    model=Post
    template_name="blog/post_list.html"
    paginate_by=3

    def get_queryset(self) :
        print("★"*30)
        print(vars(self))
        print("★"*30)
        slug=self.kwargs["slug"]

        self.category=get_object_or_404(Category,slug=slug)

        return super().get_queryset().filter(category=self.category)
    
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        print("="*30)
        print(context)
        print("="*30)
        context["category"]=self.category
        return context
    
class TagPostListView(ListView):
    model=Post
    template_name="blog/post_list.html"
    paginate_by=3

    def get_queryset(self):

        slug = self.kwargs["slug"]
        self.tag = get_object_or_404(Tag,slug=slug)
        print("=tag"*30)
        print(vars(self.tag))
        print("="*30)
        return super().get_queryset().filter(tags=self.tag)
 
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        print("="*30)
        print(context)
        print("="*30)
        context["tag"]=self.tag
        return context
    
class SearchPostListView(ListView):
    model=Post
    template_name="blog/post_list.html"
    paginate_by=4

    def get_queryset(self):        
        self.query=self.request.GET.get('query') or ""

        queryset=super().get_queryset()
        if self.query:
            queryset=queryset.filter(
                Q(title__icontains=self.query) | Q(content__icontains=self.query)
            )
        if not self.request.user.is_authenticated:
            queryset=queryset.filter(is_published=True)
        print("="*40)
        print(queryset)
        print("="*40)  

        self.post_count=len(queryset)
          
        return queryset
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        print("="*30)
        print(context)
        print("="*30)
        context["query"]=self.query
        context["post_count"] =self.post_count
        return context


class CommentCreateView(CreateView):
    model=Comment
    form_class=CommentForm
    #template_name="blog/comment_form.html"

    def form_valid(self,form):
        print("=Comment="*5)
        print(vars(form))
        comment=form.save(commit=False)
        print("=Comment="*5)
        print(vars(comment))
        post_pk=self.kwargs["post_pk"]
        post=get_object_or_404(Post,pk=post_pk)
        comment.post=post
        comment.save()
        return redirect("post-detail",pk=post_pk)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        post_pk=self.kwargs['post_pk']
        context["post"] = get_object_or_404(Post,pk=post_pk)
        return context

class ReplyCreateView(CreateView):
    model=Reply
    form_class=ReplyForm
    template_name="blog/comment_form.html"

    def form_valid(self,form):
        print("="*30)
        print(vars(form))

        reply=form.save(commit=False)
        print("="*30)
        print(reply)
        comment_pk=self.kwargs["comment_pk"]
        comment=get_object_or_404(Comment,pk=comment_pk)
        reply.comment=comment
        reply.save()
        return redirect("post-detail",pk=comment.post.pk)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        comment_pk=self.kwargs['comment_pk']
        context["comment"] = get_object_or_404(Comment,pk=comment_pk)
        return context

class CommentDeleteView(DeleteView):
    model=Comment
    #success_url=reverse_lazy("post-list")
    template_name="blog/comment_delete.html"

    def get_success_url(self):
        print("=1"*30)
        print(vars(self))
        return reverse("post-detail",kwargs={"pk":self.object.post.pk})
    
class ReplyDeleteView(DeleteView):
    model=Reply
    #success_url=reverse_lazy("post-list")
    template_name="blog/comment_delete.html"
    def get_success_url(self):
        print("=2"*30)
        print(vars(self))
        return reverse("post-detail",kwargs={"pk":self.object.comment.post.pk})
