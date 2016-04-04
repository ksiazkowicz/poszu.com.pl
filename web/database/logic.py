# -*- coding: utf-8 -*-
from django.core.mail import EmailMessage
from models import Item
from django.template import loader, Context

def spam_challenge(hash):
    item = Item.objects.filter(hash=hash)[0]
    body = loader.get_template('mail/challenge_accepted.txt')
    
    if not item:
        return
    
    context = Context({
        'url': "http://poszu.com.pl/item/" + hash + "/auth/" + str(item.auth_hash()) + "/",
        'name': item.name
    })
    
    e = EmailMessage(u'Przyjęto zgłoszenie  [' + item.name + ']', body.render(context), "poszucompel <donotreply@poszu.com.pl>",[item.email])
    e.send()
    
def spam_digest(hash):
    item = Item.objects.filter(hash=hash)[0]
    body = loader.get_template('mail/digest.txt')
    
    if not item:
        return
    
    context = Context({
        'url': "http://poszu.com.pl/item/" + hash + "/auth/" + str(item.auth_hash()) + "/",
        'name': item.name
    })
    
    e = EmailMessage(u'Aktualizacja zgłoszenia  [' + item.name + ']', body.render(context), "poszucompel <donotreply@poszu.com.pl>",[item.email])
    e.send()
    
def goodbyeT_T(hash):
    item = Item.objects.filter(hash=hash)[0]
    body = loader.get_template('mail/farewell_letter.txt')
    
    if not item:
        return
    
    context = Context({})
    
    e = EmailMessage(u'Zlecenie zostało zamknięte [' + item.name + ']', body.render(context), "poszucompel <donotreply@poszu.com.pl>",[item.email])
    e.send()
    
def close_event(hash,is_success):
    item = Item.objects.filter(hash=hash)[0]
    item.close_event(is_success)
    goodbyeT_T(hash)