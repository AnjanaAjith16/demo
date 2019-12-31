from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Author(models.Model):
    author_id = models.IntegerField()
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Book(models.Model):
    book_id = models.IntegerField()
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.CharField(max_length=30)
    price = models.IntegerField()
    slug = models.SlugField(null=True, blank=True,unique=True)
    new = models.BooleanField(default=False)
    hot = models.BooleanField(default=False)
    book_img = models.ImageField(upload_to="coverpages/")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product", kwargs={'slug': self.slug})

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Book.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['title']


class Cart(models.Model):
    total = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, null = True, blank = True) # , null = True, blank = True
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return "Cart id : %s" % self.id


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,null=True,blank=True,on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    line_total = models.IntegerField(default=10)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.cart.id)


STATUS_CHOICES = (
    ("started", "started"),
    ("abandoned", "abandoned"),
    ("finished", "finished"),
)


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    sub_total = models.DecimalField(default=10.00, max_digits=1000, decimal_places=2)
    tax_total = models.DecimalField(default=10.00, max_digits=1000, decimal_places=2)
    final_total = models.DecimalField(default=10.00, max_digits=1000, decimal_places=2)
    order_id = models.CharField(max_length=120,default='ABC', unique=True)
    status = models.CharField(max_length=100, choices= STATUS_CHOICES,default="started")
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.order_id