from django.db import models

class Vacancy(models.Model):
    hh_id = models.CharField(max_length=100, unique=True)  # ID вакансии на hh.ru
    name = models.CharField(max_length=255)  # Название вакансии
    company = models.CharField(max_length=255)  # Название компании
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=1.00 ,null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, default=1.00 ,null=True)
    url = models.URLField()  # URL вакансии
    published_at = models.DateTimeField()  # Дата публикации

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancs"
