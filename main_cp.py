#!/usr/bin/python
# Copyright 2015 Telefonica Investigacion y Desarrollo, S.A.U
#
# This file is part of FlaskContextProvider.
#
# FlaskContextProvider is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# FlaskContextProvider is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Orion Context Broker. If not, see http://www.gnu.org/licenses/.

import sys
import tools.ContextProvider as CP
import tools.DataManager as DM
from providers.bikerenting import bikerenting as bikerenting


def get_data_example(_id, _type, max_cache_time):
    """
        This is an example function which shows you how to manage the data in order
        to add it properly to the Context Provider response. This example uses the
        DataManager class but if you don't feel at ease with it and you prefer to build
        the response on your own, verify that your response matches with the example
        response.

        The function will be called one time for each entity that the Context Provider
        will be asked to, so take into account that this functions have to give response
        for just one entity, in addition to this, you don't have to take care about patterned
        ids, there are a previous method that processes them and returns non patterned ids.

            :param _id: entity_id
            :param _type: entity_type
            :param max_cache_time: max_cache_time
            :rtype : list
    """

    dm = DM.Entity()
    dm.entity_add(_id, _type)

    # CREATE AN ATTRIBUTE LIST
    dm.attribute.attribute_add('attrib_name_A', 'attrib_type_A', value='attrib_value_A')
    dm.attribute.attribute_add('attrib_name_B', 'attrib_type_B', value='attrib_value_B')

    # ADD A METADATA LIST TO AN ATTRIBUTE
    dm.attribute.metadata.metadata_add('metadata_name1', 'metadata_type1', value='metadata_value1')
    dm.attribute.metadata.metadata_add('metadata_name2', 'metadata_type2', value='metadata_value2')
    dm.attribute.add_metadatas_to_attrib('attrib_name_A')
    dm.attribute.metadata.metadata_list_purge()

    # ADD AN ATTRIBUTE LIST TO THE ENTITY
    data_response = dm.add_attributes_to_entity(_id)

    # SET THE ENTITY CACHE LIFETIME
    l_time = max_cache_time

    response = [data_response, l_time]

    return response

args = ['-r']
for arg in sys.argv:
    if arg[0] == '-' and arg not in args:
        print "%s is not a valid argument" % arg
        exit(-1)

reg = True
if '-r' in sys.argv and sys.argv[2].lower() in ['0', 'false', 'off', 'no']:
    reg = False

CP.ContextProvider(bikerenting=bikerenting.get_data, r=reg)
