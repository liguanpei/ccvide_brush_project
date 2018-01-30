#/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import xml.sax

from chat_xml_parse import ChatHandler

class GengeeChatClass():
    def __init__(self, resource_path):
        self.resource_path = resource_path 
        self.all_brush_info = {}

    def load_resource(self):
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    
        Handler = ChatHandler()
        parser.setContentHandler( Handler )
    
        parser.parse(self.resource_path + "/chat1.xml")
        all_document = Handler.get_parse_result()
        return all_document
            
            
