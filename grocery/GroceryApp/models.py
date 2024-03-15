from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    STATE_CHOICES = [
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CT', 'Chhattisgarh'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OR', 'Odisha'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TG', 'Telangana'),
        ('TR', 'Tripura'),
        ('UP', 'Uttar Pradesh'),
        ('UK', 'Uttarakhand'),
        ('WB', 'West Bengal'),
        ('AN', 'Andaman and Nicobar Islands'),
        ('CH', 'Chandigarh'),
        ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('DL', 'Delhi'),
        ('JK', 'Jammu and Kashmir'),
        ('LA', 'Ladakh'),
        ('LD', 'Lakshadweep'),
        ('PY', 'Puducherry'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    pincode = models.IntegerField(
        default=0,
        blank=True,
        null=True,
    )
    
    def __str__(self):
        return str(self.id)
    
class Grocery(models.Model):

    CATEGORY_CHOICES = [
        ('VEGETABLES', 'vegetables'),
        ('FRUITS', 'fruits'),
        ('PHARMACY', 'pharmacy'),
        ('PETFOOD','petfood'),
        ('JUICES','juices'),
        ('SPROUTS','sprouts'),
        ('MILKS','milks'),
        ('BREADS','breads')
        
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    unit = models.CharField(max_length=50,default='1-kg')
    storage_tips = models.CharField(max_length=300)
    nutrient_benefits = models.TextField()
    description = models.TextField()
    disclaimer = models.TextField()
    selling_price = models.IntegerField()
    discounted_price = models.IntegerField()
    discounted_percentage = models.IntegerField(default=1)
    grocery_image =models.ImageField(upload_to='grocery_images') 

    def __str__(self):
        return str(self.id)
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Grocery, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)        

    def __str__(self):
        return str(self.id)
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    grocery_product = models.ForeignKey(Grocery, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)