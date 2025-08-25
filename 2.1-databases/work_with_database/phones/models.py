from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='res/')
    release_date = models.DateField()
    lte_exists = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200)

    def save(self, *args, **kwargs):
        # Проверяем, установлен ли slug ранее
        if not self.slug:
            # Преобразуем название в slug
            self.slug = slugify(self.name)
        # Вызываем оригинальный метод save() базового класса модели,
        # чтобы сохранить изменения объекта в базу данных.
        super(Phone, self).save(*args, **kwargs)
