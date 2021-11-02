import base64
import sys
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.clipboard import Clipboard
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from version import version

Config.set('kivy', 'exit_on_escape', '0')
Config.set('kivy', 'log_enable', '0')


class TitleLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(181 / 255, 0, 133 / 255, 0.8)
            Rectangle(pos=self.pos, size=self.size)


class encodeb64(GridLayout):
    def __init__(self, **kwargs):
        super(encodeb64, self).__init__(**kwargs)

        self.cols = 1
        self.screen_title = TitleLabel(text="Encoding in Base64", color=[250 / 255, 1, 0, 1])

        self.secondary = GridLayout()
        self.secondary.cols = 2
        self.encode_msg = Label(text="Enter data to encode: ", color=[1, 0, 0, 1])
        self.secondary.add_widget(self.encode_msg)
        self.original = TextInput(multiline=False, foreground_color=[1, 0, 0, 1],
                                  background_color=[0, 255 / 255, 228 / 255, 1], hint_text="Enter your data here!")
        self.add_widget(self.screen_title)
        self.secondary.add_widget(self.original)
        self.output = Label(text="Output: ", color=[0, 1, 0, 1])
        self.secondary.add_widget(self.output)
        self.out = TextInput(text="None", foreground_color=[0, 1, 0, 1], background_color=[0, 0, 0, 1], readonly=True,
                             multiline=False)
        self.secondary.add_widget(self.out)
        self.submit_button = Button(text='Encode!', color=[0, 0, 1, 1], background_color=[0, 1, 0, 1])
        self.submit_button.bind(on_press=self.callback)
        self.secondary.add_widget(self.submit_button)
        self.copy_button = Button(text="Copy Output To Clipboard")
        self.copy_button.bind(on_press=self.copy)
        self.secondary.add_widget(self.copy_button)
        self.back_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1], background_color=[0, 0, 1, 1])
        self.back_button.bind(on_press=self.back)
        self.secondary.add_widget(self.back_button)
        self.add_widget(self.secondary)

    def callback(self, instance):
        self.new = base64.b64encode(self.original.text.encode("utf-8"))
        self.out.text = self.new.decode("utf-8")
        if self.out.text == "":
            self.out.text = "None"

    def back(self, instance):
        self.out.text = "None"
        self.original.text = ""
        manager.transition.direction = "right"
        manager.transition.duration = 1
        manager.current = "b64menu"
        self.out.text = "None"
        self.original.text = ""

    def copy(self, instance):
        Clipboard.copy(self.out.text)


class decodeb64(GridLayout):
    def __init__(self, **kwargs):
        super(decodeb64, self).__init__(**kwargs)

        self.cols = 1
        self.screen_title = TitleLabel(text="Decoding in Base64", color=[250 / 255, 1, 0, 1])

        self.secondary = GridLayout()
        self.secondary.cols = 2
        self.encode_msg = Label(text="Enter data to decode: ", color=[1, 0, 0, 1])
        self.secondary.add_widget(self.encode_msg)
        self.original = TextInput(multiline=False, foreground_color=[1, 0, 0, 1],
                                  background_color=[0, 255 / 255, 228 / 255, 1], hint_text="Enter your data here!")
        self.add_widget(self.screen_title)
        self.secondary.add_widget(self.original)
        self.output = Label(text="Output: ", color=[0, 1, 0, 1])
        self.secondary.add_widget(self.output)
        self.out = TextInput(text="None", foreground_color=[0, 1, 0, 1], background_color=[0, 0, 0, 1], readonly=True,
                             multiline=False)
        self.secondary.add_widget(self.out)
        self.submit_button = Button(text='Decode!', color=[0, 0, 1, 1], background_color=[0, 1, 0, 1])
        self.submit_button.bind(on_press=self.callback)
        self.secondary.add_widget(self.submit_button)
        self.copy_button = Button(text="Copy Output To Clipboard")
        self.copy_button.bind(on_press=self.copy)
        self.secondary.add_widget(self.copy_button)
        self.back_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1], background_color=[0, 0, 1, 1])
        self.back_button.bind(on_press=self.back)
        self.secondary.add_widget(self.back_button)
        self.add_widget(self.secondary)

    def callback(self, instance):
        try:
            self.new = base64.b64decode(self.original.text.encode("utf-8"))
            self.out.text = self.new.decode("utf-8")
            if self.out.text == "":
                self.out.text = "None"
        except:
            layout = GridLayout(cols=1, padding=10)

            popupLabel = Label(text="Invalid Base 64...", color=[1, 0, 0, 1])
            closeButton = Button(text="Close", background_color=[1, 0, 0, 1], color=[1, 1, 1, 1])
            closeButton.bind(on_press=self.close_popup)

            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)

            self.popup = Popup(title='Error',
                               content=layout, size_hint=(None, None), size=(700, 800), separator_color=[1, 0, 0, 1])
            self.popup.open()
            Clock.schedule_once(self.popup.dismiss, 10)

    def back(self, instance):
        manager.transition.direction = "right"
        manager.transition.duration = 1
        manager.current = "b64menu"
        self.out.text = "None"
        self.original.text = ""

    def close_popup(self, instance):
        self.popup.dismiss()

    def copy(self, instance):
        Clipboard.copy(self.out.text)


class SuperTitle(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 1, 0.5)
            Rectangle(pos=self.pos, size=self.size)


class Menu(GridLayout):
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        Window.size = (900, 500)
        self.cols = 1
        self.loading_win = FloatLayout()
        self.splash_label = Label(text="Data Encoder", font_size=80, color=[218 / 255, 238 / 255, 0, 0.8])
        self.splash_version = Label(text="2021.1.6", font_size=40, color=[0, 1, 0, 1], pos=(0, -100))
        self.loading_win.add_widget(self.splash_label)
        self.loading_win.add_widget(self.splash_version)
        self.bar = ProgressBar(max=1000, size_hint_x=None, width=1400, pos=(200, -400))
        self.loading_win.add_widget(self.bar)
        self.add_widget(self.loading_win)
        self.load_bar = Clock.schedule_interval(self.up, 0.1)

    def go_to_binary(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = 1
        manager.current = "binmenu"

    def back(self, instance):
        self.exit_button.text = "The application is closing..."
        self.bin_button.disabled = True
        self.b64_button.disabled = True
        self.exit_button.disabled = True
        Clock.schedule_once(self.close_app, 2)

    def close_app(self, instance):
        sys.exit()

    def up(self, instance):
        if self.bar.value == 280:
            self.bar.value = 360
        elif self.bar.value == 620:
            self.bar.value = 1000
        elif self.bar.value == 1000:
            self.show_menu()
            Clock.unschedule(self.load_bar)
            return
        else:
            self.bar.value += 10

    def go_to_b64(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = 1
        manager.current = "b64menu"

    def show_menu(self):
        Window.maximize()
        self.clear_widgets()
        self.choose = SuperTitle(text="Choose a encoding/decoding method!")
        self.add_widget(self.choose)
        self.b64_button = Button(text='Base 64', color=[0, 0, 1, 1], background_color=[0, 1, 0, 0.5])
        self.b64_button.bind(on_press=self.go_to_b64)
        self.add_widget(self.b64_button)
        self.bin_button = Button(text='Binary', color=[0, 1, 0, 1], background_color=[0, 0, 0, 1])
        self.bin_button.bind(on_press=self.go_to_binary)
        self.add_widget(self.bin_button)
        self.exit_button = Button(text='Exit Application', color=[1, 1, 1, 1], background_color=[1, 0, 0, 1])
        self.exit_button.bind(on_press=self.back)
        self.add_widget(self.exit_button)


class b64_menu(GridLayout):
    def __init__(self, **kwargs):
        super(b64_menu, self).__init__(**kwargs)

        self.cols = 1
        self.menu_text = TitleLabel(text="Base 64 Menu")
        self.add_widget(self.menu_text)
        self.choosing = Label(text="Choose to encode or decode your data!")
        self.add_widget(self.choosing)
        self.encode_button = Button(text='Encode')
        self.encode_button.bind(on_press=self.encode)
        self.add_widget(self.encode_button)
        self.decode_button = Button(text='Decode')
        self.decode_button.bind(on_press=self.decode)
        self.add_widget(self.decode_button)
        self.exit_button = Button(text='Back')
        self.exit_button.bind(on_press=self.back)
        self.add_widget(self.exit_button)

    def back(self, instance):
        manager.transition.direction = "right"
        manager.transition.duration = 1
        manager.current = "menu"

    def decode(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = 1
        manager.current = "decb64"

    def encode(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = 1
        manager.current = "encb64"


class bin_menu(GridLayout):
    def __init__(self, **kwargs):
        super(bin_menu, self).__init__(**kwargs)

        self.cols = 1
        self.menu_text = TitleLabel(text="Binary Menu")
        self.add_widget(self.menu_text)
        self.choosing = Label(text="Choose to encode or decode your data!")
        self.add_widget(self.choosing)
        self.encode_button = Button(text='Encode')
        self.encode_button.bind(on_press=self.encode)
        self.add_widget(self.encode_button)
        self.decode_button = Button(text='Decode')
        self.decode_button.bind(on_press=self.decode)
        self.add_widget(self.decode_button)
        self.exit_button = Button(text='Back')
        self.exit_button.bind(on_press=self.back)
        self.add_widget(self.exit_button)

    def back(self, instance):
        manager.transition.direction = "right"
        manager.transition.duration = 1
        manager.current = "menu"

    def decode(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = 1
        manager.current = "decbin"

    def encode(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = 1
        manager.current = "encbin"


class encodebin(GridLayout):
    def __init__(self, **kwargs):
        super(encodebin, self).__init__(**kwargs)

        self.cols = 1
        self.screen_title = TitleLabel(text="Encoding in Binary", color=[250 / 255, 1, 0, 1])

        self.secondary = GridLayout()
        self.secondary.cols = 2
        self.encode_msg = Label(text="Enter data to encode: ", color=[1, 0, 0, 1])
        self.secondary.add_widget(self.encode_msg)
        self.original = TextInput(multiline=False, foreground_color=[1, 0, 0, 1],
                                  background_color=[0, 255 / 255, 228 / 255, 1], hint_text="Enter your data here!")
        self.add_widget(self.screen_title)
        self.secondary.add_widget(self.original)
        self.output = Label(text="Output: ", color=[0, 1, 0, 1])
        self.secondary.add_widget(self.output)
        self.out = TextInput(text="None", foreground_color=[0, 1, 0, 1], background_color=[0, 0, 0, 1], readonly=True,
                             multiline=False)
        self.secondary.add_widget(self.out)
        self.submit_button = Button(text='Encode!', color=[0, 0, 1, 1], background_color=[0, 1, 0, 1])
        self.submit_button.bind(on_press=self.callback)
        self.secondary.add_widget(self.submit_button)
        self.copy_button = Button(text="Copy Output To Clipboard")
        self.copy_button.bind(on_press=self.copy)
        self.secondary.add_widget(self.copy_button)
        self.back_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1], background_color=[0, 0, 1, 1])
        self.back_button.bind(on_press=self.back)
        self.secondary.add_widget(self.back_button)
        self.add_widget(self.secondary)

    def callback(self, instance):
        self.new = bin(int.from_bytes(self.original.text.encode(), 'big')).replace('b', '')
        self.out.text = self.new
        if self.out.text == "":
            self.out.text = "None"

    def back(self, instance):
        manager.transition.direction = "right"
        manager.transition.duration = 1
        manager.current = "binmenu"
        self.out.text = "None"
        self.original.text = ""

    def copy(self, instance):
        Clipboard.copy(self.out.text)


class decodebin(GridLayout):
    def __init__(self, **kwargs):
        super(decodebin, self).__init__(**kwargs)

        self.cols = 1
        self.screen_title = TitleLabel(text="Decoding in Binary", color=[250 / 255, 1, 0, 1])

        self.secondary = GridLayout()
        self.secondary.cols = 2
        self.encode_msg = Label(text="Enter data to decode: ", color=[1, 0, 0, 1])
        self.secondary.add_widget(self.encode_msg)
        self.original = TextInput(multiline=False, foreground_color=[1, 0, 0, 1],
                                  background_color=[0, 255 / 255, 228 / 255, 1], hint_text="Enter your data here!")
        self.add_widget(self.screen_title)
        self.secondary.add_widget(self.original)
        self.output = Label(text="Output: ", color=[0, 1, 0, 1])
        self.secondary.add_widget(self.output)
        self.out = TextInput(text="None", foreground_color=[0, 1, 0, 1], background_color=[0, 0, 0, 1], readonly=True,
                             multiline=False)
        self.secondary.add_widget(self.out)
        self.submit_button = Button(text='Decode!', color=[0, 0, 1, 1], background_color=[0, 1, 0, 1])
        self.submit_button.bind(on_press=self.callback)
        self.secondary.add_widget(self.submit_button)
        self.copy_button = Button(text="Copy Output To Clipboard")
        self.copy_button.bind(on_press=self.copy)
        self.secondary.add_widget(self.copy_button)
        self.back_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1], background_color=[0, 0, 1, 1])
        self.back_button.bind(on_press=self.back)
        self.secondary.add_widget(self.back_button)
        self.add_widget(self.secondary)

    def callback(self, instance):
        try:
            self.n = int(self.original.text.replace(" ", ""), 2)
            self.new = self.n.to_bytes((self.n.bit_length() + 7) // 8, 'big').decode()
            self.out.text = self.new
            if self.out.text == "":
                self.out.text = "None"
        except Exception:
            layout = GridLayout(cols=1, padding=10)

            popupLabel = Label(text="Invalid Binary...", color=[1, 0, 0, 1])
            closeButton = Button(text="Close", background_color=[1, 0, 0, 1], color=[1, 1, 1, 1])
            closeButton.bind(on_press=self.close_popup)

            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)

            self.popup = Popup(title='Error',
                               content=layout, size_hint=(None, None), size=(700, 800), separator_color=[1, 0, 0, 1])
            self.popup.open()
            Clock.schedule_once(self.popup.dismiss, 10)

    def back(self, instance):
        manager.transition.direction = "right"
        manager.transition.duration = 1
        manager.current = "binmenu"
        self.out.text = "None"
        self.original.text = ""

    def close_popup(self, instance):
        self.popup.dismiss()

    def copy(self, instance):
        Clipboard.copy(self.out.text)


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.add_widget(Menu())


class encodeb64screen(Screen):
    def __init__(self, **kwargs):
        super(encodeb64screen, self).__init__(**kwargs)
        self.add_widget(encodeb64())


class b64menuscreen(Screen):
    def __init__(self, **kwargs):
        super(b64menuscreen, self).__init__(**kwargs)
        self.add_widget(b64_menu())


class binmenuscreen(Screen):
    def __init__(self, **kwargs):
        super(binmenuscreen, self).__init__(**kwargs)
        self.add_widget(bin_menu())


class decodeb64screen(Screen):
    def __init__(self, **kwargs):
        super(decodeb64screen, self).__init__(**kwargs)
        self.add_widget(decodeb64())


class encodebinscreen(Screen):
    def __init__(self, **kwargs):
        super(encodebinscreen, self).__init__(**kwargs)
        self.add_widget(encodebin())


class decodebinscreen(Screen):
    def __init__(self, **kwargs):
        super(decodebinscreen, self).__init__(**kwargs)
        self.add_widget(decodebin())


manager = ScreenManager()
manager.add_widget(MenuScreen(name="menu"))
manager.add_widget(encodeb64screen(name="encb64"))
manager.add_widget(b64menuscreen(name="b64menu"))
manager.add_widget(binmenuscreen(name="binmenu"))
manager.add_widget(decodeb64screen(name="decb64"))
manager.add_widget(decodebinscreen(name="decbin"))
manager.add_widget(encodebinscreen(name="encbin"))
manager.current = "menu"


class Data_Encoder(App):
    def build(self):
        self.title = "Data Encoder"
        return manager


if __name__ == '__main__':
    Data_Encoder().run()