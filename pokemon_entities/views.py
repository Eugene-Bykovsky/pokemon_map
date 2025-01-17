import folium

from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime

from pokemon_entities.models import Pokemon

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def get_image_url(pokemon, request):
    if pokemon.image:
        return request.build_absolute_uri(pokemon.image.url)
    return DEFAULT_IMAGE_URL


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    current_time = localtime()
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for pokemon_entity in pokemon.entities.filter(
                disappeared_at__gt=current_time,
                appeared_at__lte=current_time):
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                get_image_url(pokemon, request)
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': get_image_url(pokemon, request),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    current_time = localtime()
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    requested_pokemon = {
        'pokemon_id': pokemon.id,
        'img_url': get_image_url(pokemon, request),
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'previous_evolution': None,
        'next_evolution': None,
    }

    if pokemon.evolved_from:
        requested_pokemon['previous_evolution'] = {
            'pokemon_id': pokemon.evolved_from.id,
            'title_ru': pokemon.evolved_from.title_ru,
            'img_url': get_image_url(pokemon.evolved_from, request),
        }

    next_evolution = pokemon.evolves_to.first()
    if next_evolution:
        requested_pokemon['next_evolution'] = {
            'pokemon_id': next_evolution.id,
            'title_ru': next_evolution.title_ru,
            'img_url': get_image_url(next_evolution, request),
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon.entities.filter(
            disappeared_at__gt=current_time,
            appeared_at__lte=current_time
    ):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            get_image_url(pokemon, request),
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon
    })
