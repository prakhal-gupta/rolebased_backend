import locale
import pandas as pd
from django import template

register = template.Library()


@register.filter
def split(str, splitter):
    return str.split(splitter) if str else []


@register.filter
def mul(one, two):
    if one and two:
        return float(one) * float(two)
    else:
        return 0.0


@register.filter
def mul_float(one, two):
    if one and two:
        return float(float(one) * float(two))
    else:
        return 0.0


@register.filter
def to_date(date_str, two=None):
    return pd.to_datetime(date_str)


@register.filter
def to_dmy_date(date_str, two=None):
    return pd.to_datetime(date_str).strftime('%d-%m-%Y')


@register.filter
def div(one, two):
    return one / two if two != 0 else 0


@register.filter
def sub(one, two):
    if one is not None and two is not None:
        return float(one) - float(two)
    else:
        return 0.0


@register.filter
def roundoff(one, two):
    if one and two is not None:
        return round(one, two)
    else:
        return 0.0


@register.filter
def add(one, two):
    if one and two:
        return one + two
    elif one:
        return one
    elif two:
        return two
    else:
        return 0.0

@register.filter
def sum_of_list(num_list, key):
    if key:
        return sum(item[key] for item in num_list)
    else:
        return sum(num_list)


@register.filter
def find_no_form_name(data, total):
    result = []
    allowed = 0
    for record in data:
        if record['form_name'] is None:
            for i in record.get('declarations', []):
                result.append(i)
            allowed += record.get('allowed', 0)
    return allowed if total else result


@register.filter
def remove_empty_form_name(data):
    result = []
    for i in data:
        if i.get('form_name', None):
            result.append(i)
    return result


@register.filter
def alpha(num):
    return chr(96 + num)


@register.filter
def roman(num):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syb = [
        "m", "cm", "d", "cd",
        "c", "xc", "l", "xl",
        "x", "ix", "v", "iv",
        "i"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num


@register.filter
def user_name(data):
    if data:
        user = data.get('first_name', '')
        if data.get('middle_name', ''):
            user += " " + data.get('middle_name', '')
        if data.get('last_name', ''):
            user += " " + data.get('last_name', '')
        return user
    else:
        return " "


@register.filter
def user_address(data):
    if data:
        address = ''
        if data.get('corr_addr_l1', ''):
            address += data.get('corr_addr_l1', '') + ", "
        if data.get('corr_addr_l2', ''):
            address += data.get('corr_addr_l2', '') + ", "
        if data.get('corr_dist_data', ''):
            address += data.get('corr_dist_data', {}).get('value', '') + ", "
        if data.get('corr_state_data', ''):
            address += data.get('corr_state_data', {}).get('value', '') + ", "
        if data.get('corr_pincode', ''):
            address += str(data.get('corr_pincode', '')) + ", "
        return address[:-2]
    else:
        return " "



@register.filter
def half_day(data):
    if data // 1 == data / 1:
        return int(data)
    return data


@register.filter
def less_slab_rows(data):
    result = 4 - len(data)
    return range(result if result > 0 else 0)


@register.filter
def dict_length_add_counter(data, counter):
    return len(data) + counter


@register.filter
def fetch_dict(result, key):
    return result[key] if key in result else []


@register.filter
def none_check(data):
    if data:
        return data
    return "--"


@register.filter
def round_comma(data):
    if data or data == 0:
        locale.setlocale(locale.LC_MONETARY, 'en_IN')
        return locale.currency(data, grouping=True).replace("₹", "").replace(".00", "")
    else:
        return ""


@register.filter
def generated_on(input_datetime):
    formatted_date = input_datetime.strftime("%d/%m/%Y")
    formatted_time = input_datetime.strftime("%I:%M:%S %p")
    formatted_datetime = f"on {formatted_date} at {formatted_time}"
    return formatted_datetime
