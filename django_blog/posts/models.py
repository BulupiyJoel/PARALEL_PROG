from django.db import models
from django.conf import settings
from .tasks import send_new_post_notification, create_thumbnail
import os

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
        ('archived', 'Archivé'),
    )

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0)
    thumbnail = models.ImageField(upload_to='posts/thumbnails/', blank=True, null=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        image_changed = False
        if self.pk:
            old = type(self).objects.filter(pk=self.pk).first()
            if old and old.image != self.image:
                image_changed = True
        else:
            image_changed = bool(self.image)
        super().save(*args, **kwargs)
        # Envoi d'email lors de la création d'un nouveau post publié
        if is_new and self.status == 'published':
            if self.author_id:
                author_obj = self.author
                if hasattr(author_obj, 'email'):
                    send_new_post_notification.delay(self.title, author_obj.email)
        # Création de la miniature lors de l'upload d'une image
        if self.image and (is_new or image_changed):
            image_name = self.image.name if self.image and hasattr(self.image, 'name') else None
            if image_name:
                thumb_name = f"posts/thumbnails/thumb_{os.path.basename(image_name)}"
                create_thumbnail.delay(image_name, thumb_name)
                self.thumbnail = thumb_name
                super().save(update_fields=['thumbnail'])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Commentaire de {self.author} sur {self.post}"
