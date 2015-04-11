from django import template

register = template.Library()


@register.filter(name='get_new_alerts_num')
def get_new_alerts_num(alerts):
    num = alerts.filter(is_viewed=False).count()
    return num
