from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    parent = models.ForeignKey('self', on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey('Post', on_delete= models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default= timezone.now)


    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


    def __str__(self):
        return self.user.username + self.text
    

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField('Содержание', null=True)
    file = models.FileField(upload_to="post_file/")
    date = models.DateTimeField('Дата создания поста', default=timezone.now)
    slug = models.SlugField('Ссылка', unique=True)
    code = models.CharField(max_length=10)
    published = models.BooleanField(default = True)
    featured = models.BooleanField(default = True)
    


    def get_link2(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})    


    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user_avatar/', null=True)
    birth_date = models.DateField(null=True)
    text = models.TextField(blank=True, null=True)
    phone = models.IntegerField('Номер', null=True, blank=True)


    def __str__(self):
        return self.user.username
    


    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'



class Chat(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE, null = True, blank = True)
    sender = models.ForeignKey(User, models.CASCADE, 'Отправитель')
    receiver = models.ForeignKey(User, models.CASCADE, 'Получатель')




class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now)




class Like(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null= True, blank=True)
    date = models.DateTimeField(default= timezone.now)



class Favourite(models.Model):
    post = models.ManyToManyField(Post)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Follow(models.Model):
    user1 = models.OneToOneField(User, on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user1')