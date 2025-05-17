from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Favorite, User, Rating, Category
from .forms import PostForm, RatingForm
from .utils import get_keyboard_adjacency, search
import markdown


# Create your views here.

def index(request):
    return render(request, 'index.html')


def view_posts(request):
    """View all posts

    Args:
        request (HTTPRequest): Request sent in from the browser

    Returns:
        A template that displays all posts
    """

    posts = Post.objects.all()
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).all()
        my_posts = Post.objects.filter(creator=request.user).all()

    else:
        favorites = []
        my_posts = []

    categories = Category.objects.all()

    context = {
        'posts': posts,
        'favorites': favorites,
        'my_posts': my_posts,
        'categories': categories,

    }
    
    return render(request, 'posts/posts.html', context)



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
        content_file = request.FILES.get('content-file')
        if content_file:
            # manually overriding content with the content from the file
            file_content = content_file.read().decode('utf-8')
            post_data = request.POST.copy()
            post_data['content'] = file_content
            form = PostForm(post_data)
        
        else:
            form = PostForm(request.POST)

        if form.is_valid():
            # Save the post to the database
            post = form.save(commit=False)
            post.creator = user
            post.save()
            form.save_m2m()
            return redirect('view_posts')
        
    return render(request, 'posts/create_post.html', {'form': PostForm()})

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
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return redirect('view_posts')
    
    # Check if the user is the author of the post
    if request.user != post.creator:
        return HttpResponse('You are not authorized to update this post')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # Save the updated post to the database
            form.save()
            return redirect('view_posts')

    context = {
        'form': PostForm(instance=post),
        'post': post,
    }

    return render(request, 'posts/update_post.html', context)

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
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return redirect('view_posts')
    
    # Check if the user is the author of the post
    if request.user != post.creator:
        return redirect('view_posts')

    # Delete the post
    post.delete()
    
    return redirect('view_posts')


def search_posts(request):
    """Search for posts based on a query
    
    Args:
        request (HTTPRequest): Request sent in from the browser
        serch_query (str): The query string to search for
    
    Returns:
        A template that displays the search results
    
    """

    # Get the search query from the request
    search_query = request.POST.get('search-query').lower().strip()
    categories = request.POST.getlist('category-filters')
    # posts = Post.objects.filter(title__icontains=search_query)
    posts = search(search_query.replace(' ', '-'), categories)

    # Get all posts that match the search query
    # posts = Post.objects.exclude(creator=request.user)


    # Render the template with the search results
    context = {
        'posts': posts,
        'search_query': search_query,
    }

    return render(request, 'posts/search.html', context)


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
        return redirect('view_posts')
    
    amount_of_ratings = Rating.objects.filter(post=post).count()
    try:
        is_favorite = Favorite.objects.get(post=post, user=request.user) if request.user.is_authenticated else False
    except Favorite.DoesNotExist:
        is_favorite = False

    md = markdown.Markdown(extensions=['fenced_code'])
    content = md.convert(post.content)

    # Render the template with the post details
    context = {
        'post': post,
        'content': content,
        'amount_of_ratings': amount_of_ratings,
        'is_favorite': is_favorite,
    }

    return render(request, 'posts/view_post.html', context)

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
@csrf_exempt
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
        try:
            # Remove the favorite
            favorite = Favorite.objects.get(post=post, user=user)
            favorite.delete()
            return HttpResponse('Favorite removed successfully')
        except Favorite.DoesNotExist:
            # Add to favorites
            favorite = Favorite(post=post, user=user)
            favorite.save()
            return HttpResponse('Favorite added successfully')
