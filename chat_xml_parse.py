#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import ast
import xml.sax
 
class ChatHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.all_chat_info_list = []
        self.single_chat_info_dct = {}
        self.all_chat_info_dct = {}
        self.mtype = ""

    def get_parse_result(self):
        #print len(self.all_brush_info_list)
        return self.all_chat_info_list
 
    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "ems":
            self.single_chat_info_dct["userName"] = attributes["sender"]
            self.single_chat_info_dct["userId"] = attributes["senderId"]
            self.single_chat_info_dct["userAvatar"] = ""
            if attributes.has_key("senderRole"):
                self.single_chat_info_dct["userRole"] = "publisher"
            else:
                self.single_chat_info_dct["userRole"] = "student"
            self.single_chat_info_dct["userCustomMark"] = ""
            
        elif tag == "chat":
            self.single_chat_info_dct["time"] = int(round(ast.literal_eval(attributes["timestamp"])))
            
                

    def endElement(self, tag):
        if tag == "chat":
            self.all_chat_info_list.append(self.single_chat_info_dct)
            self.single_chat_info_dct = {}

            
    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "ems":
            if content.strip():
                self.single_chat_info_dct["content"] = content
  
if ( __name__ == "__main__"):
   
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
 
    # 重写 ContextHandler
    Handler = ChatHandler()
    parser.setContentHandler( Handler )
    
    parser.parse("./media/chat1.xml")
    all_chat = Handler.get_parse_result()
    for i in all_chat:
        print i
