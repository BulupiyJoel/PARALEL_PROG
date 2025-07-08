from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from PIL import Image
import os
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def send_new_post_notification(self, post_title, post_author_email):
    """
    Envoie un email de notification à l'auteur lorsqu'un nouveau post est publié.
    """
    try:
        if not post_title or not post_author_email:
            raise ValueError("Le titre du post et l'email de l'auteur sont requis.")

        subject = f"Nouveau post publié : {post_title}"
        message = f"Bonjour,\n\nVotre article \"{post_title}\" a été publié avec succès !"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [post_author_email]

        send_mail(subject, message, from_email, recipient_list)
        logger.info(f"Notification envoyée à {post_author_email} pour le post '{post_title}'.")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email : {e}")
        self.retry(exc=e, countdown=10, max_retries=3)
        return False


@shared_task(bind=True)
def create_thumbnail(self, image_path, thumbnail_path, size=(200, 200)):
    """
    Crée une miniature d'une image à partir d'un chemin donné.
    """
    try:
        full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
        full_thumbnail_path = os.path.join(settings.MEDIA_ROOT, thumbnail_path)

        if not os.path.exists(full_image_path):
            raise FileNotFoundError(f"Image source non trouvée : {full_image_path}")

        with Image.open(full_image_path) as img:
            img.thumbnail(size)
            img.save(full_thumbnail_path)

        logger.info(f"Miniature créée : {full_thumbnail_path}")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la création de la miniature : {e}")
        self.retry(exc=e, countdown=5, max_retries=3)
        return False
