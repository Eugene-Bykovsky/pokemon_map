from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, default='', blank=True)
    title_jp = models.CharField(max_length=200, default='', blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    evolved_from = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evolves_to',
        verbose_name='Из кого эволюционировал'
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,
                                on_delete=models.CASCADE,
                                related_name='entities')
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(null=True)
    health = models.IntegerField(null=True)
    strength = models.IntegerField(null=True)
    defence = models.IntegerField(null=True)
    stamina = models.IntegerField(null=True)