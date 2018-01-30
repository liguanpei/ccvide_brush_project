#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import ast
import xml.sax
 
class DocumentHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.single_document_info_dct = {}
        self.all_document_info_dct = {}
        self.single_pagechange_info_list = []
        self.single_pagechange_info_dct = {}
        self.all_pagechange_info_dct = {}
        self.mid = ""
        self.name = ""

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
            self.name = name
            self.single_document_info_dct["timestamp"] = timestamp
        elif tag == "page":
            self.single_pagechange_info_dct = {}
            width = attributes["width"]
            height = attributes["height"]
            self.single_document_info_dct["width"] = width
            self.single_document_info_dct["height"] = height

            self.single_pagechange_info_dct["time"] = int(round(ast.literal_eval(attributes["starttimestamp"])))
            self.single_pagechange_info_dct["url"] = "http://image.csslcloud.net/image/docid/roomid/" + attributes["id"] + ".jpg" # 需要填充roomid和docid
            self.single_pagechange_info_dct["docId"] = self.mid
            self.single_pagechange_info_dct["docName"] = self.name
            self.single_pagechange_info_dct["docTotalPage"] = 100 # 此项展视不存在，可能没有意义
            self.single_pagechange_info_dct["pageNum"] = int(attributes["id"])
            self.single_pagechange_info_dct["encryptDocId"] = self.mid
            self.single_pagechange_info_dct["useSDK"] = False
            self.single_pagechange_info_dct["height"] = attributes["height"] 
            self.single_pagechange_info_dct["width"] = attributes["width"] 
            if attributes.has_key("title"):
                self.single_pagechange_info_dct["pageTitle"] = attributes["title"]
            else:
                self.single_pagechange_info_dct["pageTitle"] = ""

            self.single_pagechange_info_list.append(self.single_pagechange_info_dct)
            self.single_pagechange_info_dct = {}
            #print width, height
                

    def endElement(self, tag):
        if tag == "document":
            if self.all_pagechange_info_dct.has_key(self.mid):
                for v in self.all_pagechange_info_dct[self.mid]:
                    self.single_pagechange_info_list.append(v)
            self.single_document_info_dct["pageChange"] = self.single_pagechange_info_list
            self.all_document_info_dct[self.mid] =  self.single_document_info_dct
            self.all_pagechange_info_dct[self.mid] = self.single_pagechange_info_list
            self.mid = ""
            self.name = ""
            self.single_pagechange_info_list = []
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
        print value["pageChange"]
    
