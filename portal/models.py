from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

from .manager import UserManager


# Create your models here.
class Academia(models.Model):
    degree = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name}"


class Interest(models.Model):
    interest = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.interest}"


class Skill(models.Model):
    skill = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.skill}"


class User(AbstractUser):
    image = CloudinaryField(blank=True, null=True)
    username = models.CharField(("username"), max_length=30, blank=True, unique=True)
    email = models.EmailField("Email", blank=False, null=False, unique=True)
    first_name = models.CharField(("first name"), max_length=30, blank=False)
    last_name = models.CharField(("last name"), max_length=30, blank=False)
    password = models.CharField(("Password"), max_length=30)
    confirm_password = models.CharField(
        ("confirm_password"), max_length=30, blank=True, null=True
    )

    academia = models.ManyToManyField(
        Academia,
        blank=True,
    )
    skills = models.ManyToManyField(Skill)
    interests = models.ManyToManyField(Interest, blank=True)

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "email",
        "password",
        "confirm_password",
    ]
    objects = UserManager()


class Post(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    body = models.TextField(blank=True, null=True)
    commentCount = models.IntegerField(default=0, null=True, blank=True)
    postedOn = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-postedOn"]

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    content = models.TextField()
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    postedOn = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ["-postedOn"]

    def __str__(self):
        return f"{self.content}"


class Product(models.Model):
    name = models.CharField(max_length=75)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    condition = models.CharField(max_length=10)
    category = models.CharField(max_length=20, null=True, blank=True)
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="seller",
    )
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="buyer", null=True, blank=True
    )
    postedOn = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-postedOn"]


class Service(models.Model):
    title = models.CharField(max_length=75)
    description = models.TextField()
    price = models.CharField(max_length=15)
    provider = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="provider"
    )
    skills = models.ManyToManyField(Skill)
    postedOn = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-postedOn"]


class Image(models.Model):
    image = CloudinaryField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product", blank=True, null=True
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="service", blank=True, null=True
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post", blank=True, null=True
    )


class File(models.Model):
    file = models.FileField(upload_to="files/")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_file", blank=True, null=True
    )
