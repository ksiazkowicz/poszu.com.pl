# -*- coding: utf-8 -*-
import requests, json
from models import Item

import uuid

from django.shortcuts import render_to_response, get_object_or_404, HttpResponsePermanentRedirect, HttpResponseRedirect, Http404
from django.template import RequestContext

from morfeusz import *

import logic

lost = ["zgubiono", "zguba", "zgubiłem", "zgubiłam", "zagubiono", "zagubić", "skradziono", "ukradziony", "ukradziono"]

# geolocation
from geopy.geocoders import Nominatim


def pull_from_gumtree(request, template="gumtree_result.html"):    
    # initialize geolocator
    geolocator = Nominatim()
    
    page = 1
    crawled_pages = 1
    
    imported_data = []
            
    while True:
        print "Importing page %s" % page
        
        crawling_url = "https://extraction.import.io/query/runtime/eeb84685-a55f-4dd2-929c-acf349c8025f?_apikey=1d7510385b8a44e0aae52fcb69cd92596aab14039d36aca6e26593d0719c357aecfc66c2fd72b082368a1d8a81e60a1750d29277d4b9de345ac6d6a95dff63f49c528c9985929814ea31dd0f875a4b4d&url=http%3A%2F%2Fwww.gumtree.pl%2Fs-rzeczy-zagubione%2Fpage-" + str(page) + "%2Fv1c9036p" + str(page)
        data = requests.get(crawling_url)
        
        try:
            results = data.json()['extractorData']['data'][0]['group']
        except:
            # no data returned, exit
            return

        for item in results:
            desc = item['HIDDEN DESCRIPTION'][0]['text']
            name = item['HREF LINK'][0]['text']
            url = item['HREF LINK'][0]['href']

            # check if item is already in the database
            try:
                last_crawled = Item.objects.filter(source="Gumtree", url=url)
            except:
                last_crawled = None

            if last_crawled:
                crawled_pages = page-1
                # check if we should keep crawling
                print "Database up-to-date, good job!"
                return render_to_response(template, locals(), context_instance=RequestContext(request))

            try:
                photo = item['THUMBM IMAGE'][0]['src']
            except:
                photo = None

            try:
                location = geolocator.geocode(item['CATEGORY VALUE'][0]['text'].replace("zgubiono lub znaleziono , ", ""))
            except:
                print "znowu jakies timeouty, ugh"
                continue
                
            words = desc.split(" ")
            is_lost = False

            for word in words:
                if not is_lost:
                    is_lost = any(x for x in lost if x == word.lower())
                else:
                    break

            #print "Importing %s from Gumtree" % (name) 
            imported_data += Item.objects.create(description=desc,name=name,is_lost=is_lost,source="Gumtree",photo=photo,url=url,location_lat=location.latitude,location_lon=location.longitude, location=location.address, hash=uuid.uuid1().hex),
                    
        page+=1
        crawled_pages = page-1

    return render_to_response(template, locals(), context_instance=RequestContext(request))


def pull_from_oglaszamy24(request, template="gumtree_result.html"):    
    # initialize geolocator
    geolocator = Nominatim()
    
    page = 1
    crawled_pages = 1
    
    imported_data = []
    
    crawling_phase = [True, False]
            
    for is_lost in crawling_phase:
        if is_lost:
            category_name = "zgubione"
        else:
            category_name = "znalezione"
        
        while True:
            print "Importing page %s of %s" % (page, category_name)
            crawling_url = "https://extraction.import.io/query/runtime/b95b5a1a-ef4f-4663-92d9-b59825eccd87?_apikey=1d7510385b8a44e0aae52fcb69cd92596aab14039d36aca6e26593d0719c357aecfc66c2fd72b082368a1d8a81e60a1750d29277d4b9de345ac6d6a95dff63f49c528c9985929814ea31dd0f875a4b4d&url=http%3A%2F%2Fwww.oglaszamy24.pl%2Fogloszenia%2Fpozostale%2F"+category_name+"%2F%3Fstd%3D"+str(page)+"%26amp%3Bresults%3D"+str(page)
            data = requests.get(crawling_url)
                    
            try:
                results = data.json()['extractorData']['data'][0]['group']
            except:
                # no data returned, exit
                break

            for item in results:
                desc = item['DESCRIPTION'][0]['text']
                name = item['TITLE LINK'][0]['text']
                url = item['TITLE LINK'][0]['href']

                # check if item is already in the database
                try:
                    last_crawled = Item.objects.filter(source="Oglaszamy24", url=url)
                except:
                    last_crawled = None

                if last_crawled:
                    crawled_pages = page-1
                    # check if we should keep crawling
                    print "Database up-to-date, good job!"
                    return render_to_response(template, locals(), context_instance=RequestContext(request))

                try:
                    photo = item['IMAGE'][0]['src']
                except:
                    photo = None

                try:
                    location = geolocator.geocode(item['CAT LINK'][0]['text'])
                except:
                    print item['CAT LINK'][0]['text']
                
                if not location:
                    print "No location data found for %s, ugh." % item['CAT LINK'][0]['text']
                    continue

                #print "Importing %s from Oglaszamy" % (name) 
                imported_data += Item.objects.create(description=desc,name=name,is_lost=is_lost,source="Oglaszamy24",photo=photo,url=url,location_lat=location.latitude,location_lon=location.longitude, location=location.address, hash=uuid.uuid1().hex),

            page+=1
            crawled_pages = page-1

    return render_to_response(template, locals(), context_instance=RequestContext(request))

def pull_from_oglaszamy24_2(request, template="gumtree_result.html"):    
    # initialize geolocator
    geolocator = Nominatim()
    
    page = 1
    crawled_pages = 1
    
    imported_data = []
    
    is_lost = False
    crawling_phase = "ugh"
            
    for blah in crawling_phase:
        category_name = "znalezione"
        
        while True:
            print "Importing page %s of %s" % (page, category_name)
            crawling_url = "https://extraction.import.io/query/runtime/b95b5a1a-ef4f-4663-92d9-b59825eccd87?_apikey=1d7510385b8a44e0aae52fcb69cd92596aab14039d36aca6e26593d0719c357aecfc66c2fd72b082368a1d8a81e60a1750d29277d4b9de345ac6d6a95dff63f49c528c9985929814ea31dd0f875a4b4d&url=http%3A%2F%2Fwww.oglaszamy24.pl%2Fogloszenia%2Fpozostale%2F"+category_name+"%2F%3Fstd%3D"+str(page)+"%26amp%3Bresults%3D"+str(page)
            data = requests.get(crawling_url)
                    
            try:
                results = data.json()['extractorData']['data'][0]['group']
            except:
                # no data returned, exit
                break

            for item in results:
                desc = item['DESCRIPTION'][0]['text']
                name = item['TITLE LINK'][0]['text']
                url = item['TITLE LINK'][0]['href']

                # check if item is already in the database
                try:
                    last_crawled = Item.objects.filter(source="Oglaszamy24", url=url)
                except:
                    last_crawled = None

                if last_crawled:
                    crawled_pages = page-1
                    # check if we should keep crawling
                    print "Database up-to-date, good job!"
                    return render_to_response(template, locals(), context_instance=RequestContext(request))

                try:
                    photo = item['IMAGE'][0]['src']
                except:
                    photo = None

                try:
                    location = geolocator.geocode(item['CAT LINK'][0]['text'])
                except:
                    print item['CAT LINK'][0]['text']
                
                if not location:
                    print "No location data found for %s, ugh." % item['CAT LINK'][0]['text']
                    continue

                #print "Importing %s from Oglaszamy" % (name) 
                imported_data += Item.objects.create(description=desc,name=name,is_lost=is_lost,source="Oglaszamy24",photo=photo,url=url,location_lat=location.latitude,location_lon=location.longitude, location=location.address, hash=uuid.uuid1().hex),

            page+=1
            crawled_pages = page-1

    return render_to_response(template, locals(), context_instance=RequestContext(request))