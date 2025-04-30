from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post, Favorite, User, Rating
from .forms import PostForm, RatingForm

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
    # print(posts)
    context = {
        'posts': [post.title for post in posts]
    }
    
    return JsonResponse(context)


@login_required
def manage_posts(request):
    """Allows users to manage their own posts

    Args:
        request (HTTPRequest): Request sent in from the browser

    Returns:
        A template that displays the user's posts
    """

    # TODO: Implement the search into this page

    # Get the current user
    user = request.user

    # Get all posts created by the user
    posts = Post.objects.filter(author=user)
    
    # Get favorites
    favorites = Favorite.objects.filter(user=user)


    # Render the template with the user's posts
    context = {
        'user': user,
        'posts': posts,
        'favorites': favorites,
    }

    print(context)
    
    return HttpResponse(
        'hello world'
    )


@login_required
def create_post(request):
    """Create a new post
    
    Args:
        request (HTTPRequest): Request sent in from the browser
    
    Returns:
        A template that displays the form to create a new post
    
    """
    user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Save the post to the database
            post = form.save(commit=False)
            post.author = user
            post.save()
            return HttpResponse('Post created successfully')
        
    return HttpResponse('Create Post')

@login_required
def update_post(request, post_id: int):
    """Update an existing post
    
    Args:
        request (HTTPRequest): Request sent in from the browser
        post_id (int): The ID of the post to update
    
    Returns:
        A template that displays the form to update a post
    
    """

    # Get the post to update
    post = Post.objects.get(id=post_id)
    
    # Check if the user is the author of the post
    if request.user != post.author:
        return HttpResponse('You are not authorized to update this post')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # Save the updated post to the database
            form.save()
            return HttpResponse('Post updated successfully')
    
    return HttpResponse('Update Post')

@login_required
def delete_post(request, post_id: int):
    """Delete a post
    
    Args:
        request (HTTPRequest): Request sent in from the browser
        post_id (int): The ID of the post to be deleted
    
    Returns:
        An HTTP response indicating success or failure
    
    """

    # Get the post to delete
    post = Post.objects.get(id=post_id)
    
    # Check if the user is the author of the post
    if request.user != post.author:
        return HttpResponse('You are not authorized to delete this post')

    # Delete the post
    post.delete()
    
    return HttpResponse('Post deleted successfully')


def search_posts(request, search_query: str):
    """Search for posts based on a query
    
    Args:
        request (HTTPRequest): Request sent in from the browser
        serch_query (str): The query string to search for
    
    Returns:
        A template that displays the search results
    
    """

    # TODO: make this a lot more advanced obviously
    # Get all posts that match the search query
    posts = Post.objects.filter(title__icontains=search_query)

    # Render the template with the search results
    context = {
        'posts': posts,
        'search_query': search_query,
    }

    return HttpResponse('Search Posts')


def view_post(request, post_id: int):
    """
    View a single post

    Args:
        request (HTTPRequest): Request sent in from the browser
        post_id (int): The ID of the post to view
    """

    # Get the post to view
    post = Post.objects.get(id=post_id)

    # Check if the post exists
    if not post:
        return HttpResponse('Post not found')

    # Render the template with the post details
    context = {
        'post': post,
    }

    return HttpResponse('View Post')

@login_required
def rate_post(request, post_id: int):
    """Endpoint to send a rating for a post

    Args:
        request (HTTPRequest): Request sent in from the browser
        post_id (int): The ID of the post to rate
    """

    user = request.user
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating_data = form.cleaned_data['rating']
            post = Post.objects.get(id=post_id)
            user = request.user
            # checking if the rating already exists
            if Rating.objects.get(post=post, user=user):
                # Update the existing rating
                rating = Rating.objects.get(post=post, user=user)
                rating.rating = rating_data
                rating.save()
            else:
                rating = Rating(post, user, rating_data)
                rating.save()
            
            return HttpResponse('Rating saved successfully')
        
    return HttpResponse('Rate Post')


@login_required
def manage_favorite(request, post_id):
    """Endpoint to add or remove a post from favorites

    Args:
        request (HTTPRequest): Request sent in from the browser
        post_id (int): ID of the post to add or remove from favorites
    """

    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        user = request.user
        # checking if the favorite already exists
        if Favorite.objects.get(post=post, user=user):
            # Remove the favorite
            favorite = Favorite.objects.get(post=post, user=user)
            favorite.delete()
            return HttpResponse('Favorite removed successfully')
        else:
            # Add to favorites
            favorite = Favorite(post, user)
            favorite.save()
            return HttpResponse('Favorite added successfully')
