""" models for Brand,Category,GenderCategory, ProductStatus, Product """
from django.db import models
from profiles.models import UserProfile


class Brand(models.Model):
    """
    Brand model
    """

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        """
        Returns friendly name in string
        """
        return str(self.friendly_name)


class Category(models.Model):
    """
    Category models
    """

    class Meta:
        """ Adds correct plural name"""
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        """method to get category friendly name"""
        return str(self.friendly_name)


class GenderCategory(models.Model):
    """
    Gender category model
    """

    class Meta:
        """ Adds correct plural name"""
        verbose_name_plural = "Gender Categories"

    name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        """method to get category friendly name"""
        return str(self.friendly_name)


class ProductStatus(models.Model):
    """
    Product status model
    """

    class Meta:
        """ Adds correct plural name"""
        verbose_name_plural = "Product Status"

    name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        """
        Returns friendly name in string
        """
        return str(self.friendly_name)


class Product(models.Model):
    """
    Product model
    """

    category = models.ForeignKey(
        "Category", null=True, blank=True, on_delete=models.SET_NULL
    )
    gender_category = models.ForeignKey(
        "GenderCategory", null=True, blank=True, on_delete=models.SET_NULL
    )
    brand = models.ForeignKey("Brand", null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    watch_details = models.TextField()
    features = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
                                 max_digits=6,
                                 decimal_places=2,
                                 null=True,
                                 blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(
                              upload_to="products_images/",
                              null=True,
                              blank=True)
    product_status = models.ForeignKey(
        "ProductStatus", null=True, blank=True, on_delete=models.SET_NULL
    )
    featured = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=False)
    review_count = models.DecimalField(
        max_digits=6, decimal_places=0, null=True, blank=True, default=0
    )

    def __str__(self):
        return str(self.name)


class Review(models.Model):
    """ A review model for users to review products """

    RATING = [
        (5, '5'),
        (4, '4'),
        (3, '3'),
        (2, '2'),
        (1, '1'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING, default=3)
    body = models.TextField(max_length=1024)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User: {self.user} rated {self.product}, {self.product} stars.'
