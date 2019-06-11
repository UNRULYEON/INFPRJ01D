from django.db import models

# Create your models here.
class Sales(models.Model):
  item = models.IntegerField()
  week = models.IntegerField()
  year = models.IntegerField()
  stock = models.IntegerField()
  location = models.CharField(max_length=255)
  type = models.CharField(max_length=254)

  def __str__(self):
        return "{} - {}".format(self.year, self.stock)