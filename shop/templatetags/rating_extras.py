from django import template

register = template.Library()

@register.filter
def star_range(rating):
    return range(int(rating))  # Convert rating to an integer if needed
