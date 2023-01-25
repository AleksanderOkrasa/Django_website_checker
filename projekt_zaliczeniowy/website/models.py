from django.db import models


#password = kali


URL_STATUS = (
    ('available', 'Available'),
    ('notAvailable', 'Not Available')
)


class WebpageData(models.Model):
    name_webpage = models.CharField(max_length=1000, primary_key=True)
    status = models.CharField(choices=URL_STATUS, max_length=30, default='notAvailable')
    first_search_user = models.CharField(max_length=255, blank=True, null=True)
    search_value = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)
    count_of_search = models.IntegerField('count of search', default=1)
    buttons = models.IntegerField(null=True)
    links = models.IntegerField(null=True)
    def __str__(self):
        return self.name_webpage
    def __repr__(self):
        return self.name_webpage

class UserData(models.Model):
    user_web = models.CharField(max_length=1255, primary_key=True)
    user = models.CharField(max_length=255)
    webpage = models.ForeignKey(WebpageData, on_delete=models.CASCADE, related_name='users')
    count_of_search = models.IntegerField('count of search', default=1)
    def __str__(self):
        return self.user_web
    def __repr__(self):
        return self.user_web



