from django.db import models

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)

class Sensor(models.Model):

    name = models.CharField(max_length = 50, null = False, verbose_name = 'Название датчик')
    description = models.CharField(max_length = 100, null = False, verbose_name ='Описание датчика')

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        ordering = ['name']

    def __str__(self):
        return self.name


class Measurement(models.Model):


    temperature = models.DecimalField(max_digits = 5, decimal_places = 1, null = False,
                                      verbose_name ='Температура')
    created_at = models.DateTimeField(auto_now_add = True, verbose_name ='Время фиксации')
    sensor = models.ForeignKey(Sensor, on_delete = models.CASCADE, related_name='measurements')

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'

    def __str__(self):
        return f"Temperature: {self.temperature}°C on {self.created_at}"
