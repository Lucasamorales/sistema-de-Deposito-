
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
import re
from pymongo import MongoClient


Builder.load_file('ope/ope.kv')
class OpeWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        client = MongoClient()
        self.db=client.silverpos
        self.stocks = self.db.stocks


        self.cart=[]
        self.cant=[]
        self.total=0.00
    
    def logout(self):
        self.parent.parent.current = 'scrn_si'
        
    def update_purchases(self):
        pcode = self.ids.code_input.text
        products_container= self.ids.products
        
        target_code= self.stocks.find_one({'product_code':pcode})
        if target_code == None:
            pass
        else:
            details = BoxLayout(size_hint_y=None, height= 30, pos_hint={"top":1})
            products_container.add_widget(details)

            code= Label(text=pcode,size_hint_x=.2,color=(.06,.45,.45,1))
            name= Label(text=target_code['product_name'],size_hint_x=.3,color=(.06,.45,.45,1))
            Cant = Label(text="1",size_hint_x=.1,color=(.06,.45,.45,1))
            desc= Label(text="0.00",size_hint_x=.1,color=(.06,.45,.45,1))
            precio= Label(text=target_code['product_price'],size_hint_x=.1,color=(.06,.45,.45,1))
            total= Label(text="0.00",size_hint_x=.2,color=(.06,.45,.45,1))
            details.add_widget(code)
            details.add_widget(name)
            details.add_widget(Cant)
            details.add_widget(desc)
            details.add_widget(precio)
            details.add_widget(total)

            #update preview
            pname= name.text
            

            pprice = float(precio.text)
            pqty = str(1)
            self.total += pprice
            purchase_total = '`\n\nTotal\t\t\t\t\t\t\t\t'+str(self.total) 
            self.ids.cur_product.text = pname
            self.ids.cur_price.text = str(pprice)
            preview= self.ids.receipt_preview
            prev_text = preview.text 
            _prev = prev_text.find('`')

            if _prev >0:
                prev_text=prev_text[:_prev]
            ptarget= -1
            for i,c in enumerate(self.cart):
                if c == pcode:
                    ptarget = i   

            if ptarget >=0:
                pqty= self.cant[ptarget]+1
                self.cant[ptarget]=pqty
                expr ='%s\t\tx\d\t'%(pname)
                rexpr = pname+'\t\tx'+str(pqty)+'\t'
                nu_text = re.sub(expr,rexpr,prev_text)
                preview.text = nu_text + purchase_total
            else: 
                self.cart.append(pcode)
                self.cant.append(1)
                nu_preview = '\n'.join([prev_text,pname+'\t\tx'+pqty+'\t\t'+str(pprice),purchase_total])
                preview.text = nu_preview
            
            self.ids.desc_input.text ='0.00'
            self.ids.desc_perc_input.text ='0.00'
            self.ids.cant_input.text= str(pqty)
            self.ids.price_input.text =str(pprice)
            self.ids.Total_input.text =str(pprice)
class OpeApp(App):
    def build(self):
        return OpeWindow()


if __name__ == "__main__":
    oa = OpeApp()
    oa.run()
