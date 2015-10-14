####################################################################################################
# 
# GroupedPurchaseOrder - A Django Application.
# Copyright (C) 2014 Fabrice Salvaire
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
# 
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
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

with open('db.json', 'w') as f:
    data = json.loads(json_string)
    json.dump(data, f, indent='  ')

####################################################################################################
# 
# End
# 
####################################################################################################
