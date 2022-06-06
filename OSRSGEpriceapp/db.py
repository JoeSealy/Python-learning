#item information display
"""""""""
rs_item_info_list = Listbox(app, height=8, width=50)
rs_item_info_list.grid(row =3, column=0, columnspan = 3, 
rowspan=2, pady = 20, padx=20)
#scrollbar set up for item list
rs_item_info_scrollbar = Scrollbar(app)
rs_item_info_scrollbar.grid(row=3,column=3)
rs_item_info_list.configure(yscrollcommand=rs_item_info_scrollbar.set)
rs_item_info_scrollbar.configure(command=rs_item_info_list.yview)
"""""""""