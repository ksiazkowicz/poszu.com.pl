import base64
from database.models import Item

from sorl.thumbnail import get_thumbnail

def get_photo_base64(photo,is_thumbnail=False):
    '''
    Converts value from Django's ImageField to base64 string.
    '''
    
    if is_thumbnail:
        image = get_thumbnail(photo.file, '200x200', crop='center', quality=99)
    else:
        image = photo.file
        
    # initialize empty value
    image_base64 = None
    
    # try to encode string
    try:
        image_base64 = base64.b64encode(image.read())
    except:
        # failed, pass
        pass
    
    # return string
    return image_base64

def get_items_dictionary(item,details=False):
    if not item:
        return None
    
    result = {}
    result['id'] = item.pk
    result['name'] = item.name
    
    if details:
        result['description'] = item.description
        #result['user_id'] = item.user
        result['coordinates'] = str(item.loc_latitude) + "," + str(item.loc_longitude)
        
             
    # if photo, append base64
    if item.photo:
        result['photo'] = get_photo_base64(item.photo,is_thumbnail=not details)
                
    result['date'] = item.upload_date
    result['is_lost'] = item.is_lost
    
    return result