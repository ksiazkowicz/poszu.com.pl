from django.shortcuts import render_to_response, HttpResponseRedirect

from database.models import Item
from database import logic

from django.template import RequestContext

from web.forms import NewItemForm
import uuid


def home(request, template="index.html"):
    """
    Displays homepage
    """
    lost_objects = Item.objects.filter(is_lost=True).order_by('-upload_date')
    
    return render_to_response(template, locals(), context_instance=RequestContext(request))


def show_item(request, item_hash, template="item_view.html"):
    """
    Displays item
    """
    try:
        item = Item.objects.filter(hash=item_hash,is_open=True)[0]
    except:
        return HttpResponseRedirect("/")
    
    return render_to_response(template, locals(), context_instance=RequestContext(request))


def admin_item(request, item_hash, auth_hash, template="item_view.html"):
    """
    Displays item
    """
    try:
        item = Item.objects.filter(hash=item_hash,is_open=True)[0]
    except:
        return HttpResponseRedirect("/")
        
    if item.auth_hash() == auth_hash:
        is_admin = True
    else:
        return HttpResponseRedirect("/")
    
    if request.method == 'GET':
        try:
            if int(request.GET.get('close')) == 1:
                is_success = int(request.GET.get('success'))
                logic.close_event(item_hash,is_success)
                if is_success == 1:
                    return HttpResponseRedirect("/success/?finished=1")
                else:
                    return HttpResponseRedirect("/failure/")
        except:
            pass
    
    similar = sorted(item.get_similar(),key=lambda x: -x[1])
    
    return render_to_response(template, locals(), context_instance=RequestContext(request))


def new_lost_form(request, template="lost_form.html"):
    # get form for adding new posts
    form = NewItemForm(is_lost=True)

    if request.method == 'POST':
        multiple = ""
        x = 1
        while True:
            data = request.POST.get("description["+str(x)+"]")
                
            if data != None:
                multiple = multiple + data + ";"
                x += 1
            else:
                break
                
        request.POST['description'] = multiple[:-1]
        request.POST['hash'] = uuid.uuid1().hex
        
        form = NewItemForm(request.POST,request.FILES,is_lost=True)
        
        if form.is_valid():
            newpost = form.save()
            if newpost:
                logic.spam_challenge(newpost.hash)
            return HttpResponseRedirect("/success/")

    return render_to_response(template, locals(), context_instance=RequestContext(request))


def success(request, template="success.html"):
    is_closed = request.GET.get("finished")
    
    return render_to_response(template, locals(), context_instance=RequestContext(request))


def failure(request, template="failure.html"):
    return render_to_response(template, locals(), context_instance=RequestContext(request))


def new_found_form(request, template="lost_form.html"):
    # get form for adding new posts
    form = NewItemForm(is_lost=False)

    if request.method == 'POST':
        multiple = ""
        x = 1
        while True:
            data = request.POST.get("description["+str(x)+"]")
                
            if data != None:
                multiple = multiple + data + ";"
                x += 1
            else:
                break
                
        request.POST['description'] = multiple[:-1]
        request.POST['hash'] = uuid.uuid1().hex
        
        form = NewItemForm(request.POST,request.FILES,is_lost=False)
        if form.is_valid():
            newpost = form.save()
            if newpost:
                logic.spam_challenge(newpost.hash)
            return HttpResponseRedirect("/success/")

    return render_to_response(template, locals(), context_instance=RequestContext(request))

