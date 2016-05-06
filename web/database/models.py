# -*- coding: utf-8 -*-
#
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField
from osm_field.fields import LatitudeField, LongitudeField, OSMField

from morfeusz import *

import uuid

import hashlib, os
from geopy.distance import great_circle
from datetime import datetime
from django.utils import timezone

obvious_words = ['w','.','na',u'pobliżu','o','z','kontakt','właścicielem','prosimy',',','lub','bd','mi','u','ja','i','dla',u'','za','do','zna','ten','do','znalazc','znalazca','nagroda','godzina','jej','on','opis','(',')','warta','wart','prosz','uczciwy','przyjacielu','drogi','drog','a','jak','tam','mam','m','przez','si','moj','co','kt','r','zostaa','go','t']

class Item(models.Model):
    email = models.CharField(_("E-Mail"),max_length=128,blank=False)
    name = models.CharField(_("Name"),max_length=128,blank=False)
    photo = ImageField(_("Photo"),upload_to="media/photos",blank=True)
    description = models.CharField(_("Description"),max_length=300)
    upload_date = models.DateTimeField(_("Uploaded date"),auto_now=True)
    url = models.CharField(_("URL"), max_length=400, blank=True)
    source = models.CharField(_("Source"), max_length=20, default="poszu.com.pl")
    
    location = OSMField()
    location_lat = LatitudeField()
    location_lon = LongitudeField()
    
    is_lost = models.BooleanField(_("Is a lost object"),default=False)
    is_open = models.BooleanField(_("Is open?"), default=True)
    is_successful = models.BooleanField(_("Was a success?"), default=False)
    hash = models.CharField(_("Hash"),max_length=256, blank=False)
    
    uuid.uuid1().hex
    
    def __unicode__(self):
        return self.name
    
    def auth_hash(self):
        m = hashlib.new('ripemd160')
        m.update(self.description.encode("ASCII",'ignore'))
        return m.hexdigest()[:6]
    
    def gimme_link(self):
        return "http://127.0.0.1:8000/item/"+str(self.hash)+"/auth/"+str(self.auth_hash())+"/"
    
    def variations_hashes(self):
        phrases = self.description.split(" ")
        
        hashes = []
        
        for sentence in phrases:
            word = sentence
            try:
                base = ""
                for a in analyse(word):
                    if base == "":
                        base = a[0][1].split(":")[0]
                        
                    c = os.path.commonprefix([base,a[0][1].split(":")[0]])
                    base = c
                    if not c in hashes and not c in obvious_words:
                        hashes += c.lower(),
            except:
                pass
            
        return hashes
    
    def close_event(self,success):
        self.is_open = False
        self.is_successful = success
        self.save()
            
    def compare_hashes(self,hashes,object):
        #print(object.name)
        try:
            distance = great_circle((object.location_lat, object.location_lon), (self.location_lat,self.location_lon)).kilometers
        except:
            print "ugh, fix laterz"
            distance = 0
        #print("Distance from %s to %s (self): %s" % (object.location, self.location, distance))
        
        if distance > 30:
            return 0
        
        hit = float(0)
        all = float(0)
        oth_hashes = object.variations_hashes()
        
        for hash in hashes:
            if any(x for x in oth_hashes if x.find(hash) > -1):
                hit += 1
            all += 1
            
        if hit/all*100 > 20:
            print(object.name)
            print("found hashes: "+str(len(oth_hashes)))
            print(oth_hashes)
                
        try:
            return hit/all*100
        except:
            return 0
    
    def get_similar(self):
        all_objects = Item.objects.filter(is_open=True).exclude(pk=self.pk)#,is_lost=not self.is_lost)
        
        this_hashes = self.variations_hashes()
        
        similar = ()
        
        for object in all_objects:
            similarity_rate = self.compare_hashes(this_hashes,object)
            if similarity_rate > 20:
                similar += ([object,similarity_rate,],)
                
        return similar


class Service(models.Model):
    name = models.CharField(_("Name"), max_length=128, blank=False)
    last_update = models.DateTimeField(_("Uploaded date"), auto_now=True)
    last_attempt = models.DateTimeField(_("Uploaded date"), auto_now=True)

    def get_status(self):
        if self.last_update != self.last_attempt:
            return "API_ERROR"

        if (self.last_update-timezone.now()).days > -3:
            return "API_UPTODATE"
        else:
            return "API_OUTDATED"

    def get_count(self):
        return len(Item.objects.filter(source=self.name))
