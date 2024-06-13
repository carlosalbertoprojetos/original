from django import template
from .notifications_tags import show_notifications

register = template.Library()
register.inclusion_tag("includes/notifications.html")(show_notifications)
