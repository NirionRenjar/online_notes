from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def create_user(self, username, password):
        self.username = username
        self.set_password(password)
        self.save()

