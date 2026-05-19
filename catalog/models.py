from django.db import models
from tinymce.models import HTMLField

class Place(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    short_description = models.TextField(verbose_name="Краткое описание", blank=True)
    long_description = HTMLField(verbose_name="Полное описание", blank=True, null=False)
    longitude = models.DecimalField(verbose_name="Долгота", max_digits=17, decimal_places=14)
    latitude = models.DecimalField(verbose_name="Широта", max_digits=17, decimal_places=14)

    def __str__(self):
        return self.title

class Image(models.Model):
    place = models.ForeignKey("Place", on_delete=models.CASCADE, verbose_name="Место", related_name='images')
    image = models.ImageField(verbose_name="Картинка",)
    images = models.PositiveIntegerField(default=0, db_index=True, verbose_name="Порядковый номер")
    class Meta:
        ordering = ["images"]

    def __str__(self):
        return self.place




