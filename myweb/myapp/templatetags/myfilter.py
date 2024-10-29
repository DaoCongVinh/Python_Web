from atexit import register
from django import template
register = template.Library()

@register.filter

def make_capitalize(value):
    return value.capitalize()

# Hàm make_capitalize() có 1 tham số
# Khi gọi hàm ở template thì tham số|make_capitalize

@register.filter

def is_empty_list(list_object):
    return len(list_object) == 0

@register.filter

def make_range(num):
    return range(1,num+1)


@register.filter

def make_serial(current_page, index_loop):
    # Số phần tử trên 1 trang 5
    # Current_page = 2
    # Index_loop = 3
    # Index trả về là 8 = index_loop + (Số item trên 1 trang * (current_page - 1))
    return index_loop + 5*(current_page - 1)