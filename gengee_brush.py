#/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import xml.sax

from xml_parse import BrushHandler

class GengeeBrushClass():
    def __init__(self, resource_path):
        self.resource_path = resource_path 
        self.all_brush_info = {}

    def load_resource(self):
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    
        Handler = BrushHandler()
        parser.setContentHandler( Handler )
    
        parser.parse(self.resource_path + "/anno.xml")
        all_brush = Handler.get_parse_result()
        for i in all_brush:
            print i
        return all_brush
            
            
