
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout


class SigninWindow(BoxLayout):#pantalla de logeo 
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def validate_user(self):#validacion de Usuario 
        user = self.ids.username_field
        pwd = self.ids.pwd_field
        info= self.ids.info

        uname = user.text
        passw = pwd.text

        if uname == "" or passw == "":
            info.text= " [color=#FF0000]Se requiere un usuario o contraseña[/color]"
        else:
            if uname== "admin" and passw == "admin":
                info.text= "[color=#32CD32]Inicio de sesion exitosa![/color]"
            else:
                 info.text= " [color=#FF0000]Usuario o Contraseña Incorrectos[/color]"



class SigninApp(App): #displays the layout of the app 
    def build(self):
        return SigninWindow()


if __name__=="__main__":
    sa = SigninApp()
    sa.run()
