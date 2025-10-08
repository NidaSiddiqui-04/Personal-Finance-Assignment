from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Transactions(models.Model):
     TYPE_CHOICES=(
          ('Income','Income'),
          ('Expense','Expense'),
     )
     CATEGORY_CHOICES=(
         ('Salary','Salary'),
          ('Food','Food'),
          ('Rent','Rent'),
         ('Travel','Travel'),
          ('Entertainment','Entertainment')
     )




     user=models.ForeignKey(User ,on_delete=models.CASCADE,null=False)
     amount=models.DecimalField(max_digits=20,decimal_places=2)
     type=models.CharField(max_length=10,choices=TYPE_CHOICES)
     category=models.CharField(max_length=20,choices=CATEGORY_CHOICES)
     date=models.DateField(default=timezone.now)
     notes=models.TextField(blank=True,null=True)
     def __str__(self):
          return f'{self.type}-{self.amount}-{self.category}'