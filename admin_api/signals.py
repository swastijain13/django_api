from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

@receiver(post_migrate)
def set_is_admin_for_superuser(sender, **kwargs):
    User = get_user_model()

    admin_user = User.objects.filter(username = 'admin').first()
    if admin_user and not admin_user.is_admin:
        admin_user.is_admin = True  # Set the is_admin field to True
        admin_user.save()
        print("Admin user created!")
    else :
        print("No admin user found or there is already an admin!!")