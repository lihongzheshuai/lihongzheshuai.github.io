---
title: Python瞎学瞎用
tags: [python]
date: 2023-02-01 23:00:24 +0800
comments: true
author: onecoder
---
很久没有更新博客了，有年底很忙的原因，也有在学习用Python瞎鼓捣点什么的因素，其实我并没有停止学习。

学了一段时间Python，本身有开发基础，总想着用Python鼓捣点什么我自己用的上的东西，所以从去年11月开始，就开始学习研究Python GUI编程，现在每天学学写写，走走停停，也算有所积累吧。

当然，还没什么见的人的成果，不过也可以考虑把阶段性代码更新上来，权当记录和一乐了。

2023年，祝自己好运，心想事成。

<!--more-->

```python
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox

from project.data.data_handler import ProjectHandler
from project.gui.const_ui import ui_const
from project.gui.ui_dialog import NewProjectDialog, ProjectDetailDialog


class Main_UI(Tk):

    def __init__(self):
        super().__init__()
        self._cur_index = 0
        self._main_table = None
        self._view_pro_button = None
        self._edit_button = None
        self._ph = ProjectHandler()

    @property
    def main_table(self):
        return self._main_table

    @main_table.setter
    def main_table(self, table):
        self._main_table = table

    @property
    def cur_index(self):
        return self._cur_index

    @cur_index.setter
    def cur_index(self, index):
        self._cur_index = index

    # 加载主页面
    def do_load(self):
        # 加载中窗口信息
        self.load_main_info()
        # 加载菜单
        self.load_menu()
        # 加载表格
        self.load_project_table()
        # 加载按钮
        self.load_buttons()

    # 设置按钮
    def load_buttons(self):
        # 设置button_frame
        button_frame = Frame(self)
        button_frame.pack(pady=10, fill=X)
        # 设置按钮
        view_project_button = tk.Button(button_frame, text="查看项目详情", takefocus=TRUE, state=DISABLED,
                                        command=self.view_project_detail_command)
        new_project_button = tk.Button(button_frame, text="新增项目", takefocus=TRUE,
                                       command=self.new_project_command)
        remove_project_button = tk.Button(button_frame, text="删除项目", takefocus=TRUE, state=DISABLED,
                                          command=self.delete_project_command)
        self._del_pro_button = remove_project_button
        self._view_pro_button = view_project_button
        remove_project_button.pack(ipadx=10, padx=10, side=RIGHT)
        new_project_button.pack(ipadx=10, side=RIGHT)
        view_project_button.pack(ipadx=10, padx=10, side=RIGHT)

    # 弹出新建项目窗口
    def open_new_project_page(self):
        print("Open new project dialog")
        inputDialog = NewProjectDialog()
        self.wait_window(inputDialog)
        return inputDialog._project

    def open_project_detail_page(self, item):
        project_detail_dialog = ProjectDetailDialog(item["values"])
        self.wait_window(project_detail_dialog)

    # 查看项目详情
    def view_project_detail_command(self):
        item_id = self._main_table.selection()[0]
        item = self._main_table.item(item_id)
        self.open_project_detail_page(item)

    def delete_project_command(self):
        confirm = messagebox.askokcancel('提示', '确定删除项目吗，项目所有数据将被清除？')
        if confirm:
            selected_list = self._main_table.selection()
            print("Delete projects:", selected_list)
            self._ph.delete_projects_by_code(selected_list)
            for item in selected_list:
                self._main_table.delete(item)
        else:
            print("Cancel deleting project.")

    def new_project_command(self):
        p = self.open_new_project_page()
        self._insert_one_project(p)
        self._cur_index += 1

    def load_main_info(self):
        self.title(ui_const.MAIN_TITLE)
        self.geometry(ui_const.WINDOW_SIZE)

    # 加载数据
    def load_table_data(self):
        table_data = self._ph.get_all()
        for i in range(len(table_data.projects_in_tuple)):  # 写入数据
            p = table_data.projects[i]
            self._insert_one_project(p)

    def refresh_table(self):
        self.delete_all_table_data()
        self.load_table_data()

    def _insert_one_project(self, p):
        if p is None:
            print("No project to insert.")
            return
        self._main_table.insert('', END, p.id,
                                values=(p.name, p.code, p.manager, p.state, p.id
                                        ), tags=(p.id, p.code))
        self._cur_index += 1

    # 根据列表条目选定情况，改变按钮状态
    def change_button_state(self, event):
        selected_list = self._main_table.selection()
        selected_item_num = len(selected_list)
        if selected_item_num == 0:
            self._del_pro_button["state"] = DISABLED
            self._view_pro_button["state"] = DISABLED
        elif selected_item_num == 1:
            self._view_pro_button["state"] = NORMAL
            self._del_pro_button["state"] = NORMAL
        else:
            self._view_pro_button["state"] = DISABLED
            self._del_pro_button["state"] = NORMAL

    # 加载表格
    def load_project_table(self):
        # 创建table_frame
        table_frame = Frame(self, pady=20)
        table_frame.pack(fill=BOTH)
        # 创建滚动条
        table_scroll_y = Scrollbar(table_frame)
        table_scroll_y.pack(side=RIGHT, fill=Y)
        # 创建表格
        table = ttk.Treeview(table_frame, columns=("name", "code", "manager", "status"), show='headings'
                             , yscrollcommand=table_scroll_y.set, height=25)
        # 设置表格样式
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=('微软雅黑', 11))
        style.configure("Treeview", font=('微软雅黑', 11), rowheight=25)
        # 设置表格表头
        table.heading("name", text="项目名称")
        table.heading("code", text="项目编号")
        table.heading("manager", text="项目经理")
        table.heading("status", text="项目状态")
        table.column("name", width=450, anchor='center')
        table.column("code", width=250, anchor='center')
        table.column("manager", width=150, anchor='center')
        table.column("status", width=150, anchor='center')
        table.bind("<<TreeviewSelect>>", self.change_button_state)
        table.pack(padx=10, fill=BOTH)
        self._main_table = table
        table_scroll_y.config(command=table.yview)
        # 加载表格数据
        self.load_table_data()

    # 删除表格中所有数据
    def delete_all_table_data(self):
        for i in self._main_table.get_children():
            self._main_table.delete(i)

    # 加载菜单
    def load_menu(self):
        # 创建菜单Frame
        table_frame = Frame(self, pady=20)
        table_frame.pack(fill=BOTH)


if __name__ == "__main__":
    print("abc\n")
    print("abc\\n".splitlines(False))
    print("IN " + str(tuple(["sd"])))

```
