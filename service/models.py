from django.db import models

# Create your models here.
class item(models.Model):
    item_id =  models.AutoField
    item_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.item_name
    

class  lost_item(models.Model):
    ITEM_CHOICES = [
        ('purse', 'Purse/Bag'),
        ('phone', 'Phone'),
        ('bottle', 'Bottle'),
        ('watch', 'Watch'),
        ('umbrella', 'Umbrella'),
        ('others', 'Others'),
    ]

    date = models.DateField()
    location = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    specific_mark = models.CharField(max_length=255,default='')
    shape = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    item_category = models.CharField(max_length=50, choices=ITEM_CHOICES,default='')
    def __str__(self):
        return f"{self.item_category} - {self.date}"
    

class  found_item(models.Model):
    ITEM_CHOICES = [
        ('purse', 'Purse/Bag'),
        ('phone', 'Phone'),
        ('bottle', 'Bottle'),
        ('watch', 'Watch'),
        ('umbrella', 'Umbrella'),
        ('others', 'Others'),
    ]

    date = models.DateField()
    location = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    specific_mark = models.CharField(max_length=255,default='')
    shape = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    material = models.CharField(max_length=100,default='')
    item_category = models.CharField(max_length=50, choices=ITEM_CHOICES,default='')
    def __str__(self):
        return f"{self.item_category} - {self.date}"
    
class contactenquiry(models.Model):
    contactid = models.AutoField
    name=models.CharField(max_length=50 ,null=True, blank=True)
    email=models.CharField(max_length=50)
    message=models.TextField()

    def __str__(self):
        return self.name