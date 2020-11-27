from djongo import models

# Create your models here.


class Content(models.Model):
    """Content to be created, displayed, updated, delete"""
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField(blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.id)
