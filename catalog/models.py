from django.db import models
from tinymce import models as tinymce_models

class Place(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description_short = models.TextField(verbose_name="Краткое описание", blank=True)
    description_long = tinymce_models.HTMLField(verbose_name="Полное описание", blank=True)
    longitude = models.DecimalField(verbose_name="Долгота", max_digits=17, decimal_places=14)
    latitude = models.DecimalField(verbose_name="Широта", max_digits=17, decimal_places=14)


    def __str__(self):
        return f"{self.title}"




