import uuid
from django.db import models

# Create your models here.





class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, primary_key=False)
    email = models.CharField(max_length=100, primary_key=False)

    def __str__(self) -> str:
        return self.name


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, primary_key=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100, primary_key=False)

    def __str__(self) -> str:
        return self.phone_number