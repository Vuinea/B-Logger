from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post, User

# Create your views here.

def index(request):
    return HttpResponse('hello world')


def view_posts(request):
    """View all posts

    Args:
        request (HTTPRequest): Request sent in from the browser

    Returns:
        A template that displays all posts
    """

    posts = Post.objects.all()
    print(posts)
    context = {
        'posts': posts
    }
    
    return HttpResponse('View Posts')


@login_required
def manage_posts(request):
    """Allows users to manage their own posts

    Args:
        request (HTTPRequest): Request sent in from the browser

    Returns:
        A template that displays the user's posts
    """


@login_required
def create_post(request):
    """Create a new post
    
    Args:
        request (HTTPRequest): Request sent in from the browser
    
    Returns:
        A template that displays the form to create a new post
    
    """

@login_required
def update_post(request, post_id: int):
    """Update an existing post
    
    Args:
        request (HTTPRequest): Request sent in from the browser
        post_id (int): The ID of the post to update
    
    Returns:
        A template that displays the form to update a post
    
    """

@login_required
def delete_post(request, post_id: int):
    """Delete a post
    
    Args:
        request (HTTPRequest): Request sent in from the browser
        post_id (int): The ID of the post to be deleted
    
    Returns:
        An HTTP response indicating success or failure
    
    """


def search_posts(request, search_query: str):
    """Search for posts based on a query
    
    Args:
        request (HTTPRequest): Request sent in from the browser
        serch_query (str): The query string to search for
    
    Returns:
        A template that displays the search results
    
    """


def view_post(request, post_id: int):
    """
    View a single post

    Args:
        request (HTTPRequest): Request sent in from the browser
        post_id (int): The ID of the post to view
    """


@login_required
def rate_post(request, post_id: int):
    """Endpoint to send a rating for a post

    Args:
        request (HTTPRequest): Request sent in from the browser
        post_id (int): The ID of the post to rate
    """


@login_required
def manage_favorite(request, post_id):
    """Endpoint to add or remove a post from favorites

    Args:
        request (HTTPRequest): Request sent in from the browser
        post_id (int): ID of the post to add or remove from favorites
    """
