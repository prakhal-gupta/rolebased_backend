from rest_framework.fields import FileField

class CustomFileField(FileField):
    use_url = False
