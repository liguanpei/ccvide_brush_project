#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import xml.sax
 
class DocumentHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.single_document_info_dct = {}
        self.all_document_info_dct = {}
        self.mid = ""

    def get_parse_result(self):
        #print len(self.all_brush_info_list)
        return self.all_document_info_dct
 
    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "document":
            #print attributes.keys()
            mtype = attributes["type"]
            mid = attributes["id"]
            self.mid = mid
            name = attributes["name"]
            timestamp = attributes["timestamp"]
            #print mtype, mid, name, timestamp
            self.single_document_info_dct["type"] = mtype
            self.single_document_info_dct["id"] = mid
            self.single_document_info_dct["name"] = name
            self.single_document_info_dct["timestamp"] = timestamp
        elif tag == "page":
            #print attributes.keys()
            width = attributes["width"]
            height = attributes["height"]
            self.single_document_info_dct["width"] = width
            self.single_document_info_dct["height"] = height
            #print width, height
                

    def endElement(self, tag):
        if tag == "document":
            self.all_document_info_dct[self.mid] =  self.single_document_info_dct
            self.mid = ""
            self.single_document_info_dct = {}
            
  
if ( __name__ == "__main__"):
   
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
 
    # 重写 ContextHandler
    Handler = DocumentHandler()
    parser.setContentHandler( Handler )
    
    parser.parse("./media/record.xml")
    all_document = Handler.get_parse_result()
    for key, value in all_document.iteritems():
        print key, value
    
