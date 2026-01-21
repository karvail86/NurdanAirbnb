from .models import City, Service, Room, Property, Review
from modeltranslation.translator import TranslationOptions, register


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name',)


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('service_name',)


@register(Property)
class PropertyTranslationOptions(TranslationOptions):
    fields = ('property_name',)


@register(Room)
class RoomTranslationOptions(TranslationOptions):
    fields = ('description',)

@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('comment',)