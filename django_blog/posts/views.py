from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm,PostForm
from .models import Post,Comment
from .forms import CommentForm


## Post views
# Liste des articles publiés
def post_list(request):
    posts = Post.objects.filter(status='published').order_by('-pub_date')
    return render(request, 'posts/post_list.html', {'posts': posts})

# Détail d’un article
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    return render(request, 'posts/post_detail.html', {'post': post})

# Création d’un article (connexion requise)
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Article créé avec succès.')
            return redirect('posts:post_detail', slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'posts/post_form.html', {'form': form})
## End

## Comment views
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comment_form = CommentForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('posts:login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('posts:post_detail', slug=post.slug)

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comment_form': comment_form,
    })
## End

### Authentification
# Inscription utilisateur
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique après inscription
            messages.success(request, f'Bienvenue {user.username} ! Votre compte a été créé.')
            return redirect('posts:post_list')
    else:
        form = UserRegisterForm()
    return render(request, 'posts/auth/register.html', {'form': form})

# Connexion utilisateur
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Connecté en tant que {user.username}.')
            return redirect('posts:post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'posts/auth/login.html', {'form': form})

# Déconnexion utilisateur
def logout_view(request):
    logout(request)
    messages.info(request, "Vous êtes déconnecté.")
    return redirect('posts:login')
