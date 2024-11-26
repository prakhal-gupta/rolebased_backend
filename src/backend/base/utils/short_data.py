import re


def get_first_name(email):
    regexStr = r'([a-zA-Z]+)'
    matchobj = re.search(regexStr, email)
    if matchobj:
        return matchobj.group(1)



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
