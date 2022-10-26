from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class OpeWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_purchases(self):
        code = self.ids.code_input.text
        products_container= self.ids.products
        if code == "1234":
            details = BoxLayout(size_hint_y=None, height= 30, pos_hint={"top":1})
            products_container.add_widget(details)


            code= Label(text=code,size_hint_x=.2,color=(.06,.45,.45,1))
            name= Label(text="primer producto",size_hint_x=.3,color=(.06,.45,.45,1))
            Cant = Label(text="1",size_hint_x=.1,color=(.06,.45,.45,1))
            desc= Label(text="0.00",size_hint_x=.1,color=(.06,.45,.45,1))
            precio= Label(text="0.00",size_hint_x=.1,color=(.06,.45,.45,1))
            total= Label(text="0.00",size_hint_x=.2,color=(.06,.45,.45,1))
            details.add_widget(code)
            details.add_widget(name)
            details.add_widget(Cant)
            details.add_widget(desc)
            details.add_widget(precio)
            details.add_widget(total)

            #update preview
            pname= "primer producto"
            pprice = 1.00
            preview= self.ids.receipt_preview
            prev_text = preview.text 
            _prev = prev_text.find('`')
            if _prev >0:
                prev_text=prev_text[:_prev]
            purchase_total = '`\n\nTotal\t\t\t\t\t\t\t\t0.00'   
            nu_preview = '\n'.join([prev_text,pname+'\t\t\t\t'+str(pprice),purchase_total])
            preview.text = nu_preview
            
class OpeApp(App):
    def build(self):
        return OpeWindow()


if __name__ == "__main__":
    oa = OpeApp()
    oa.run()
