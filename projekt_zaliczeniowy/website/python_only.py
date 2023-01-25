
from .models import WebpageData, UserData
from django.contrib.auth.models import User
from django.db.models import Sum

import logging
import requests
from bs4 import BeautifulSoup


class log():
    logging.format = logging.Formatter("%(asctime)s  ::: %(levelname)s ::: %(message)s", datefmt='%Y/%m/%d %H:%M:%S')
    logging.logging_root = logging.getLogger()
    logging.fileHandler = logging.FileHandler('website/website_logs.log')
    logging.fileHandler.setFormatter(logging.format)
    logging.logging_root.addHandler(logging.fileHandler)

    logging.consoleHandler = logging.StreamHandler()
    logging.consoleHandler.setFormatter(logging.format)
    logging.logging_root.addHandler(logging.consoleHandler)

    logging.logging_root.setLevel(logging.DEBUG)

    def error(message):
        return (logging.logging_root.error(message))

    def info(message):
        return (logging.logging_root.info(message))

    def warning(message):
        return (logging.logging_root.warning(message))

    def debug(message):
        return (logging.logging_root.debug(message))

logging.logging_root.info("log")


class webpage_data():
    def __init__(self, search_value, webpage, current_user):
        self.__webs = WebpageData.objects.all()
        self.__search_value = search_value
        self.__webpage = webpage
        self.__current_user = current_user

        if self.__webs.filter(pk=self.__webpage).exists():
            self.increment()
        else:
            self.create()

    def increment(self):
        web = self.__webs.get(pk=self.__webpage)
        web.count_of_search += 1
        log.info(f'increment count_of_search in {self.__webpage}, now is {web.count_of_search}')
        web.save()
        log.info(f'{self.__webpage} data was been saved')

    def create(self):
        log.warning(f'do not find a record {self.__webpage} in DB')
        web = WebpageData(name_webpage=self.__webpage, first_search_user=self.__current_user, search_value=self.__search_value)
        web.save()
        log.info(f'{self.__webpage} was been added to DB')

        try:
            check_webpage = check_url(self.__search_value)
            check_webpage.check_conection()
            web.url = check_webpage.url
            log.info(f'added url {web.url} to {self.__webpage}')
            if check_webpage.isavailable:
                web.status = 'available'
                check_webpage.check_buttons_and_links()
                web.buttons = check_webpage.buttons
                web.links = check_webpage.links
                log.info(f'webpage {self.__webpage} is available, find {web.buttons} buttons and {web.links} links')
            else:
                log.info(f'webpage {self.__webpage} is not available')

        except:
            log.info(f'{self.__webpage} is not available')
        web.save()
        log.info(f'{self.__webpage} data was been saved')

class user_web_data():
    def __init__(self, user, webpage):
        self.__user = user
        self.__webpage = webpage
        self.__user_web = f"{user}_{webpage}"
        self.__web = WebpageData.objects.get(pk = webpage)
        log.info(f'user_web = {self.__user_web}')
        self.__userdata = UserData.objects.all()
        if not self.__userdata.filter(pk=self.__user_web).exists():
            self.create()
        else:
            self.increment()



    def create(self):
        log.warning(f'do not find a record {self.__user_web} in DB')
        user_web = UserData(user_web=self.__user_web, user=self.__user, webpage=self.__web)
        log.info(f'added {self.__user_web} to DB')
        user_web.save()

    def increment(self):
        user_web = self.__userdata.get(pk=self.__user_web)
        user_web.count_of_search += 1
        user_web.save()

def user_add_up():
    users = User.objects.all()
    results = {}
    for user in users:
        userdata = UserData.objects.filter(user=user.username)
        result = userdata.aggregate(total = Sum('count_of_search'))
        results[user.username] = result["total"]
        print(results[user.username])
    return(results)

def web_add_up():
    webs = WebpageData.objects.all()
    results = {}
    for web in webs:
        count = 0
        webdata = UserData.objects.filter(webpage=web)
        for user in webdata:
            count = count + 1
        results[web] = count
        print(results[web])
    return(results)


class check_url():

        def __init__(self, webpage):
            url = 'https://' + webpage
            self.__response = requests.get(url)
            self.__url = self.__response.url

        def __repr__(self):
            return self.url

        def __str__(self):
            return self.url

        @property
        def url(self):
            return self.__url

        @property
        def isavailable(self):
            return self.__available

        @property
        def buttons(self):
            return self.__buttons_count

        @property
        def links(self):
            return self.__links_count

        def check_conection(self):

            if self.__response.status_code in range(200, 300):
                self.__available = True
            else:
                self.available = False

            return self.__available

        def check_buttons_and_links(self):

            self.__soup = BeautifulSoup(self.__response.text, 'html.parser')

            self.__buttons = self.__soup.find_all('button')
            self.__buttons_count = len(self.__buttons)

            self.__links = self.__soup.find_all('a')
            self.__links_count = len(self.__links)

        def show_results(self):
            if self.isavailable:
                log.info(f'url: {self.url}\nprzyciskow: {self.buttons}\nlinkow: {self.links}')
            else:
                print('Strona jest nie osiagalna')