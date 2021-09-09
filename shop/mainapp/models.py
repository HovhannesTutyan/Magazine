from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

User = get_user_model()

def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug':obj.slug})


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(self, *args, **kwargs):
        with_respect_to = kwargs.get('with_repect_to')
        products = []
        ct_models  = ContentType.objects.filter(model__in = args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
            )
        return products

class LatestProducts:
    objects = LatestProductsManager()

#*************
#1 Category
#2 Product
#3 CartProduct
#4 Cart
#5 Order
#*************
#6 Customer
#7 Specification

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Category name")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    class Meta:
        abstract=True

    category = models.ForeignKey(Category, verbose_name="Categories", on_delete=models.CASCADE)
    title=models.CharField(max_length=255, verbose_name='Products')
    slug=models.SlugField(unique=True)
    image = models.CharField(max_length=255)
    description = models.TextField(verbose_name='Description', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return self.title

class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name="Diagonal")
    display_type = models.CharField(max_length=255, verbose_name="Display type")
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    video = models.CharField(max_length=255, verbose_name='Видеокарта')
    time_without_charge = models.CharField(max_length=255, verbose_name='Время работы аккумулятора')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    accum_volume = models.CharField(max_length=255, verbose_name='Объем батареи')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    sd = models.BooleanField(default=True, verbose_name='Наличие SD карты')
    sd_volume_max = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Максимальный объем встраивамой памяти'
    )
    main_cam_mp = models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Customers', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='related_products')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price=models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total Price')

    def __str__(self):
        return "Product: {}".format(self.content_object.title)

class Cart(models.Model):
     owner = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
     products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
     total_products = models.PositiveIntegerField(default=0)
     final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total Price')

     def __str__(self):
         return str(self.id)

class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='User Name')
    phone = models.CharField(max_length=23, verbose_name='Phone Number')
    address = models.CharField(max_length=255, verbose_name='Adress')

    def __str__(self):
        return 'Buyer: {} {}'.format(self.user.first_name, self.user.last_name)
class Specification(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255, verbose_name="Products charachteristics")
    def __str__(self):
        return "Products chatachteristics: {}".format(self.name)

