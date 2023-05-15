from django.db import models
from django.core.validators import MaxValueValidator,RegexValidator
# Create your models here.
class Credit(models.Model):
    Card_num=models.CharField(max_length=16,validators=[RegexValidator(r'^[0-9]{16}$')])
    holder_name=models.CharField(max_length=30)
    cvv=models.CharField(max_length=3,validators=[RegexValidator(r'^[0-9]{3}$')])
    valid_month=models.CharField(max_length=2,validators=[RegexValidator(r'^[0-9]{2}$')])
    valid_year=models.CharField(max_length=4,validators=[RegexValidator(r'^[0-9]{4}$')])
    mobile=models.CharField(max_length=13,default=0)
    email=models.CharField(max_length=30,default=0)
    image=models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,default='temp.jpeg')