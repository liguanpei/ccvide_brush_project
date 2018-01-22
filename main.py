#/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import ast
from gengee_brush import GengeeBrushClass
from gengee_document import GengeeDocumentClass
from ccvideo_brush import CCVideoBrushClass

def get_rgb_color(red, green, blue):
    color = 0
    color |= red << 16
    color |= green << 8
    color |= blue
    return color

def generate_cc_json_data(first_docid, all_gengee_brush_list, all_gengee_document_dct):
    all_json_data = {}
    all_json_data["success"] = True
    all_json_data["msg"] = "操作成功"
    
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

    print all_gengee_document_dct
    for brush in all_gengee_brush_list:
        tmp_brush = {}
        data = {}
        mtype = brush["type"]
        if mtype == "2":
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
            data["type"] = mtype
            
            drawl = []
            x_y = {}
            width = int(data["width"])
            height = int(data["height"])
            for area in brush["brush_area_list"]:
                x, y = area.split(",")
                x_y["x"] = round(float(x) / width, 4)
                x_y["y"] = round(float(y) / height, 4)
                drawl.append(x_y)

            data["draw"] = drawl
            tmp_brush["data"] = data

        draw.append(tmp_brush)
        
            
    meta["draw"] = draw
    all_json_data["meta"] = meta
    
    
    return all_json_data
    

def main():
    # 所有画笔相关信息
    genBrush = GengeeBrushClass("./media")
    all_gengee_brush_list = genBrush.load_resource()

    # 画笔对应的文档信息
    genDocument = GengeeDocumentClass("./media")
    all_gengee_document_dct = genDocument.load_resource()

    first_docid = ""
    ccBrush = CCVideoBrushClass("./meta.json")
    if all_gengee_brush_list:
        first_docid = all_gengee_brush_list[0]["documentid"]
    data = generate_cc_json_data(first_docid, all_gengee_brush_list, all_gengee_document_dct)
    print data
    ccBrush.export_data(data)

if __name__ == '__main__':
    main()
