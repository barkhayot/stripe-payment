from django.db import models

# Create your models here.


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.name

# Pack Model
class Pack(models.Model):
    creted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}___{self.creted_at}'

# Order Model
class Order(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart            = models.ForeignKey(Pack, on_delete=models.CASCADE)
    qantity         = models.IntegerField(default=1)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
