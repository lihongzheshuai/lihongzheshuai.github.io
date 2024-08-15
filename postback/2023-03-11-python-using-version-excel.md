---
title: Python实战-生成版本排期Excel
tags: [python]
date: 2023-03-11 21:13:24 +0800
comments: true
author: onecoder
---

最新工作很忙，需要做一个整体项目和版本排期的大表。幸亏之前学了一点Python，尝试用Python处理数学，生成所需要表格。主要用到了pandas、xlsxwriter等工具包。代码并不具备什么通用性，可能写的也很啰嗦，不过好在也算用Python为自己做了一项实用的工作。下面代码中，一些工作信息隐去了。

<!--more-->

```python
from datetime import datetime

import openpyxl
import pandas as pd

file_path = "./resources/系统版本计划统筹表.xlsx"
input_sheet_name = "3-项目版本统筹"
out_file_path = "./resources/"
out_sheet_name = "版本排布-总览"
out_sheet_name_trans_withoutxc = "**"
col_name_product_trade = "**"
col_name_product_clear = "**"
col_name_product_delivery = "**"
col_name_product_supervise = "**"
col_name_product_member = "**"
col_name_product_otc = "**"
col_name_product_data = "**"
col_name_product_risk_management = "**"
col_name_product_other = "**"
col_name_product_line = "**"
col_name_index = "**"
col_name_project_name = "**"
col_name_project_simple_name = "**"
col_name_project_approval_state = "**"
col_name_project_stage = "**"
col_name_if_xc = "**"
col_name_expected_time = "**"
col_name_time_line = "**"
col_name_online_time = "**"
col_name_if_decision = "**"
col_name_explanation = "**"
col_name_system_trade = "**"
col_name_system_clear = "**"
col_name_system_clear_old = "**"
col_name_system_delivery = "**"
col_name_system_supervise = "**"
col_name_system_otc = "**"
col_name_system_member = "**"
col_name_system_index = "**"
col_name_system_dwr = "**"
col_name_system_risk_management = "**"
col_name_system_data = "**"
col_name_system_data_old = "**"
col_name_system_website = "**"
col_name_system_deliveryapp = "**"
col_name_system_bean2 = "**"
col_name_new_project_count = "**"


# 读取Excel
def read_excel(file_path, sheet_name):
    workbook = openpyxl.load_workbook(filename=file_path, data_only=True)
    return pd.read_excel(workbook, sheet_name=sheet_name, engine='openpyxl')


# 定义输出表格
def create_out_frame():
    columns = [col_name_product_trade, col_name_product_clear, col_name_product_delivery, col_name_product_supervise,
               col_name_product_member, col_name_product_otc, col_name_product_data,
               col_name_product_other, col_name_time_line, col_name_online_time, col_name_system_trade,
               col_name_system_clear, col_name_system_clear_old, col_name_system_delivery, col_name_system_supervise,
               col_name_system_otc, col_name_system_member, col_name_system_index, col_name_system_dwr,
               col_name_system_risk_management, col_name_system_data, col_name_system_data_old, col_name_system_website,
               col_name_system_deliveryapp, col_name_system_bean2
               ]
    result = pd.DataFrame(columns=columns)
    return result


def fill_the_frame(source_df, result_frame):
    # 1.对读入数据按照上线时间排序
    source_df.sort_values(by=col_name_online_time, inplace=True)
    # 2.插入上线时间列
    result_frame[col_name_online_time] = pd.to_datetime(source_df[col_name_online_time],
                                                        errors='coerce').dt.strftime('%m/%d')
    result_frame[col_name_time_line] = pd.to_datetime(source_df[col_name_online_time],
                                                      errors='coerce').dt.strftime('%Y-%m')
    # 3.插入版本号列
    result_frame[col_name_system_trade] = source_df[col_name_system_trade]
    result_frame[col_name_system_clear] = source_df[col_name_system_clear]
    result_frame[col_name_system_clear_old] = source_df[col_name_system_clear_old]
    result_frame[col_name_system_delivery] = source_df[col_name_system_delivery]
    result_frame[col_name_system_supervise] = source_df[col_name_system_supervise]
    result_frame[col_name_system_otc] = source_df[col_name_system_otc]
    result_frame[col_name_system_member] = source_df[col_name_system_member]
    result_frame[col_name_system_index] = source_df[col_name_system_index]
    result_frame[col_name_system_dwr] = source_df[col_name_system_dwr]
    result_frame[col_name_system_risk_management] = source_df[col_name_system_risk_management]
    result_frame[col_name_system_data] = source_df[col_name_system_data]
    result_frame[col_name_system_data_old] = source_df[col_name_system_data_old]
    result_frame[col_name_system_website] = source_df[col_name_system_website]
    result_frame[col_name_system_deliveryapp] = source_df[col_name_system_deliveryapp]
    result_frame[col_name_system_bean2] = source_df[col_name_system_bean2]
    result_frame[col_name_project_approval_state] = source_df[col_name_project_approval_state]

    # 4.填充项目列
    for row in source_df.itertuples():
        cur_product_line_name = row.产品线
        result_frame.at[(row.Index,), cur_product_line_name] = row.简称


# 按行合并
def merge_row(row_num, format, df, sheet):
    time_line_row = df.iloc[row_num]
    start_cell_index = 1
    end_cell_index = 1
    last_cell_val = None
    total_count = len(time_line_row)
    for cell in time_line_row:
        # 刚合并过
        if start_cell_index == end_cell_index:
            if end_cell_index == total_count:
                # 处理最后一个单元格
                sheet.write(row_num, end_cell_index, cell, format)
            else:
                end_cell_index += 1
                last_cell_val = cell
            continue
        # 如果值相同，索引+1
        if cell == last_cell_val:
            # 处理最后一个单元格
            if end_cell_index == total_count:
                sheet.merge_range(row_num, start_cell_index + 1, row_num, end_cell_index + 1,
                                  cell,
                                  format)
            else:
                end_cell_index += 1
        else:
            # 单一值单元格
            if end_cell_index - start_cell_index <= 1:
                sheet.write(row_num, start_cell_index + 1, last_cell_val, format)
                if end_cell_index == total_count:
                    sheet.write(row_num, end_cell_index + 1, cell, format)
            else:
                sheet.merge_range(row_num, start_cell_index + 1, row_num, end_cell_index,
                                  last_cell_val,
                                  format)
            start_cell_index = end_cell_index
            end_cell_index += 1
        last_cell_val = cell


def write_result(writer, result_frame):
    result_frame.dropna(axis=0, how="all", inplace=True)
    result_frame.dropna(axis=1, how="all", inplace=True)
    # 总览
    _trans_to_sheet(result_frame, writer, out_sheet_name, True)
    # 交易
    trade_frame = result_frame.drop(axis=1,
                                    columns=[col_name_product_clear, col_name_product_delivery,
                                             col_name_product_supervise,
                                             col_name_product_member, col_name_product_data, col_name_product_otc,
                                             col_name_product_other])
    trade_frame.dropna(inplace=True, how="any", subset=[col_name_product_trade])
    _trans_to_sheet(trade_frame, writer, "1-交易", False)
    # 清算
    trade_frame = result_frame.drop(axis=1,
                                    columns=[col_name_product_trade, col_name_product_delivery,
                                             col_name_product_supervise,
                                             col_name_product_member, col_name_product_data, col_name_product_otc,
                                             col_name_product_other])
    trade_frame.dropna(inplace=True, how="any", subset=[col_name_product_clear])
    _trans_to_sheet(trade_frame, writer, "2-清算", False)
    # 交割
    trade_frame = result_frame.drop(axis=1,
                                    columns=[col_name_product_trade, col_name_product_clear,
                                             col_name_product_supervise,
                                             col_name_product_member, col_name_product_data, col_name_product_otc,
                                             col_name_product_other])
    trade_frame.dropna(inplace=True, how="any", subset=[col_name_product_delivery])
    _trans_to_sheet(trade_frame, writer, "3-交割", False)
    # 监查
    trade_frame = result_frame.drop(axis=1,
                                    columns=[col_name_product_trade, col_name_product_clear,
                                             col_name_product_delivery,
                                             col_name_product_member, col_name_product_data, col_name_product_otc,
                                             col_name_product_other])
    trade_frame.dropna(inplace=True, how="any", subset=[col_name_product_supervise])
    _trans_to_sheet(trade_frame, writer, "4-监查", False)
    # 场外
    trade_frame = result_frame.drop(axis=1,
                                    columns=[col_name_product_trade, col_name_product_clear,
                                             col_name_product_delivery,
                                             col_name_product_member, col_name_product_data, col_name_product_supervise,
                                             col_name_product_other])
    trade_frame.dropna(inplace=True, how="any", subset=[col_name_product_otc])
    _trans_to_sheet(trade_frame, writer, "5-场外", False)
    # 会服
    trade_frame = result_frame.drop(axis=1,
                                    columns=[col_name_product_trade, col_name_product_clear,
                                             col_name_product_delivery,
                                             col_name_product_otc, col_name_product_data, col_name_product_supervise,
                                             col_name_product_other])
    trade_frame.dropna(inplace=True, how="any", subset=[col_name_product_member])
    _trans_to_sheet(trade_frame, writer, "6-会服", False)
    # 数据
    trade_frame = result_frame.drop(axis=1,
                                    columns=[col_name_product_trade, col_name_product_clear,
                                             col_name_product_delivery,
                                             col_name_product_otc, col_name_product_member, col_name_product_supervise,
                                             col_name_product_other])
    trade_frame.dropna(inplace=True, how="any", subset=[col_name_product_data])
    _trans_to_sheet(trade_frame, writer, "7-数据", False)
    # 其他
    trade_frame = result_frame.drop(axis=1,
                                    columns=[col_name_product_trade, col_name_product_clear,
                                             col_name_product_delivery,
                                             col_name_product_otc, col_name_product_member, col_name_product_supervise,
                                             col_name_product_data])
    trade_frame.dropna(inplace=True, how="any", subset=[col_name_product_other])
    _trans_to_sheet(trade_frame, writer, "8-其他", False)


def _trans_to_sheet(df, writer, sheet_name, is_all):
    final_result_frame = df.drop(axis=1, columns=[col_name_project_approval_state])
    ori_trans_frame = df.transpose(copy=True)
    ori_trans_frame.set_index(ori_trans_frame.index, append=True, inplace=True)
    # 5.转置输出
    result_frame_trans = final_result_frame.transpose(copy=True)
    # 加一列索引列
    result_frame_trans.set_index(result_frame_trans.index, append=True, inplace=True)
    # 6.处理时间线列-合并单元格
    result_frame_trans.to_excel(writer, sheet_name=sheet_name, header=False)
    out_sheet = writer.sheets[sheet_name]
    sheet_table = out_sheet.table
    row_counts = len(sheet_table)
    # 交替设置行样式
    odd_row_format = writer.book.add_format({
        "border": 1,
        "fg_color": "D9D9D9",
        "border_color": "808080",
        "font_name": "微软雅黑",
        "bold": True,
        "align": "center",
        "valign": "vcenter",
    })
    even_row_format = writer.book.add_format({
        "border": 1,
        "fg_color": "F2F2F2",
        "border_color": "808080",
        "font_name": "微软雅黑",
        "bold": True,
        "align": "center",
        "valign": "vcenter",
    })
    project_cell_format = writer.book.add_format({
        "border": 1,
        "fg_color": "4F81BD",
        "border_color": "808080",
        "font_name": "Times New Roman",
        "font_color": "white",
        "bold": True,
        "align": "center",
        "valign": "vcenter",
        "text_wrap": True
    })
    new_project_cell_format = writer.book.add_format({
        "border": 1,
        "fg_color": "00B050",
        "border_color": "808080",
        "font_name": "Times New Roman",
        "font_color": "white",
        "bold": True,
        "align": "center",
        "valign": "vcenter",
        "text_wrap": True
    })
    version_cell_format = writer.book.add_format({
        "border": 1,
        "fg_color": "BFBFBF",
        "border_color": "808080",
        "font_name": "Times New Roman",
        "font_color": "black",
        "bold": True,
        "align": "center",
        "valign": "vcenter",
        "text_wrap": True
    })
    merge_cell_format = writer.book.add_format({
        "bold": True,
        "border": 2,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "1F497D",
        "font_color": "white",
        "font_name": "Times New Roman",
        "border_color": "808080"
    })
    time_line_row_num = 0
    online_time_row_num = 0
    if is_all:
        time_line_row_num = 8
        online_time_row_num = 9
    else:
        time_line_row_num = 1
        online_time_row_num = 2
    for row_index in range(row_counts):
        table_row = sheet_table[row_index]
        cur_cell_format = None
        if row_index % 2 == 0:
            out_sheet.set_row(row=row_index, height=30, cell_format=even_row_format)
        else:
            out_sheet.set_row(row=row_index, height=30, cell_format=odd_row_format)

        if time_line_row_num <= row_index <= online_time_row_num:
            cur_cell_format = merge_cell_format
        elif row_index > online_time_row_num:
            cur_cell_format = version_cell_format
        for col_idx in table_row:
            if col_idx == 0:
                continue
            if col_idx == 1:
                value = ori_trans_frame.index[row_index][0]
                cur_idx_format = None
                if row_index % 2 == 0:
                    cur_idx_format = even_row_format
                else:
                    cur_idx_format = odd_row_format
                out_sheet.write(row_index, col_idx, value, cur_idx_format)
            else:
                if row_index < time_line_row_num:
                    cur_cell_format = project_cell_format
                    if_new_project = ori_trans_frame.iloc[row_counts, col_idx - 2]
                    if if_new_project == "待立项":
                        cur_cell_format = new_project_cell_format
                value = ori_trans_frame.iloc[row_index, col_idx - 2]
                out_sheet.write(row_index, col_idx, value, cur_cell_format)

    # 合并项目、系统和时间轴
    if is_all:
        out_sheet.merge_range(0, 0, time_line_row_num - 1, 0,
                              "项目",
                              merge_cell_format)
    else:
        out_sheet.write(0, 0, "项目", merge_cell_format)
    out_sheet.merge_range(time_line_row_num, 0, online_time_row_num, 1,
                          "时间轴",
                          merge_cell_format)
    out_sheet.merge_range(online_time_row_num + 1, 0, row_counts - 1, 0,
                          "系统",
                          merge_cell_format)
    merge_row(time_line_row_num, format=merge_cell_format, sheet=out_sheet, df=result_frame_trans)
    merge_row(online_time_row_num, format=merge_cell_format, sheet=out_sheet, df=result_frame_trans)
    # 7.设置样式
    # 列宽
    out_sheet.set_column(0, 0, width=5)
    out_sheet.set_column(1, 1, width=20)


def write_detail_table(source_df, writer):
    # 定义输出的DataFrame
    result_frame = create_out_frame()
    # 遍历填写数据1
    fill_the_frame(source_df, result_frame)
    # 输出结果
    write_result(writer, result_frame)



def run():
    currentDateAndTime = datetime.now()
    time_str = currentDateAndTime.strftime("%Y%m%d(%H%M)")
    out_file = out_file_path + time_str + "版本排布.xlsx"
    writer = pd.ExcelWriter(out_file,
                            engine='xlsxwriter',
                            date_format='yyyy-dd-mm')
    # 读取源数据到DataFrame
    source_df = read_excel(file_path, input_sheet_name)
    # 输出明细数据
    write_detail_table(source_df, writer)
    # 输出统计数据
    # write_statistic_tables(source_df, writer)
    writer.close()


run()


```
