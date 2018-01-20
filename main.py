#/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
from gengee_brush import GengeeBrushClass
from ccvideo_brush import CCVideoBrushClass

def generate_cc_json_data(first_docid, all_gengee_brush_list):
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

    for brush in all_gengee_brush_list:
        tmp_brush = {}
        mtype = brush["type"]
        if mtype == "2":
            tmp_brush["time"] = round(ast.literal_eval(brush["time"]))
            #tmp_brush["docName"] = 
             

    meta["draw"] = draw
    all_json_data["meta"] = meta
    
    
    return all_json_data
    

def main():
    # 所有画笔相关信息
    genBrush = GengeeBrushClass("./media")
    all_gengee_brush_list = genBrush.load_resource()

    # 画笔对应的文档信息
    genBrush = GengeeBrushClass("./media")
    all_gengee_fileinfo_list = genBrush.load_resource()

    first_docid = ""
    ccBrush = CCVideoBrushClass("./meta.json")
    if all_gengee_brush_list:
        first_docid = all_gengee_brush_list[0]["documentid"]
    data = generate_cc_json_data(first_docid, all_gengee_brush_list)
    ccBrush.export_data(data)

if __name__ == '__main__':
    main()
