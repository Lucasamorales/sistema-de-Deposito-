

from turtle import width
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from collections import OrderedDict
from pymongo import MongoClient
from utils.datatable import DataTable
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner 
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.uix.label import Label
from datetime import datetime
import hashlib

Builder.load_file('admin/admin.kv')
class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint =(.7,.7)

class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client = MongoClient()
        db= client.silverpos
        self.users = db.users
        self.products = db.stocks
        self.notify = Notify()
        


        #Display users
        content = self.ids.scrn_contents
        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

        #Display products 
        product_scrn = self.ids.scrn_product_contents
        products = self.get_products()
        prod_table = DataTable(table=products)
        product_scrn.add_widget(prod_table)

    def logout(self):
        self.parent.parent.current = 'scrn_si'

    def add_Product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        crud_code=TextInput(hint_text='Codigo de Producto',multiline=False)
        crud_name=TextInput(hint_text='Nombre del producto',multiline=False)
        crud_weight=TextInput(hint_text='Peso del producto',multiline=False)
        crud_stock=TextInput(hint_text='producto en stock',multiline=False)
        crud_sold=TextInput(hint_text='producto vendido',multiline=False)
        crud_order=TextInput(hint_text='pedido del producto',multiline=False)
        crud_purchase=TextInput(hint_text='ultima compra de producto',multiline=False)
        crud_sumbit= Button(text='Agregar', 
                            size_hint_x=None,
                            width=100,
                            on_release= lambda x: self.add_product(
                                crud_code.text,
                                crud_name.text,
                                crud_weight.text,
                                crud_stock.text,
                                crud_sold.text,
                                crud_order.text,
                                crud_purchase.text
                            ))
                            
        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_weight)
        target.add_widget(crud_stock)
        target.add_widget(crud_sold)
        target.add_widget(crud_order)
        target.add_widget(crud_purchase)
        target.add_widget(crud_sumbit)

    def add_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first=TextInput(hint_text='Nombre',multiline=False)
        crud_last=TextInput(hint_text='Apellido',multiline=False)
        crud_user=TextInput(hint_text='nombre de usuario',multiline=False)
        crud_pwd=TextInput(hint_text='Contraseña',multiline=False)
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

    def update_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first=TextInput(hint_text='Nombre')
        crud_last=TextInput(hint_text='Apellido')
        crud_user=TextInput(hint_text='nombre de usuario')
        crud_pwd=TextInput(hint_text='Contraseña')
        crud_des = Spinner(text='Operator', values=['Operator','Administrator'])
        crud_sumbit= Button(text='Actualizar', 
                            size_hint_x=None,
                            width=100,
                            on_release= lambda x:self.update_user(
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

    def update_Product_fields(self):
            target = self.ids.ops_fields_p
            target.clear_widgets()

            crud_code=TextInput(hint_text='Codigo de Producto',multiline=False)
            crud_name=TextInput(hint_text='Nombre del producto',multiline=False)
            crud_weight=TextInput(hint_text='Peso del producto',multiline=False)
            crud_stock=TextInput(hint_text='producto en stock',multiline=False)
            crud_sold=TextInput(hint_text='producto vendido',multiline=False)
            crud_order=TextInput(hint_text='pedido del producto',multiline=False)
            crud_purchase=TextInput(hint_text='ultima compra de producto',multiline=False)
            crud_sumbit= Button(text='Actualizar', 
                                size_hint_x=None,
                                width=100,
                                on_release= lambda x: self.update_product(
                                    crud_code.text,
                                    crud_name.text,
                                    crud_weight.text,
                                    crud_stock.text,
                                    crud_sold.text,
                                    crud_order.text,
                                    crud_purchase.text
                                ))
                                
            target.add_widget(crud_code)
            target.add_widget(crud_name)
            target.add_widget(crud_weight)
            target.add_widget(crud_stock)
            target.add_widget(crud_sold)
            target.add_widget(crud_order)
            target.add_widget(crud_purchase)
            target.add_widget(crud_sumbit)

    def remove_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_user= TextInput(hint_text='Usuario',multiline=False)
        crud_sumbit= Button(text='Eliminar', 
                            size_hint_x=None,
                            width=100,
                            on_release= lambda x:self.remove_user(crud_user.text))

        target.add_widget(crud_user)
        target.add_widget(crud_sumbit)
    
    def remove_Product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_code= TextInput(hint_text='Codigo de Producto',multiline=False)
        crud_sumbit= Button(text='Eliminar', 
                            size_hint_x=None,
                            width=100,
                            on_release= lambda x:self.remove_product(crud_code.text))

        target.add_widget(crud_code)
        target.add_widget(crud_sumbit)

    def remove_user(self,user):
        content = self.ids.scrn_contents
        content.clear_widgets()
        if user == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b] Nombre de usuario requerido[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            target_user = self.users.find_one({'user_name':user})
            if target_user == None:
                self.notify.add_widget(Label(text='[color=#FF0000][b] Nombre de usuario invalido [/b][/color]',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,1)
            else:
                 self.users.delete_one({'user_name':user})

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

    def remove_product(self,code):
        content=self.ids.scrn_product_contents
        content.clear_widgets()
        if code == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b] Codigo requerido[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            target_code = self.products.find_one({'product_code':code})
            if target_code == None:
                self.notify.add_widget(Label(text='[color=#FF0000][b] Codigo invalido [/b][/color]',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,1)
            else:
                self.products.delete_one({'product_code': code})

        prodz= self.get_products()
        stocktable=DataTable(table=prodz)
        content.add_widget(stocktable)

    def update_user(self,first,last,user,pwd,des):
        target = self.ids.scrn_contents
        target.clear_widgets()
        pwd = hashlib.sha256(pwd.encode()).hexdigest()

        if user == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b] Todos Los campos son requeridos[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
           user= self.users.find_one({'user_name':user})
           if user == None:
            self.notify.add_widget(Label(text='[color=#FF0000][b] Nombre de usuario invalido[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
           else:
                if first =='':
                    first= user['first_name']
                if last =='':
                    last= user['last_name']
                if pwd =='':
                    pwd= user['password']

                self.users.update_one({'user_name':user},{'$set':{'first_name':first,'last_name':last,
                                'user_name':user,'password':pwd,'designation':des,'date':datetime.now()}})

        users = self.get_users()
        usertable =DataTable(table=users)
        target.add_widget(usertable)  
               
    def update_product(self,code,name,weight,stock,sold,order,purchase):
        content= self.ids.scrn_product_contents
        content.clear_widgets()
        if code=='':
            self.notify.add_widget(Label(text='[color=#FF0000][b] codigo requerido[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            target_code = self.products.find_one({'product_code': code})
            if target_code == None:
                self.notify.add_widget(Label(text='[color=#FF0000][b] Codigo Invalido[/b][/color]',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,1)
            else:
                if name=='':
                    name = target_code['product_name']
                if weight=='':
                    weight = target_code['product_weight']
                if stock=='':
                    stock= target_code['in_stock']
                if sold=='':
                    sold = target_code['sold']
                if purchase=='':
                    purchase = target_code['last_purchase']
                if order=='':
                    order = target_code['order']

                self.products.update_one({'product_code':code},{'$set':{'product_code':code,'product_name':name,
                                            'product_weight':weight,'in_stock':stock,
                                            'product_sold':sold,'product_order':order,
                                            'last_purchase':purchase}})
        prodz= self.get_products()
        stocktable=DataTable(table=prodz)
        content.add_widget(stocktable)

    def add_user(self, first,last,user,pwd,des):
        content = self.ids.scrn_contents
        content.clear_widgets()
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        if first == '' or last == '' or user == '' or pwd == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b] Todos Los campos son requeridos[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:

            self.users.insert_one({'first_name':first,
                                    'last_name':last,
                                    'user_name':user,
                                    'password':pwd,
                                    'designation':des,
                                    'date':datetime.now()})


        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)
    def killswitch(self,dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def add_product(self,code,name,weight,stock,sold,order,purchase):
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        if code =='' or name =='' or weight =='' or stock =='' or order =='':
            self.notify.add_widget(Label(text='[color=#FF0000][b] Todos Los campos son requeridos[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            self.products.insert_one({'product_code':code,'product_name':name,
                                        'product_weight':weight,'in_stock':stock,
                                        'product_sold':sold,'product_order':order,
                                        'last_purchase':purchase})

        prodz=self.get_products()
        stocktable = DataTable(table=prodz)
        content.add_widget(stocktable)

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
            try:
                sold.append(product['sold'])
            except KeyError:
                sold.append('')
            try:
                order.append(product['order'])
            except KeyError:
                order.append('')
            try:
                last_purchase.append(product['last_purchase'])
            except KeyError:
                last_purchase.append('')

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
