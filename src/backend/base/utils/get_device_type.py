import re


def get_device_type(request):
    device = {}

    ua = request.META.get('HTTP_USER_AGENT', '').lower()

    if ua.find("iphone") > 0:
        device['iphone'] = "iphone" + re.search("iphone os (\d)", ua).groups(0)[0]

    if ua.find("ipad") > 0:
        device['ipad'] = "ipad"

    if ua.find("android") > 0:
        device['android'] = "android" + re.search("android (\d\.\d)", ua).groups(0)[0].translate(None, '.')

    device['classes'] = " ".join(v for (k,v) in device.items())

    return device
