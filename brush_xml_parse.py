#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import xml.sax
 
class BrushHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.single_brush_info_dct = {}
        self.single_brush_info_list = [] 
        self.all_brush_info_list = []

    def get_parse_result(self):
        #print len(self.all_brush_info_list)
        return self.all_brush_info_list
 
    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "command":
            #print "*****command*****"
            #print attributes.keys()
            mtype = attributes["type"]
            if mtype == "2":
                mid = attributes["id"]
                timestamp = attributes["timestamp"]
                documentid = attributes["documentid"]
                pageid = attributes["pageid"]
                color = attributes["color"]
                linesize = attributes["linesize"]

                self.single_brush_info_dct["type"] = mtype
                self.single_brush_info_dct["id"] = mid
                self.single_brush_info_dct["timestamp"] = timestamp
                self.single_brush_info_dct["documentid"] = documentid
                self.single_brush_info_dct["pageid"] = pageid
                self.single_brush_info_dct["color"] = color
                self.single_brush_info_dct["linesize"] = linesize
                #print mid, mtype, timestamp, documentid, pageid, color, linesize
            elif mtype == "3":
                mid = attributes["id"]
                removed = attributes["removed"]
                timestamp = attributes["timestamp"]
                documentid = attributes["documentid"]
                pageid = attributes["pageid"]

                self.single_brush_info_dct["type"] = mtype
                self.single_brush_info_dct["id"] = mid
                self.single_brush_info_dct["removed"] = removed
                self.single_brush_info_dct["timestamp"] = timestamp
                self.single_brush_info_dct["documentid"] = documentid
                self.single_brush_info_dct["pageid"] = pageid
                #print mid, mtype, removed, timestamp, documentid, pageid
                

    def endElement(self, tag):
        if tag == "command":
            self.single_brush_info_dct["brush_area_list"] =  self.single_brush_info_list
            self.all_brush_info_list.append(self.single_brush_info_dct)
            self.single_brush_info_list = []
            self.single_brush_info_dct = {}

            
    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "p":
            self.p = content
            if content.find(",") != -1:
                #print content, len(content)
                self.single_brush_info_list.append(content)
           
  
if ( __name__ == "__main__"):
   
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
 
    # 重写 ContextHandler
    Handler = BrushHandler()
    parser.setContentHandler( Handler )
    
    parser.parse("anno.xml")
    all_brush = Handler.get_parse_result()
    for i in all_brush:
        print i
