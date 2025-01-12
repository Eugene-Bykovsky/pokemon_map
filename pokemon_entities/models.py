from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200,
                                verbose_name='Название (русское)')
    title_en = models.CharField(max_length=200, default='', blank=True,
                                verbose_name='Название (английское)')
    title_jp = models.CharField(max_length=200, default='', blank=True,
                                verbose_name='Название (японское)')
    image = models.ImageField(null=True, blank=True,
                              verbose_name='Изображение')
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание')
    evolved_from = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evolves_to',
        verbose_name='Из кого эволюционировал'
    )

    class Meta:
        verbose_name = 'Покемон'
        verbose_name_plural = 'Покемоны'

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,
                                on_delete=models.CASCADE,
                                related_name='entities',
                                verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(null=True,
                                       verbose_name='Появился в')
    disappeared_at = models.DateTimeField(null=True,
                                          verbose_name='Исчез в')
    level = models.IntegerField(null=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, verbose_name='Сила')
    defence = models.IntegerField(null=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, verbose_name='Выносливость')

    class Meta:
        verbose_name = 'Экземпляр покемона'
        verbose_name_plural = 'Экземпляры покемонов'

    def __str__(self):
        return f"Экземпляр покемона {self.pokemon.title_ru}"
