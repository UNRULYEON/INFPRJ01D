from django.db import models

# Create your models here.
class Sales(models.Model):
  date = models.IntegerField()
  stock = models.IntegerField()

  def __str__(self):
        return "{} - {}".format(self.quantity_sold, self.stock)