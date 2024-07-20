import uuid
from django.db import models

# Create your models here.


class User(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, blank=False, null=False
    )
    name = models.CharField(max_length=100, primary_key=False, blank=False, null=False)
    email = models.CharField(max_length=100, primary_key=False)
    phone_number = models.CharField(max_length=22, primary_key=False)
    password = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self) -> str:
        return self.name


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, primary_key=False, blank=False, null=False)
    is_spam = models.BooleanField(primary_key=False, default=False)
    phone_number = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self) -> str:
        return self.phone_number


class UserContact(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    contact_id = models.ForeignKey(
        Contact, on_delete=models.CASCADE, blank=False, null=False
    )
