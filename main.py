#/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import ast
from gengee_brush import GengeeBrushClass
from gengee_document import GengeeDocumentClass
from gengee_chat import GengeeChatClass
from ccvideo_brush import CCVideoBrushClass

def get_rgb_color(red, green, blue):
    color = 0
    color |= red << 16
    color |= green << 8
    color |= blue
    return color

def generate_cc_json_data(first_docid, all_gengee_brush_list, all_gengee_document_dct, all_gengee_chat_lst):
    all_json_data = {}
    all_json_data["success"] = True
    all_json_data["msg"] = "操作成功"
    

    # TODU: 模板信息具体场景具体拼接
    datas = {}
    template = {}
    template["name"] = "模板五"
    template["id"] = 5
    template["type"] = 5
    template["status"] = 1
    template["desc"] = "视频，文档，聊天，问答"
    template["iconPath"] = "ltab5"
    template["pdfView"] = 1
    template["chatView"] = 1
    template["qaView"] = 1
    datas["template"] = template
    all_json_data["datas"] = datas

    meta = {}
    draw = []
    # 开始直播时的 clear_up 事件
    first_packet = {}
    first_packet["time"] = 0
    first_packet["docName"] = "0"
    first_packet["pageNum"] = 0
    first_data = {}
    first_data["docid"] = first_docid
    first_data["page"] = 0
    first_data["type"] = 8
    first_packet["data"] = first_data
    draw.append(first_packet) 

    # add draw Event
    for brush in all_gengee_brush_list:
        tmp_brush = {}
        data = {}
        mtype = brush["type"]
        if mtype == "2": # 展视画笔 --> CC普通画笔
            tmp_brush["time"] = int(round(ast.literal_eval(brush["timestamp"])))
            tmp_brush["docName"] = all_gengee_document_dct[brush["documentid"]]["name"]
            tmp_brush["pageNum"] = brush["pageid"]
            data["alpha"] = 1
            
            tmp_color = brush["color"][1:7]
            tmp_color_re = re.findall(r'(.{2})', tmp_color)
            data["color"] = get_rgb_color(int(tmp_color_re[0], 16), int(tmp_color_re[1], 16), int(tmp_color_re[2], 16))
            data["docid"] = brush["documentid"]
            data["height"] = all_gengee_document_dct[brush["documentid"]]["height"]
            data["width"] = all_gengee_document_dct[brush["documentid"]]["width"]
            data["page"] = brush["pageid"]
            data["thickness"] = brush["linesize"]
            data["type"] = int(mtype)
            
            drawl = []
            x_y = {}
            width = int(data["width"])
            height = int(data["height"])
            for area in brush["brush_area_list"]:
                x, y = area.split(",")
                x_y["x"] = round(float(x) / width, 4)
                x_y["y"] = round(float(y) / height, 4)
                drawl.append(x_y)
                x_y = {}

            data["draw"] = drawl
            tmp_brush["data"] = data

        elif mtype == "6": # 展视矩形 --> CC矩形 type:3
            tmp_brush["time"] = int(round(ast.literal_eval(brush["timestamp"])))
            tmp_brush["docName"] = all_gengee_document_dct[brush["documentid"]]["name"]
            tmp_brush["pageNum"] = brush["pageid"]
            data["alpha"] = 1
            tmp_color = brush["color"][1:7]
            tmp_color_re = re.findall(r'(.{2})', tmp_color)
            data["color"] = get_rgb_color(int(tmp_color_re[0], 16), int(tmp_color_re[1], 16), int(tmp_color_re[2], 16))
            data["docid"] = brush["documentid"]
            data["drawid"] = "2018-01-30" # TODU
            data["width"] = all_gengee_document_dct[brush["documentid"]]["width"]
            data["height"] = all_gengee_document_dct[brush["documentid"]]["height"]
            data["page"] = brush["pageid"]
            data["thickness"] = brush["linesize"]
            data["type"] = 3
            
            draw1 = {}
            width = int(data["width"])
            height = int(data["height"])
            xy_str = brush["brush_area_list"][0]
            wh_str = brush["brush_area_list"][1]
            x, y = xy_str.split(",")
            w, h = wh_str.split(",")
            draw1["x"] = round(float(x) / width, 4)
            draw1["y"] = round(float(y) / height, 4)
            draw1["width"] = round(float(w) / width, 4)
            draw1["height"] = round(float(h) / height, 4)

            data["draw"] = drawl
            tmp_brush["data"] = data

        elif mtype == "5": # 展视圆或椭圆 --> CC圆 type:4
            tmp_brush["time"] = int(round(ast.literal_eval(brush["timestamp"])))
            tmp_brush["docName"] = all_gengee_document_dct[brush["documentid"]]["name"]
            tmp_brush["pageNum"] = brush["pageid"]
            data["alpha"] = 1
            tmp_color = brush["color"][1:7]
            tmp_color_re = re.findall(r'(.{2})', tmp_color)
            data["color"] = get_rgb_color(int(tmp_color_re[0], 16), int(tmp_color_re[1], 16), int(tmp_color_re[2], 16))
            data["docid"] = brush["documentid"]
            data["drawid"] = "2018-01-30" # TODU
            data["width"] = all_gengee_document_dct[brush["documentid"]]["width"]
            data["height"] = all_gengee_document_dct[brush["documentid"]]["height"]
            data["page"] = brush["pageid"]
            data["thickness"] = brush["linesize"]
            data["type"] = 4
            
            draw1 = {}
            width = int(data["width"])
            height = int(data["height"])
            xy_str = brush["brush_area_list"][0]
            wh_str = brush["brush_area_list"][1]
            x, y = xy_str.split(",")
            w, h = wh_str.split(",")
            draw1["x"] = round(float(x) / width, 4)
            draw1["y"] = round(float(y) / height, 4)
            draw1["widthRadius"] = round(float(w) / width, 4)
            draw1["heightRadius"] = round(float(h) / height, 4)

            data["draw"] = drawl
            tmp_brush["data"] = data

        elif mtype == "8": # 展视直线 --> CC直线 type:2
            tmp_brush["time"] = int(round(ast.literal_eval(brush["timestamp"])))
            tmp_brush["docName"] = all_gengee_document_dct[brush["documentid"]]["name"]
            tmp_brush["pageNum"] = brush["pageid"]
            data["alpha"] = 1
            tmp_color = brush["color"][1:7]
            tmp_color_re = re.findall(r'(.{2})', tmp_color)
            data["color"] = get_rgb_color(int(tmp_color_re[0], 16), int(tmp_color_re[1], 16), int(tmp_color_re[2], 16))
            data["docid"] = brush["documentid"]
            data["drawid"] = "2018-01-30" # TODU
            data["width"] = all_gengee_document_dct[brush["documentid"]]["width"]
            data["height"] = all_gengee_document_dct[brush["documentid"]]["height"]
            data["page"] = brush["pageid"]
            data["thickness"] = brush["linesize"]
            data["type"] = 2
            
            drawl = []
            x_y = {}
            width = int(data["width"])
            height = int(data["height"])
            xy_str = brush["brush_area_list"][0]
            wh_str = brush["brush_area_list"][1]
            x, y = xy_str.split(",")
            end_x, end_y = wh_str.split(",")
            x_y["x"] = round(float(x) / width, 4)
            x_y["y"] = round(float(y) / height, 4)
            x_y = {}
            drawl.append(x_y)
            x_y["x"] = round(float(end_x) / width, 4)
            x_y["y"] = round(float(end_y) / height, 4)
            drawl.append(x_y)

            data["draw"] = drawl
            tmp_brush["data"] = data


        elif mtype == "4": # 展视批注 --> CC批注 type: 5
            tmp_brush["time"] = int(round(ast.literal_eval(brush["timestamp"])))
            tmp_brush["docName"] = all_gengee_document_dct[brush["documentid"]]["name"]
            tmp_brush["pageNum"] = brush["pageid"]
            data["alpha"] = 1
            tmp_color = brush["color"][1:7]
            tmp_color_re = re.findall(r'(.{2})', tmp_color)
            data["color"] = get_rgb_color(int(tmp_color_re[0], 16), int(tmp_color_re[1], 16), int(tmp_color_re[2], 16))
            data["docid"] = brush["documentid"]
            data["drawid"] = "2018-01-30" # TODU
            data["width"] = all_gengee_document_dct[brush["documentid"]]["width"]
            data["height"] = all_gengee_document_dct[brush["documentid"]]["height"]
            data["page"] = brush["pageid"]
            data["thickness"] = 2
            data["type"] = 5
            
            draw1 = {}
            width = int(data["width"])
            height = int(data["height"])
            xy_str = brush["brush_area_list"][0]
            wh_str = brush["brush_area_list"][1]
            label_str = brush["brush_area_list"][2]
            x, y = xy_str.split(",")
            end_x, end_y = wh_str.split(",")
            draw1["x"] = round(float(x) / width, 4)
            draw1["y"] = round(float(y) / height, 4)
            draw1["width"] = round((float(end_x) - float(x)) / width, 4)
            draw1["height"] = round((float(end_y) - float(x)) / height, 4)
            draw1["label"] = label_str

            data["draw"] = draw1
            tmp_brush["data"] = data


        elif mtype == "3": # 展视撤回 --> CC撤回 type: 9, 0清屏
            tmp_brush["time"] = int(round(ast.literal_eval(brush["timestamp"])))
            tmp_brush["docName"] = all_gengee_document_dct[brush["documentid"]]["name"]
            tmp_brush["pageNum"] = brush["pageid"]
            data["docid"] = brush["documentid"]
            data["drawid"] = "2018-01-30" # TODU
            data["page"] = brush["pageid"]
            data["thickness"] = 5
            
            if brush["removed"] == "0":
                data["type"] = 0
            else:
                data["type"] = 9
            
            tmp_brush["data"] = data


        draw.append(tmp_brush)
        
            
    #print draw
    #draw.sort(key=lambda e: e.__getitem__('time'))
    meta["draw"] = draw

    # add pageChange Event
    pageChange = []
    for i, value in all_gengee_document_dct.iteritems():
        for lst in value["pageChange"]:
            pageChange.append(lst)

    pageChange.sort(key=lambda e: e.__getitem__('time'))
    meta["pageChange"] = pageChange

    # add chat Event
    meta["chatLog"] = all_gengee_chat_lst
    #print all_gengee_chat_lst
         

    all_json_data["meta"] = meta
    
    return all_json_data
    

def main():
    first_docid = ""
    all_gengee_brush_list = []
    all_gengee_document_dct = {}
    all_gengee_chat_lst = []

    try:
        # 获取展视所有画笔相关信息
        genBrush = GengeeBrushClass("./media")
        all_gengee_brush_list = genBrush.load_resource()
    except Exception, e:
        print str(e)

    try:
        # 获取画笔对应的文档信息
        genDocument = GengeeDocumentClass("./media")
        all_gengee_document_dct = genDocument.load_resource()
    except Exception, e:
        #print str(e)
        pass

    try:
        # 获取展视所有聊天
        genChat = GengeeChatClass("./media")
        all_gengee_chat_lst = genChat.load_resource()
    except Exception, e:
        #print str(e)
        pass

    try:
        first_docid = ""
        # 初始化CC画笔文件
        ccBrush = CCVideoBrushClass("./meta.json")
        if all_gengee_brush_list:
            first_docid = all_gengee_brush_list[0]["documentid"]
    except Exception, e:
        #print str(e)
        pass

    data = generate_cc_json_data(first_docid, all_gengee_brush_list, all_gengee_document_dct, all_gengee_chat_lst)
    #print data
    if data:
        print 'Export Success'
    ccBrush.export_data(data)

if __name__ == '__main__':
    main()
