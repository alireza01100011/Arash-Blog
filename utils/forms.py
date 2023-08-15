from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget , CheckboxInput

formats = {
    'image' : ['jpg' , 'jpeg' , 'png' , 'webp' , 'gif' , 'svg'],
    'audio' : ['mp3' , 'oog'  , 'aac' , 'wav'] ,
    'video' : ['mp4' , 'wmv' , 'webm'],
    'exe' : ['exe' , 'apk' , 'bash'],
    'compressed' : ['zip' , 'rar' , 'gz' , 'tar' , '7z'],
    'document' : ['txt' , 'log' , 'pdf' , 'html' , 'xls' , 'xlsx' , 'odt' , 'PPT' , 'PPTX']
}

class MultipleCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

def _get_fields(obj):
    fields = [_ for _ in obj._fields]
    return [getattr(obj , _ ) for _ in fields]