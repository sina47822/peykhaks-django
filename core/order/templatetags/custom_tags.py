from django import template

register = template.Library()

@register.filter
def humanize_number(value):
    """Format number with thousand separator."""
    try:
        value = int(value)  # مطمئن شوید که مقدار عددی است
        return f"{value:,}".replace(",", "٬")  # کاما را با جداکننده فارسی جایگزین کنید
    except (ValueError, TypeError):
        return value  # اگر ورودی معتبر نبود، بدون تغییر برگردانید