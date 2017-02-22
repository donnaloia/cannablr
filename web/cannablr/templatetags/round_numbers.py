from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def roundnumbers(value):
	if value > 1.75 and value < 2.25:
		return '<img src="/static/img/stars2/2stars.png">'
	elif value > 2.25 and value < 2.75:
		return '<img src="/static/img/stars2/25stars.png">'
	elif value > 2.75 and value < 3.25:
		return '<img src="/static/img/stars2/3stars.png">'
	elif value > 3.25 and value < 3.75:
		return '<img src="/static/img/stars2/35stars.png">'
	elif value > 3.75 and value < 4.25:
		return '<img src="/static/img/stars2/4stars.png">'
	elif value > 4.25 and value < 4.75:
		return '<img src="/static/img/stars2/45stars.png">'
	elif value > 4.75 and value < 5.25:
		return '<img src="/static/img/stars2/5stars.png">'
	if not value:
		return '<img src="/static/img/stars2/5stars.png">'