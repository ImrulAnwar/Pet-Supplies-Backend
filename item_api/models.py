from django.db import models
from django.utils.text import slugify


class Item(models.Model):
    title = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=20, choices=(
        ('Cat', 'Cat'), ('Dog', 'Dog'), ('Bird', 'Bird')))
    accessory_type = models.CharField(max_length=100, choices=(
        ('Accessories', 'Accessories'),
        ('Health & Care', 'Health & Care'),
        ('Food', 'Food'),
        ('Litter', 'Litter'),
        ('Beds & Carrier', 'Beds & Carrier'))
    )
    brand = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    short_description = models.TextField()
    long_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    product_image = models.ImageField(
        upload_to="item_api/product_images/", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, max_length=500, blank=True)
    is_avialable = models.BooleanField(default=True)
    is_favorite = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Item.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
