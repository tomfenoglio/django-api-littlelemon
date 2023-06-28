from django.db import models
from django.contrib.auth.models import User

# Django will create an implicit PK named id for every model unless a custom primary key is specified.

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True) #db_index creates an index in the database for efficient lookups based on this field

    def __str__(self):
        return f'{self.title}'


class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu items'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # User its a built-in Django model that represents user accounts
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        unique_together = ('menuitem', 'user')
        # the combination of values in these two fields must be unique to ensure that a user can only have one entry for a specific menu item in their cart

    def __str__(self):
        return f'{self.user}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='delivery_crew', null=True)
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(db_index=True)

    def __str__(self):
        return f'{self.user} {self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.order}'

    class Meta:
        unique_together = ('order', 'menuitem')
