from django.shortcuts import render
from .models import Post, Profile, Comment, Message, User, Follow, Favourite
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, ProfileForm
from django.db.models import Q
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from .translit import translit_slug

# Create your views here.
def index(request):
    posts = Post.objects.filter(published = True).order_by('-date')
    featureds = Post.objects.filter(featured = True).order_by('-date')[:4]
    context = {'posts': posts, 'featureds': featureds,}
    return render(request, 'index.html', context)

def login_site(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)    
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            message = 'Долбаеб пиши правильно'
            return render(request, 'login.html', {'message': message})
    return render(request, 'login.html')    



def logout_site(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')



def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                profile = Profile()
                profile.user = user
                profile.save()
                login(request, user)
                return redirect('index')
        else:
            form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    return redirect('index.html')    


def comment(request,slug):
    post = Post.objects.get(slug__exact=slug)
    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.post = post
        comment.text = request.POST.get('text')
        if not comment.text:
             return redirect(reverse('post_detail_url', kwargs={'slug': slug}))
        comment.save()
        return redirect(reverse('post_detail_url', kwargs ={'slug': slug}))
    return redirect(reverse('post_detail_url', kwargs ={'slug': post.slug}))

def reply_to_comment(request, comment_id):
    parent_comment = Comment.objects.get(pk=comment_id)
    if request.method == 'POST':
        # Получаем текст ответа из POST-запроса
        reply_text = request.POST.get('reply_text', '')
        # Создаем новый комментарий с текстом ответа и родительским комментарием
        new_comment = Comment.objects.create(
            user=request.user,
            post=parent_comment.post,  # Предполагается, что комментарий относится к тому же посту
            parent=parent_comment,
            content=reply_text
        )
        return redirect('post_detail', post_id=parent_comment.post.id)  # Перенаправляем пользователя на страницу с постом
    else:
        return render(request, 'reply_to_comment.html', {'parent_comment': parent_comment})
# Пример использования в urls.py:
# path('reply_to_comment/<int:comment_id>/', reply_to_comment, name='reply_to_comment')
    
def posts(request):
    posts = Post.objects.filter(published = True).order_by('-date')
    context = {'posts': posts,}
    return render(request, 'posts.html', context)

def post_detail(request, slug):
    post = Post.objects.get(slug__exact=slug)
    if request.user.is_authenticated:
        if not post.view_set.filter(user = request.user).exists():
            post.view_set.create(user = request.user)
        else:
            view = request.user.view_set.get(post=post)
            view.date = timezone.now()
            view.save()    
    return render(request, 'post_detail.html', {'post': post})

def create_post(request):
    if request.method == 'POST':
        post = Post()
        post.user = request.user
        post.code = translit_slug()
        if request.FILES.get('file', False) != False:
            myfile = request.FILES['file']
            fsi = FileSystemStorage()
            filenameimage = fsi.save(myfile.name, myfile)
            post.file = filenameimage
        post.text = request.POST.get('text')
        post.save()
        return redirect('index')
    return render(request, 'create_post.html')

def edit_post(request, slug):
    post = Post.objects.get(slug__exact=slug)
    if request.method == 'POST':
        post.user = request.user
        post.slug = translit_slug()
        if request.FILES.get('file', False) != False:
            myfile = request.FILES['file']
            fsi = FileSystemStorage()
            filename = fsi.save(myfile.name, myfile)
            post.file = filename
        if request.FILES.get('file', False) != False:
            myfile = request.FILES['file']
            fsv = FileSystemStorage()
            filename = fsv.save(myfile.name, myfile)
            post.video = filename
        post.text = request.POST.get('text')
        post.save()
        return redirect('index')
    return render(request, 'edit_post.html', {'post':post})

def post_delete(slug):
    post = Post.objects.get(slug__exact=slug)
    post.delete()
    return redirect('index')



def profile(request):
    profile = Profile.objects.get(user_id__exact = request.user.id)
    return render(request, 'profile.html' , {'profile': profile})

def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect()
    else:
        form = ProfileForm()
    return render(request, 'create_profile.html', {'form': form})

def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, usr = request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(usr = request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})

def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('index') 



def search(request):
    query = request.GET.get('search')
    posts = Post.objects.filter(Q(title__iregex = query))
    content = {'posts': posts, "query":query}
    return render(request, 'search.html', content)




def like(request, slug):
    post = Post.objects.get(slug__exact = slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if not post.like_set.filter(user=request.user).exists():
                post.like_set.create(user = request.user)
            else:
               like = request.user.like_set.get(post=post)
               like.delete()
        else:
            return redirect('login')
    return redirect(reverse('post_detail_url', kwargs={'slug':slug}))



def send_message(request, sender_id, receiver_id):
    if request.method == 'POST':
        sender = User.objects.get(pk=sender_id)
        receiver = User.objects.get(pk=receiver_id)
        message_content = request.POST.get('message', '')
        
        # Создание нового сообщения
        message = Message.objects.create(sender=sender, receiver=receiver, content=message_content)


def message(request, sender_id, receiver_id):
    if request.method == 'POST':
        sender = User.objects.get(pk=sender_id)
        receiver = User.objects.get(pk=receiver_id)
        message_content = request.POST['message']
        
        # Создание нового сообщения
        message = Message.objects.create(sender=sender, receiver=receiver, content=message_content)


def follow(request, follower_id, following_id):
    if request.method == 'POST':
        follower = User.objects.get(pk=follower_id)
        following = User.objects.get(pk=following_id)
        
        # Проверяем, не подписан ли уже пользователь
        if Follow.objects.filter(follower=follower, following=following).exists():
            return redirect('')
        
        # Создаем запись о подписке
        follow_instance = Follow.objects.create(follower=follower, following=following)


def cancel_follow(request, follow_id):
    # Получаем объект подписки, который пользователь хочет отменить
    follow_instance = Follow.objects.get(pk=follow_id)

    # Проверяем, принадлежит ли подписка текущему пользователю
    if follow_instance.follower == request.user:
        # Удаляем подписку
        follow_instance.delete()

    return redirect('profile')



def favourite(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(pk=user_id)
        item = request.POST.get('item', '')
        # Проверяем, не добавлен ли уже элемент в избранное
        if Favourite.objects.filter(user=user, item=item).exists():
            return redirect()
        # Создаем запись об избранном
        favourite_instance = Favourite.objects.create(user=user, item=item)

def delete_favourite(request, favourite_id):
    # Получаем объект избранного, который пользователь хочет удалить
    favourite_item = Favourite.objects.get(pk=favourite_id)

    # Проверяем, принадлежит ли элемент текущему пользователю
    if favourite_item.user == request.user:
        # Удаляем элемент из избранного
        favourite_item.delete()

    return redirect('favourites')