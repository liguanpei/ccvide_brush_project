#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import xml.sax
 
class BrushHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.single_brush_info_dct = {}
        self.single_brush_info_list = [] 
        self.all_brush_info_list = []
        self.mtype = ""

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
            if mtype == "2": # 普通画笔
                mid = attributes["id"]
                self.mtype = mtype
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

            elif mtype == "3": # 撤销
                mid = attributes["id"]
                self.mtype = mtype
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

            elif mtype == "6": #矩形
                mid = attributes["id"]
                self.mtype = mtype
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
                
            elif mtype == "5": # 圆或椭圆
                mid = attributes["id"]
                self.mtype = mtype
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

            elif mtype == "8": # 展视直线
                mid = attributes["id"]
                self.mtype = mtype
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

            elif mtype == "4": # 展视批注
                mid = attributes["id"]
                self.mtype = mtype
                timestamp = attributes["timestamp"]
                documentid = attributes["documentid"]
                pageid = attributes["pageid"]
                color = attributes["color"]
                fontsize = attributes["fontsize"]

                self.single_brush_info_dct["type"] = mtype
                self.single_brush_info_dct["id"] = mid
                self.single_brush_info_dct["timestamp"] = timestamp
                self.single_brush_info_dct["documentid"] = documentid
                self.single_brush_info_dct["pageid"] = pageid
                self.single_brush_info_dct["color"] = color
                self.single_brush_info_dct["fontsize"] = fontsize

    def endElement(self, tag):
        if tag == "command":
            if self.mtype == "2" or self.mtype == "3" or self.mtype == "6" or self.mtype == "5" or self.mtype == "8" or self.mtype == "4":
                self.single_brush_info_dct["brush_area_list"] =  self.single_brush_info_list
                self.all_brush_info_list.append(self.single_brush_info_dct)
                self.single_brush_info_list = []
                self.single_brush_info_dct = {}
                self.mtype = ""

            
    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "p":
            if content.find(",") != -1:
                #print content, len(content)
                self.single_brush_info_list.append(content)
        elif self.CurrentData == "ep":
                self.single_brush_info_list.append(content)
           
  
if ( __name__ == "__main__"):
   
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
 
    # 重写 ContextHandler
    Handler = BrushHandler()
    parser.setContentHandler( Handler )
    
    parser.parse("./media/anno.xml")
    all_brush = Handler.get_parse_result()
    for i in all_brush:
        print i
