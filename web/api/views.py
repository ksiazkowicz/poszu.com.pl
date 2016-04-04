# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.views.decorators.csrf import csrf_exempt

from rest_framework import serializers
from django.conf import settings

import os
import random

import logic, distance

from database.models import Item
import json

"""
@api_view(['GET'])
def get_item(request, itemId):
    c = request.GET.get("c","").split(",")
    item = Item.objects.filter(pk=itemId)[0]
    
    if len(c) > 1:         
        # parse coordinates
        lat = float(c[0])
        lon = float(c[1])
    
    if not item:
        return Response(status=500)
    
    results = logic.get_items_dictionary(item,details=True)
    
    if len(c) > 1:
        results['distance'] = distance.calculate((lat,lon),(item.loc_latitude,item.loc_longitude))*1000
    
    return Response(results)
    

@csrf_exempt
@api_view(['GET','POST'])
"""

@csrf_exempt
@api_view(['POST'])
def get_items(request):
    """if request.method == 'GET':
        # get all objects
        objects = Item.objects.all()
        
        # get coordinates
        c = request.GET.get("c","").split(",")
        
        # LOL WYDAJNOSC XDDD
        if len(c) > 1:         
            # parse coordinates
            lat = float(c[0])
            lon = float(c[1])
            
            # iterate through objects list
            for item in objects:
                if distance.calculate((lat,lon),(item.loc_latitude,item.loc_longitude)) > float(1.5):
                    objects = objects.exclude(pk=item.pk)

        # filter by name
        name_filter = request.GET.get("name","")
        if name_filter != "":
            objects = objects.filter(name__contains=name_filter)
            
        # filter by month
        month_filter = request.GET.get("month",0)
        if month_filter != 0 and month_filter < 13:
            objects = objects.filter(upload_date__month=month_filter)
        
        # filter by day
        day_filter = request.GET.get("day",0)
        if day_filter != 0 and day_filter < 31:
            objects = objects.filter(upload_date__day=day_filter)

        results = []
        for item in objects:
            result = logic.get_items_dictionary(item)
            
            if len(c) > 1:
                result['distance'] = distance.calculate((lat,lon),(item.loc_latitude,item.loc_longitude))*1000
            
            # append
            results.append(result)

        return Response({"results": results})
    
    el"""
    if request.method == 'POST':
        content = request.POST['_content']
        
        # try to parse json, if failed, return error 500
        try:
            content = json.loads(content)
        except:
            return Response(status=200)
        
        coordinates = content['coordinates'].split(',')
        
        date = ""
        try:
            date=content['upload_date']
        except:
            pass
            
        description = ""
        try:
            description=content["description"]
        except:
            pass
            
        _item = Item.objects.create(name=content['name'],email=content['email'],upload_date=date,loc_latitude=coordinates[0],loc_longitude=coordinates[1],description=description,is_lost=content['is_lost'])
            
        photo_file = None
        try:
            photo_file = base64.b64decode(content['photo'])
        except:
            pass
            
        if photo_file:
            file = open(settings.BASE_DIR + os.path.normpath("/static/item/photos/"+str(random.getrandbits(128))+".jpg"),"wb")
            file.write(photo_file)
            _item.photo = file
            file.close
        
        return Response({"id": _item.pk, "name": _item.name, "date": _item.upload_date})