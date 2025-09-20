from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)  
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=50)
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    def increment_views(self):
        """Tambah 1 ke jumlah views produk"""
        self.views += 1
        self.save(update_fields=["views"])

    def __str__(self):
        return self.name