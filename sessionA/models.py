from django.db import models

class Signup(models.Model):
    Name = models.CharField(max_length=100, unique=True)
    Password = models.CharField(max_length=255)
    
    class Meta:
     db_table = "Signup"
     ordering = ["id"] 

class ApiData(models.Model):
    Name = models.CharField(max_length=100)
    Invested_Amount = models.DecimalField(max_digits=10, decimal_places=2)
    fund_code = models.CharField(max_length=50)
    Units_held = models.DecimalField(max_digits=10, decimal_places=2)
    fund_name = models.CharField(max_length=255)
    nav = models.DecimalField(max_digits=10, decimal_places=2)
    current_value = models.DecimalField(max_digits=10, decimal_places=2)
    Growth = models.DecimalField(max_digits=10, decimal_places=2)



    class Meta:
     db_table = "ApiData"
     ordering = ["id"] 

