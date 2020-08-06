from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
# Create your views here.

# posts = [
#     {
#         'author': 'Corey MS',
#         'title':'Blog Post 1',
#         'content':'First Post content',
#         'date_posted':'August 27, 2018'
#     },
#      {
#         'author': 'Jane Doe',
#         'title':'Blog Post 2',
#         'content':'Second Post content',
#         'date_posted':'August 30, 2018'
#     }
# ]



def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request,'blog/home.html',context)

#Class Views
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'      #By Default the class view will look for this route => <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['date_posted']
    paginate_by = 2

#implementing pagination
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'      #By Default the class view will look for this route => <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['date_posted']
    paginate_by = 2
    #Changing the QuerySet from within this view by adding the get_query_set function
    def get_queryset(self):
        # get the user associated with the username we get from the URL
        #If the user doesn't exist then show a 404 error instead of a blank page
         user = get_object_or_404(User, username = self.kwargs.get('username'))
        #  Limit our results of this list view by finishing query
         return Post.objects.filter(author = user).order_by('-date_posted')


#Looking into the details of a single post so we need a Detail view
class PostDetailView(DetailView):
    model = Post


#This will be a form inside for creating a post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']
    #Override the form so that we can make the current user as our author of the new post we are creating
    def form_valid(self,form):
        #assigning the current user to be our author of created post
        form.instance.author = self.request.user 
        return super().form_valid(form)    #running our form_valid method on the parent class
    
#Update view
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']
    #Override the form so that we can make the current user as our author of the new post we are creating
    def form_valid(self,form):
        #assigning the current user to be our author of created post
        form.instance.author = self.request.user 
        return super().form_valid(form)    #running our form_valid method on the parent class
    #function which will prevent one user updating another users post
    def test_func(self):
        post = self.get_object()
        #Checking if the current user is the same as the author of the post
        if self.request.user == post.author:
            return True
        else:
            return False

#Delete View -> Requires a Form so we need a template here to be redirected to (blog/post_confirm_delete.html)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        #Checking if the current user is the same as the author of the post
        if self.request.user == post.author:
            return True
        else:
            return False


def about(request):
    return render(request,'blog/about.html',{'title':'About'})