from django import template
from django.conf import settings
from database.models import Service, Item

register = template.Library()


@register.assignment_tag()
def get_services():
    services = {}

    for service in settings.CRAWLERS:
        try:
            services[service[1]] = Service.objects.get(name=service[1])
        except:
            services[service[1]] = None

    return services


@register.simple_tag()
def open_count():
    return len(Item.objects.filter(source="poszu.com.pl", is_open=True))


@register.simple_tag()
def success_count():
    return len(Item.objects.filter(source="poszu.com.pl", is_successful=True))


@register.simple_tag()
def fail_count():
    return len(Item.objects.filter(source="poszu.com.pl", is_open=False, is_successful=False))
