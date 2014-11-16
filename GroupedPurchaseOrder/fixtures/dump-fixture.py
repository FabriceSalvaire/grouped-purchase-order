####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) 2014 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import json

from django.core import serializers
from django.db.models import Model

####################################################################################################

from GroupedPurchaseOrder import models

####################################################################################################

model_list = []
for item in models.__dict__.values():
    try:
        if issubclass(item, Model):
            model_list.append(item)
    except:
        pass

model_list.sort(key=lambda x:x.__name__)

json_string = '['
for model_class in model_list:
    json_string += serializers.serialize("json", model_class.objects.all())[1:-1]
    if model_class!= model_list[-1]:
        json_string += ','
json_string += ']'

with open('demo.json', 'w') as f:
    data = json.loads(json_string)
    json.dump(data, f, indent='  ')

####################################################################################################
# 
# End
# 
####################################################################################################
