#/usr/bin/env python
#-*- coding: utf-8 -*-

import json

class CCVideoBrushClass():
    def __init__(self, output_filename):
        self.output_filename = output_filename 

    def export_data(self, data):
        try:
            with open(self.output_filename, 'w') as json_file:
                json_file.write(json.dumps(data))

        except Exception, e:
            print str(e)
            
            
             
             
    
