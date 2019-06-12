from django.db import models

# Create your models here.
class Products(models.Model):
  id = models.AutoField(primary_key = True)
  name = models.CharField(max_length=255)

  def __str__(self):
        return "{} - {}".format(self.id, self.name)

class Sales(models.Model):
  item = models.ForeignKey(Products, on_delete=models.CASCADE)
  week = models.IntegerField()
  year = models.IntegerField()
  stock = models.IntegerField()
  location = models.CharField(max_length=255)
  type = models.CharField(max_length=255)


  def __str__(self):
        return "{} - {}".format(self.year, self.stock)