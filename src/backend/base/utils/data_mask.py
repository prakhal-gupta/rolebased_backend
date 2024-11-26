def encrypt_mobile(mobile):
    try:
        if mobile:
            mobile_num = mobile
            mobile_num = mobile_num[:2] + "*" * (len(mobile_num) - 2) + mobile_num[7:]
            return "%s" % mobile_num
    except Exception as e:
        print(str(e))
        return mobile
        

def encrypt_email(email):
    try:
        if email:
            username, domain = email.split("@")
            username = username[:6] + "**" 
            domain = domain[:2] + "**" + domain[-3:]
            return "%s@%s" % (username, domain)
    except Exception as e:
        print(str(e))
        return email

def get_client_browser_ip(request):
    """
    Get The Customer IP where Payment is going to Happen
    """
    try:
        client_address = request.META['HTTP_X_REAL_IP']
        if client_address:
            return client_address
    except:
        client_address = request.META['REMOTE_ADDR']
        if client_address:
            return client_address
