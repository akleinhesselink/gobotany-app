"""Template tags and filters for mapping."""

from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('_location_map.html')
def location_map(**kwargs):
    maps_static_key = settings.GMAPS_STATIC_KEY
    location = kwargs['location']
    width_px = kwargs['width_px']
    height_px = kwargs['height_px']
    zoom = kwargs['zoom']
    id = kwargs['id']
    return {
        'maps_static_key': maps_static_key,
        'location': location,
        'width_px': width_px,
        'height_px': height_px,
        'zoom': zoom,
        'id': id
    }

@register.inclusion_tag('_sightings_map.html')
def sightings_map(**kwargs):
    latitude = kwargs['latitude']
    longitude = kwargs['longitude']
    center_title = kwargs['center_title']
    height = kwargs['height']
    width = kwargs['width']
    zoom = kwargs['zoom']
    id = kwargs['id']
    return {
        'latitude': latitude,
        'longitude': longitude,
        'center_title': center_title,
        'height': height,
        'width': width,
        'zoom': zoom,
        'id': id
    }

