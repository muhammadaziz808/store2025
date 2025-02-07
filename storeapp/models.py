from django.db import models
from django.contrib.auth.models import User

class Userprofile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users/',blank=True,null=True)
    first_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    def __str__(self):
        return self.username

class CategoryModel(models.Model):
    name = models.CharField(max_length=200 , verbose_name='kategoriya nomi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'kotegoriya'
        verbose_name_plural = 'kotegoriyalar'


class TovarModel(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    about = models.TextField(max_length=200)
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE,verbose_name='kategoriya')

    def __str__(self):
        return self.name

class BasketModl(models.Model):
    product = models.ForeignKey(TovarModel, on_delete=models.PROTECT)
    owner = models.ForeignKey(Userprofile, on_delete=models.PROTECT)
    ordered = models.BooleanField(default=False)
    count = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    def basket_price(self):
        return self.product.price * self.count


class OrderModel(models.Model):
    STATUS_CHANGE = (
        ('Yetkazilmoqda','Yetkazilmoqda'),
        ('Yetkazildi','Yetkazildi'),
        ("To'landi","To'landi")
    )
    basket = models.ManyToManyField(BasketModl)
    owner = models.ForeignKey(Userprofile, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, choices=STATUS_CHANGE, blank=True, null=True)
    summa = models.IntegerField(blank=True, null=True)

    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.owner.username
