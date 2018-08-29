from django import template
register = template.Library()
@register.filter(name='get_class')
def get_class(value):
  return value.__class__.__name__

def check_type(obj, stype):
    try:
        t = obj.__class__.__name__
        return t.lower() == str(stype).lower()
    except:
        pass
    return False
register.filter('obj_type', check_type)
