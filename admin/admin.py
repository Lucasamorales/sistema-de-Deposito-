

from turtle import width
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from collections import OrderedDict
from pymongo import MongoClient
from utils.datatable import DataTable
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner 
from datetime import datetime

class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client = MongoClient()
        db= client.silverpos
        self.users = db.users
        self.products = db.stocks

        
        #print(self.get_products())

        #Display users
        content = self.ids.scrn_cotents
        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

        #Display products 
        product_scrn = self.ids.scrn_product_content
        products = self.get_products()
        prod_table = DataTable(table=products)
        product_scrn.add_widget(prod_table)

    def add_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first=TextInput(hint_text='Nombre')
        crud_last=TextInput(hint_text='Apellido')
        crud_user=TextInput(hint_text='nombre de usuario')
        crud_pwd=TextInput(hint_text='Contraseña')
        crud_des = Spinner(text='Operator', values=['Operator','Administrator'])
        crud_sumbit= Button(text='Agregar', 
                            size_hint_x=None,
                            width=100,
                            on_release= lambda x:self.add_user(
                                        crud_first.text,
                                        crud_last.text,
                                        crud_user.text,
                                        crud_pwd.text,
                                        crud_des.text))


        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_sumbit)

    def add_user(self, first,last,user,pwd,des):
        content = self.ids.scrn_cotents
        content.clear_widgets()

        self.users.insert_one({'first_name':first,
                                'last_name':last,
                                'user_name':user,
                                'password':pwd,
                                'designation':des,
                                'date':datetime.now()})


        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)


    def get_users(self):
        Client = MongoClient()
        db= Client.silverpos
        users=db.users
        _users= OrderedDict()
        _users['first_names']={}
        _users['last_names']={}
        _users['user_names']={}
        _users['passwords']={}
        _users['designations']={}
           

        first_names=[]
        last_names=[]
        user_names=[]
        passwords=[]
        designations=[]

        for user in users.find():
            first_names.append(user['first_name'])
            last_names.append(user['last_name'])
            user_names.append(user['user_name'])
            pwd=user['password']
            if len(pwd) > 10:
                pwd = pwd[:10] + '...'
            passwords.append(pwd)
            designations.append(user['designation'])

        users_lenght = len(first_names)
        idx=0
        while idx < users_lenght:
            _users['first_names'][idx]= first_names[idx]
            _users['last_names'][idx]= last_names[idx]
            _users['user_names'][idx]= user_names[idx]
            _users['passwords'][idx]= passwords[idx]
            _users['designations'][idx]= designations[idx]

            idx+=1

        return _users
    
    def get_products(self):
        Client = MongoClient()
        db= Client.silverpos
        products=db.stocks
        _stocks= OrderedDict()
        _stocks['product_code']={}
        _stocks['product_name']={}
        _stocks['product_weight']={}
        _stocks['in_stock']={}
        _stocks['sold']={}
        _stocks['order']={}
        _stocks['last_purchase']={}
            
        product_code=[]
        product_name=[]
        product_weight=[]
        in_stock=[]
        sold=[]
        order=[]
        last_purchase=[]

        for product in products.find():
            product_code.append(product['product_code'])
            name=product['product_name']
            if len(name)>10:
                name= name[:10] + '...'
            product_name.append(name)
            product_weight.append(product['product_weight'])
            in_stock.append(product['in_stock'])
            sold.append(product['sold'])
            order.append(product['order'])
            last_purchase.append(product['last_purchase'])

        products_lenght = len(product_code)
        idx=0
        while idx < products_lenght:
            _stocks['product_code'][idx]= product_code[idx]
            _stocks['product_name'][idx]= product_name[idx]
            _stocks['product_weight'][idx]= product_weight[idx]
            _stocks['in_stock'][idx]= in_stock[idx]
            _stocks['sold'][idx]= sold[idx]
            _stocks['order'][idx]= order[idx]
            _stocks['last_purchase'][idx]= last_purchase[idx]

            idx+=1
            
        return _stocks
   
    def change_screen(self, instance):
        if instance.text == 'Administrar Productos':
            self.ids.scrn_mngr.current = 'scrn_product_content'
        elif instance.text == 'Administrar Usuarios':
            self.ids.scrn_mngr.current = 'scrn_content'
        else: 
            self.ids.scrn_mngr.current = 'scrn_analysis'
    
class AdminApp(App):
    def build(self):
        return AdminWindow()


if __name__ == "__main__":
    oa = AdminApp()
    oa.run()
