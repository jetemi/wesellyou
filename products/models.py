from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Category(models.Model):
    '''Category model for products'''

    class Meta:
        '''Specify correct spelling for plural - for admin site'''
        verbose_name_plural = 'Categories'

    name=models.CharField(max_length=50, unique=True)
    friendly_name=models.CharField(max_length=50)

    def __str__(self):
        '''string method - return the category name'''
        return self.name

    def get_friendly_name(self):
        """return the user friendly name - for views"""
        return self.friendly_name

class Product(models.Model):
    '''Product model - for products in shop'''
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products_in_category')
    sku = models.CharField(max_length=10, null=False, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_new = models.BooleanField(default=True)

    def generate_sku(self):
        """generate sku, called by post save method add_sku_when_created"""
        leading_zeros = '0' * (6 - len(str(self.pk)))
        return f'{self.category.name[:3].upper()}-{leading_zeros}{self.pk}'

    def __str__(self):
        """string method - return the product name and category"""
        return f'{self.name} in {self.category}'


@receiver(post_save, sender=Product)
def add_sku_when_created(sender, instance, created, **kwargs):
    """
    Each time instance of Product is created, call generate_sku method to
    add the sku to the product.
    Method uses instance id, so needs to be done post save.
    Only one signal so including here in model file instead of signals.py file.
    """
    if created:
        if not instance.sku:
            instance.sku = instance.generate_sku()
            instance.save()