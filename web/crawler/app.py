# -*- coding: utf-8 -*-
import requests, json
from database.models import Item, Service
import uuid

from geopy import Nominatim
from geopy.location import Location

from datetime import datetime

from morfeusz import *
from database import logic

lost = ["zgubiono", "zguba", "zgubiłem", "zgubiłam", "zagubiono", "zagubić", "skradziono", "ukradziony", "ukradziono"]


class FallbackLocation(object):
    latitude = 0
    longitude = 0
    address = "Nieznana lokalizacja"


class GenericCrawler(object):
    crawling_urls = []
    lost_urls_ids = []
    manual_detection = True
    geolocator = Nominatim()    # initialize geolocator
    name = ""
    service_obj = None

    schema = {
        "desc": ('HIDDEN DESCRIPTION', "text"),
        "name": ('HREF LINK', "text"),
        "url": ('HREF LINK', "href"),
        "photo": ('THUMBM IMAGE', 'src'),
        "location": None,
    }

    @staticmethod
    def process_url(url, context):
        """
        Replaces tags in url with variables from dictionary.

        :param url: url we're processing, for example "http://rak.com.pl/index.php?page={{ page }}"
        :param context: dictionary with tags and values, for example {"page": 2}
        :return: processed url
        """
        # iterate through all keys in context
        for key in context.keys():
            # replace tag with context variable
            url = url.replace("{{ "+key+" }}", context[key])

        # return url
        return url

    @staticmethod
    def detect_lost(words):
        is_lost = False
        for word in words:
            if not is_lost:
                is_lost = any(x for x in lost if x == word.lower())
            else:
                break

        return is_lost

    def process_request(self, data):
        """
        Gets data from request and parses it. Built with import.io in mind.
        :param data: item from import.io
        :return: processed dictionary
        """
        results = {}

        for key, schema in self.schema.iteritems():
            if not schema:
                continue

            try:
                value = data[schema[0]][0][schema[1]]
            except:
                value = ""
                print "WARNING. Processing failed at [%s][0][%s]" % schema

            results[key] = value

            # try to parse location
            if key == "location":
                try:
                    results["location"] = self.geolocator.geocode(value)
                except:
                    print "WARNING! Failed to detect location."

        # our work is done
        return results

    def pull_from_url(self, url, is_lost=False):
        page = 1
        crawled_pages = 1
        imported_data = []

        while True:
            print "Importing page %s" % page

            # craft context dictionary
            context = {"page": str(page)}

            # process url
            crawling_url = self.process_url(url, context)

            # attempt to get data from API
            data = requests.get(crawling_url)

            try:
                results = data.json()['extractorData']['data'][0]['group']
            except:
                # no data returned, exit
                return

            for item in results:
                result = self.process_request(item)

                # check if item is already in the database
                try:
                    last_crawled = Item.objects.filter(source=self.name, url=result['url'])
                except:
                    last_crawled = None

                self.service_obj.last_attempt = self.service_obj.last_update = datetime.now()
                self.service_obj.save()

                # check if we should keep crawling
                if last_crawled:
                    # nope, up to date guys
                    crawled_pages = page-1
                    print "Database up-to-date, good job!"
                    return imported_data, crawled_pages

                if self.manual_detection:
                    words = (result['name'] + result['desc']).split(" ")
                    is_lost = self.detect_lost(words)

                # make sure location is there
                if not result['location']:
                    result['location'] = FallbackLocation()

                imported_data += Item.objects.create(description=result['desc'],
                                                     name=result['name'],
                                                     is_lost=is_lost,
                                                     source=self.name,
                                                     photo=result['photo'],
                                                     url=result['url'],
                                                     location_lat=result['location'].latitude,
                                                     location_lon=result['location'].longitude,
                                                     location=result['location'].address,
                                                     hash=uuid.uuid1().hex
                                                     ),
            page += 1
            crawled_pages = page-1

        # return results
        return imported_data, crawled_pages

    def pull(self):
        # check if service obj is available
        if not self.service_obj:
            # create/get service object
            obj, created = Service.objects.get_or_create(name=self.name)
            obj.last_attempt = datetime.now()
            obj.save()
            self.service_obj = obj

        # initialize result variables
        imported_data = []
        crawled_pages = 0

        # iterate through crawling urls
        for pk, url in enumerate(self.crawling_urls):
            # pull data from url
            if self.manual_detection:
                imported, pages = self.pull_from_url(url)
            else:
                is_lost = pk in self.lost_urls_ids
                imported, pages = self.pull_from_url(url, is_lost)

            # append results
            imported_data += imported
            crawled_pages += pages

        return imported_data, crawled_pages
