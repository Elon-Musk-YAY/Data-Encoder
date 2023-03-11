import base64
import json
import random
import sys
import os
import codecs
import binascii
import threading
from functools import partial
import requests
os.environ['KIVY_NO_FILELOG'] = '1'
from kivy.network.urlrequest import UrlRequest
import certifi
from kivy import require
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import contextmenus
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
from kivy.uix.screenmanager import ScreenManager, NoTransition, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.clipboard import Clipboard
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.progressbar import MDProgressBar
from version import version
import wx
from kivy.lang import Builder
from kivy.config import Config
from dotenv import load_dotenv


load_dotenv()

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('kivy', 'exit_on_escape', '0')

app = wx.App()
frame = wx.Frame(None, -1, 'win.py', style=wx.BORDER_NONE)
frame.SetSize(0, 0, 500, 900)
frame.SetBackgroundColour('black')
frame.Hide()
openFileDialog = wx.FileDialog(frame, "Open A File To Set It's Contents As The Input...", "", "",
                               "",
                               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

saveFileDialog = wx.FileDialog(frame, "Save Output As..", "txt files(*.txt)|*.*", "",
                               "",
                               wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

require("2.0.0")


class Stats(Popup):
    def on_open(self, *args):
        self.ev = Clock.schedule_once(lambda x: self.dismiss(), 30)

    def on_dismiss(self, *args):
        Clock.unschedule(lambda x: self.dismiss())


class menu1(FloatLayout):
    pass





class Pop(Popup):
    def on_open(self, *args):
        self.ev = Clock.schedule_once(lambda x: self.dismiss(), 10)

    def on_dismiss(self, *args):
        Clock.unschedule(lambda x: self.dismiss())


class transTime(Popup):
    def show_err(self, instance):
        self.inst = instance
        self.ev = Clock.schedule_once(
            lambda x: self.change_text("Please enter the new screen transition time. (MUST BE BETWEEN 0.1 AND 10)"), 3)

    def change_text(self, to):
        self.inst.text = to

    def on_dismiss(self, *args):
        try:
            Clock.unschedule(self.ev)
        except:
            pass

    def che(self):
        app = MDApp.get_running_app()
        if "." in str(app.stats["trans_time"]):
            if ".0" not in str(app.stats["trans_time"]):
                return f"Current Screen Transition Time: {app.stats['trans_time']} " + "seconds"
            elif int(app.stats["trans_time"]) == 1:
                return "Current Screen Transition Time: 1 second"
            else:
                return f"Current Screen Transition Time: {int(app.stats['trans_time'])} " + "seconds"
        elif app.stats["trans_time"] == 1:
            return "Current Screen Transition Time: 1 second"
        else:
            return f"Current Screen Transition Time: {int(app.stats['trans_time'])} " + "seconds"

    def check_text(self, textfield_inst, label_inst):
        lab = label_inst
        self.tex = textfield_inst
        try:
            float(textfield_inst.text)
        except ValueError:
            if lab.text != "Invalid Amount. Please enter a valid amount and make sure there are no letters. Then, try again.":
                lab.text = "Invalid Amount. Please enter a valid amount and make sure there are no letters. Then, try again."
                self.show_err(lab)
            return
        if float(textfield_inst.text) >= 0.1 and float(textfield_inst.text) <= 10:
            if "." in textfield_inst.text:
                MDApp.get_running_app().trans_time = float(textfield_inst.text)
                MDApp.get_running_app().stats["trans_time"] = float(textfield_inst.text)
                data = '{"trans_time":%s}' % float(textfield_inst.text)
                req = requests.patch(
                    url="https://data-encoder-default-rtdb.firebaseio.com/" + manager.screens[
                        1].localId + ".json?auth=" +
                        manager.screens[1].idToken,
                    data=data)
            else:
                MDApp.get_running_app().trans_time = int(textfield_inst.text)
                MDApp.get_running_app().stats["trans_time"] = int(textfield_inst.text)
                data = '{"trans_time": %s}' % int(textfield_inst.text)
                req = requests.patch(
                    url="https://data-encoder-default-rtdb.firebaseio.com/" + manager.screens[
                        1].localId + ".json?auth=" +
                        manager.screens[1].idToken,
                    data=data)

            self.dismiss()
            s = Snackbar(text="Successfully changed screen transition time!", bg_color=(0, 0, 1, 1),
                         snackbar_y="25dp",
                         snackbar_x="25dp")
            s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
            s.open()
        else:
            if lab.text != "Invalid Amount. Please enter a valid amount between 0.1 and 10 and try again.":
                lab.text = "Invalid Amount. Please enter a valid amount between 0.1 and 10 and try again."
                self.show_err(lab)


Builder.load_file('custom_menus.kv')


class TitleLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos=self.pos, size=self.size)


class encodeb64(GridLayout):
    def __init__(self, **kwargs):
        super(encodeb64, self).__init__(**kwargs)

        self.cols = 1
        self.screen_title = TitleLabel(text="Encoding in Base64", color=[0, 1, 0, 1])

        self.secondary = GridLayout()
        self.secondary.cols = 2
        self.encode_msg = TitleLabel(text="Enter data to encode: ", color=[1, 0, 0, 1])
        self.secondary.add_widget(self.encode_msg)
        self.original = TextInput(foreground_color=[1, 0, 0, 1], background_color=[0, 0, 0, 1],
                                  hint_text="Enter your data here!", hint_text_color=[1, 0, 0, 0.5])

        self.add_widget(self.screen_title)
        self.secondary.add_widget(self.original)
        self.output = TitleLabel(text="Output: ", color=[0, 1, 0, 1])
        self.secondary.add_widget(self.output)
        self.out = TextInput(text="", foreground_color=[0, 1, 0, 1], background_color=[0, 0, 0, 1], readonly=True,
                             hint_text="The output will come here!", cursor_color=[0, 1, 0, 1],
                             hint_text_color=[0, 1, 0, 0.5], allow_copy=True)
        self.secondary.add_widget(self.out)
        self.submit_button = Button(text='Encode!', color=[0, 0, 1, 1], background_color=[0, 1, 0, 1],
                                    background_normal='')
        self.submit_button.disabled = True
        self.submit_button.bind(on_press=self.callback)
        self.secondary.add_widget(self.submit_button)
        self.copy_button = Button(text="Copy Output To Clipboard")
        self.copy_button.bind(on_press=self.copy)
        self.secondary.add_widget(self.copy_button)
        self.open_from_file = Button(text="Get input from file", on_press=self.file_picker)
        self.secondary.add_widget(self.open_from_file)
        self.save_to_file = Button(text="Save Output To File", on_press=lambda x: self.save_to_file_def())
        self.secondary.add_widget(self.save_to_file)
        self.back_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1], background_color=[0, 0, 1, 1],
                                  background_normal='')
        self.back_button.bind(on_press=self.back)
        self.secondary.add_widget(self.back_button)
        self.ok_button = Button(text="Open File",
                                on_press=lambda x: self.open(openFileDialog.GetPath()),
                                background_color=[1, 122 / 255, 0, 1], color=[0, 1, 0, 1])
        self.add_widget(self.secondary)
        self.ev = Clock.schedule_interval(lambda y: self.check(), 0.1)
        self.has_saved = True
        self.cs = Clock.schedule_interval(lambda y: self.checkSave(), 0.1)

    def callback(self, instance):
        self.new = base64.b64encode(self.original.text.encode("utf-8"))
        if self.out.text != self.new.decode("utf-8"):
            Clock.schedule_once(lambda x: self.send_to_firebase(), 0.4)
        self.out.text = self.new.decode("utf-8")

    def send_to_firebase(self):
        app = MDApp.get_running_app()
        send1 = '{"enc_times":"%s", "total_times":"%s"}' % (
        str(app.stats["enc_times"] + 1), str(app.stats["total_times"] + 1))
        app.stats["enc_times"] += 1
        app.stats["total_times"] += 1
        if manager.screens[1].login_state == "in":
            req = requests.patch(
                "https://data-encoder-default-rtdb.firebaseio.com/" + manager.screens[1].localId + ".json?auth=" +
                manager.screens[1].idToken,
                data=send1)

    def open(self, filename):
        try:
            with open(filename) as f:
                self.original.text = f.read()
            s = Snackbar(text="Successfully imported data from file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                         snackbar_y="25dp",
                         snackbar_x="25dp")
            s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
            s.open()
        except:
            pass

    def back(self, instance):
        openFileDialog.SetFilename("")
        self.cs.cancel()
        self.ev.cancel()
        try:
            self.check_for_new.cancel()
        except:
            pass
        self.submit_button.disabled = True
        self.out.text = ""
        manager.transition.direction = "right"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "b64menu"
        self.original.text = ""

    def file_picker(self, instance):
        openFileDialog.ShowModal()
        self.open(openFileDialog.GetPath())

        Window.raise_window()

    def save_to_file_def(self):
        if openFileDialog.GetFilename():
            saveFileDialog.SetFilename(f"{os.path.splitext(openFileDialog.GetFilename())[0]} Encoded.txt")
        else:
            saveFileDialog.SetFilename(f"Encoding {random.randint(0, 999999)}.txt")
        saveFileDialog.ShowModal()
        self.write_to_file(saveFileDialog.GetPath())

        Window.raise_window()
        if len(saveFileDialog.GetPath()) > 0:
            self.has_saved = True
            self.save_1 = self.original.text
            self.save_2 = self.out.text
            self.check_for_new = Clock.schedule_interval(lambda y: self.new_check(), 0.1)
        else:
            self.has_saved = False

    def write_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                f.write(self.out.text)
                f.close()
                s = Snackbar(text="Successfully exported data to file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                             snackbar_y="25dp",
                             snackbar_x="25dp")
                s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
                s.open()
        except:
            pass

    def check(self):
        if manager.current == "encb64":
            if self.original.text:
                if self.submit_button.disabled == True:
                    self.submit_button.disabled = False
                return
            self.submit_button.disabled = True

    def copy(self, instance):
        Clipboard.copy(self.out.text)

    def new_check(self):
        if self.save_1 != self.original.text or self.save_2 != self.out.text:
            self.has_saved = False
        else:
            self.has_saved = True

    def checkSave(self):
        if self.original.text != "" or self.out.text != "":
            self.has_saved = False


class decodeb64(GridLayout):
    def __init__(self, **kwargs):
        super(decodeb64, self).__init__(**kwargs)

        self.cols = 1
        self.screen_title = TitleLabel(text="Decoding in Base64", color=[0, 1, 0, 1])

        self.secondary = GridLayout()
        self.secondary.cols = 2
        self.encode_msg = TitleLabel(text="Enter data to decode: ", color=[1, 0, 0, 1])
        self.secondary.add_widget(self.encode_msg)
        self.original = TextInput(foreground_color=[1, 0, 0, 1], background_color=[0, 0, 0, 1],
                                  hint_text="Enter your data here!", hint_text_color=[1, 0, 0, 0.5])
        self.add_widget(self.screen_title)
        self.secondary.add_widget(self.original)
        self.output = TitleLabel(text="Output: ", color=[0, 1, 0, 1])
        self.secondary.add_widget(self.output)
        self.out = TextInput(text="", foreground_color=[0, 1, 0, 1], background_color=[0, 0, 0, 1], readonly=True,
                             hint_text="The output will come here!", cursor_color=[0, 1, 0, 1],
                             hint_text_color=[0, 1, 0, 0.5], allow_copy=True)
        self.secondary.add_widget(self.out)
        self.submit_button = Button(text='Decode!', color=[0, 0, 1, 1], background_color=[0, 1, 0, 1],
                                    background_normal='')
        self.submit_button.disabled = True
        self.submit_button.bind(on_press=self.callback)
        self.secondary.add_widget(self.submit_button)
        self.copy_button = Button(text="Copy Output To Clipboard")
        self.copy_button.bind(on_press=self.copy)
        self.secondary.add_widget(self.copy_button)
        self.open_from_file = Button(text="Get input from file", on_press=self.file_picker)
        self.secondary.add_widget(self.open_from_file)
        self.save_to_file = Button(text="Save Output To File", on_press=lambda x: self.save_to_file_def())
        self.secondary.add_widget(self.save_to_file)
        self.back_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1], background_color=[0, 0, 1, 1],
                                  background_normal='')
        self.back_button.bind(on_press=self.back)
        self.secondary.add_widget(self.back_button)
        self.ok_button = Button(text="Open File",
                                on_press=lambda x: self.open(openFileDialog.GetPath()),
                                background_color=[1, 122 / 255, 0, 1], color=[0, 1, 0, 1])
        self.add_widget(self.secondary)
        self.ev = Clock.schedule_interval(lambda y: self.check(), 0.1)
        self.has_saved = True
        self.cs = Clock.schedule_interval(lambda y: self.checkSave(), 0.1)

    def callback(self, instance):
        try:
            self.new = base64.b64decode(self.original.text.encode("utf-8"))
            if self.out.text != self.new.decode("utf-8"):
                Clock.schedule_once(lambda x: self.send_to_firebase(), 0.4)
            self.out.text = self.new.decode("utf-8")
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

    def send_to_firebase(self):
        app = MDApp.get_running_app()
        send1 = '{"dec_times":"%s", "total_times":"%s"}' % (
        str(app.stats["dec_times"] + 1), str(app.stats["total_times"] + 1))
        app.stats["dec_times"] += 1
        app.stats["total_times"] += 1
        if manager.screens[1].login_state == "in":
            req = requests.patch(
                "https://data-encoder-default-rtdb.firebaseio.com/" + manager.screens[1].localId + ".json?auth=" +
                manager.screens[1].idToken,
                data=send1)

    def back(self, instance):
        self.cs.cancel()
        self.ev.cancel()
        openFileDialog.SetFilename("")
        try:
            self.check_for_new.cancel()
        except:
            pass
        self.submit_button.disabled = True
        manager.transition.direction = "right"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "b64menu"
        self.out.text = ""
        self.original.text = ""

    def close_popup(self, instance):
        self.popup.dismiss()

    def file_picker(self, instance):
        openFileDialog.ShowModal()
        self.open(openFileDialog.GetPath())

        Window.raise_window()

    def copy(self, instance):
        Clipboard.copy(self.out.text)

    def open(self, filename):
        try:
            with open(filename) as f:
                self.original.text = f.read()
            s = Snackbar(text="Successfully imported data from file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                         snackbar_y="25dp",
                         snackbar_x="25dp")
            s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
            s.open()
        except:
            pass

    def save_to_file_def(self):
        if openFileDialog.GetFilename():
            saveFileDialog.SetFilename(f"{os.path.splitext(openFileDialog.GetFilename())[0]} Decoded.txt")
        else:
            saveFileDialog.SetFilename(f"Encoding {random.randint(0, 999999)}.txt")
        saveFileDialog.ShowModal()
        self.write_to_file(saveFileDialog.GetPath())

        Window.raise_window()
        if len(saveFileDialog.GetPath()) > 0:
            self.has_saved = True
            self.save_1 = self.original.text
            self.save_2 = self.out.text
            self.check_for_new = Clock.schedule_interval(lambda y: self.new_check(), 0.1)
        else:
            self.has_saved = False

    def write_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                f.write(self.out.text)
                f.close()
                s = Snackbar(text="Successfully exported data to file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                             snackbar_y="25dp",
                             snackbar_x="25dp")
                s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
                s.open()
        except:
            pass

    def check(self):
        if manager.current == "decb64":
            if len(self.original.text) > 0:
                if self.submit_button.disabled == True:
                    self.submit_button.disabled = False
                return
            self.submit_button.disabled = True

    def new_check(self):
        if self.save_1 != self.original.text or self.save_2 != self.out.text:
            self.has_saved = False
        else:
            self.has_saved = True

    def checkSave(self):
        if self.original.text != "" or self.out.text != "":
            self.has_saved = False


class SuperTitle(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos=self.pos, size=self.size)


class splash(GridLayout):
    def __init__(self, **kwargs):
        super(splash, self).__init__(**kwargs)

        Window.size = (900, 500)
        Window.borderless = True
        Window.bind(on_resize=self.rezise)
        Window.bind(on_maximize=self._pass)
        self.cols = 1
        self.loading_win = BoxLayout(orientation="vertical")
        self.splash_label = Label(text="Data Encoder", font_size=80, color=[218 / 255, 238 / 255, 0, 0.8],
                                  pos_hint={"y": 0.2})
        self.splash_version = Label(text=version, font_size=40, color=[0, 1, 0, 1], pos_hint={"y": .5})
        self.loading_win.add_widget(self.splash_label)
        self.loading_win.add_widget(self.splash_version)
        self.bar = MDProgressBar(size_hint_x=None, width=1400, pos_hint={"x": 0.1, "y": .75}, type="indeterminate",
                                 color=[1, 0, 0, 1], running_duration=1, catching_duration=1)
        self.loading_win.add_widget(self.bar)
        self.add_widget(self.loading_win)

    def rezise(self, *args):
        Window.size = (900, 500)

    def _pass(self, *args):
        pass


def rgba(a, b, c, d):
    return [a / 255, b / 255, c / 255, d]


class splashScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = [0, 0, 0, 1]
        self.thing = splash()
        self.ids["fun"] = self.thing
        self.add_widget(self.thing)

    def on_enter(self, *args):
        self.thing.bar.start()

    def on_leave(self, *args):
        self.thing.bar.stop()


class Menu(GridLayout):
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.cols = 1
        self.show_menu()

    def go_to_binary(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "binmenu"

    def go_to_rot_13(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "rot13menu"

    def go_to_hex(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "hexmenu"

    def back(self, instance):
        self.exit_button.text = "The application is closing..."
        self.bin_button.disabled = True
        self.b64_button.disabled = True
        self.exit_button.disabled = True
        self.crs.disabled = True
        self.rot_btn.disabled = True
        self.hex_btn.disabled = True
        titlebar.ids.m1.disabled = True
        titlebar.ids.m3.disabled = True
        titlebar.ids.m4.disabled = True
        titlebar.ids.m5.disabled = True
        titlebar.ids.m6.disabled = True
        self.choose.color = (0.25, 0.25, 0.25, 1)
        Window.bind(on_request_close=lambda x: x != 5)
        Clock.schedule_once(self.close_app, 2)

    def close_app(self, instance):
        sys.exit()

    def go_to_b64(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "b64menu"

    def show_menu(self):
        self.clear_widgets()
        self.white_space = Label(text="")
        self.add_widget(self.white_space)
        self.avatar = Image(source="avatars/man-1.png")
        self.add_widget(self.avatar)
        self.choose = SuperTitle(text="Choose a encoding/decoding scheme!", color=[1, 0, 0, 1])
        self.add_widget(self.choose)
        self.b64_button = Button(text='Base 64', color=[0, 0, 1, 1], background_color=[0, 1, 0, 0.5])
        self.b64_button.bind(on_press=self.go_to_b64)
        self.add_widget(self.b64_button)
        self.bin_button = Button(text='Binary', color=[0, 1, 0, 1], background_color=[0, 0, 0, 1])
        self.bin_button.bind(on_press=self.go_to_binary)
        self.add_widget(self.bin_button)
        self.rot_btn = Button(text="Rot13", color=rgba(24, 180, 162, 0.6), background_color=rgba(136, 11, 187, 0.2),
                              on_press=self.go_to_rot_13, background_normal='', background_down='')
        self.add_widget(self.rot_btn)
        self.hex_btn = Button(text="Hex", color=rgba(204, 46, 211, 0.9), background_color=rgba(80, 63, 219, 1),
                              on_press=self.go_to_hex, background_normal='')
        self.add_widget(self.hex_btn)
        self.crs = Button(text="Credits", color=[1, 0.5, 1], background_color=[0, 0, 1, 1],
                          on_press=lambda x: self.showCredits())
        self.exit_button = Button(text='Exit Application', color=[1, 1, 1, 1], background_color=[1, 0, 0, 1])
        self.exit_button.bind(on_press=self.back)
        self.add_widget(self.crs)
        self.add_widget(self.exit_button)

    def showCredits(self):
        manager.transition.direction = "left"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "credits"


class b64_menu(GridLayout):
    def __init__(self, **kwargs):
        super(b64_menu, self).__init__(**kwargs)

        self.cols = 1
        self.menu_text = TitleLabel(text="Base 64 Menu", color=[0, 1, 0, 1])
        self.add_widget(self.menu_text)
        self.choosing = TitleLabel(text="Choose to encode or decode your data!", color=[1, 0, 0, 1])
        self.add_widget(self.choosing)
        self.encode_button = Button(text='Encode', background_normal='', background_color=rgba(232, 84, 250, 0.8))
        self.encode_button.bind(on_press=self.encode)
        self.add_widget(self.encode_button)
        self.decode_button = Button(text='Decode', background_normal='', background_color=rgba(26, 64, 202, 0.3))
        self.decode_button.bind(on_press=self.decode)
        self.add_widget(self.decode_button)
        self.exit_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1],
                                  background_color=rgba(65, 51, 137, 0.9), background_normal='')
        self.exit_button.bind(on_press=self.back)
        self.add_widget(self.exit_button)

    def back(self, instance):
        manager.transition.direction = "right"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "menu"

    def decode(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "decb64"

    def encode(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "encb64"


class bin_menu(GridLayout):
    def __init__(self, **kwargs):
        super(bin_menu, self).__init__(**kwargs)

        self.cols = 1
        self.menu_text = TitleLabel(text="Binary Menu", color=[0, 1, 0, 1])
        self.add_widget(self.menu_text)
        self.choosing = TitleLabel(text="Choose to encode or decode your data!", color=[1, 0, 0, 1])
        self.add_widget(self.choosing)
        self.encode_button = Button(text='Encode', background_normal='', background_color=rgba(232, 84, 250, 0.8))
        self.encode_button.bind(on_press=self.encode)
        self.add_widget(self.encode_button)
        self.decode_button = Button(text='Decode', background_normal='', background_color=rgba(26, 64, 202, 0.3))
        self.decode_button.bind(on_press=self.decode)
        self.add_widget(self.decode_button)
        self.exit_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1],
                                  background_color=rgba(65, 51, 137, 0.9), background_normal='')
        self.exit_button.bind(on_press=self.back)
        self.add_widget(self.exit_button)

    def back(self, instance):
        manager.transition.direction = "right"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "menu"

    def decode(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "decbin"

    def encode(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "encbin"


class encodebin(GridLayout):
    def __init__(self, **kwargs):
        super(encodebin, self).__init__(**kwargs)

        self.cols = 1
        self.screen_title = TitleLabel(text="Encoding in Binary", color=[0, 1, 0, 1])

        self.secondary = GridLayout()
        self.secondary.cols = 2
        self.encode_msg = TitleLabel(text="Enter data to encode: ", color=[1, 0, 0, 1])
        self.secondary.add_widget(self.encode_msg)
        self.original = TextInput(foreground_color=[1, 0, 0, 1], background_color=[0, 0, 0, 1],
                                  hint_text="Enter your data here!", hint_text_color=[1, 0, 0, 0.5])

        self.add_widget(self.screen_title)
        self.secondary.add_widget(self.original)
        self.output = TitleLabel(text="Output: ", color=[0, 1, 0, 1])
        self.secondary.add_widget(self.output)
        self.out = TextInput(text="", foreground_color=[0, 1, 0, 1], background_color=[0, 0, 0, 1], readonly=True,
                             hint_text="The output will come here!", cursor_color=[0, 1, 0, 1],
                             hint_text_color=[0, 1, 0, 0.5], allow_copy=True)
        self.secondary.add_widget(self.out)
        self.submit_button = Button(text='Encode!', color=[0, 0, 1, 1], background_color=[0, 1, 0, 1],
                                    background_normal='')
        self.submit_button.disabled = True
        self.submit_button.bind(on_press=self.callback)
        self.secondary.add_widget(self.submit_button)
        self.copy_button = Button(text="Copy Output To Clipboard")
        self.copy_button.bind(on_press=self.copy)
        self.secondary.add_widget(self.copy_button)
        self.open_from_file = Button(text="Get input from file", on_press=self.file_picker)
        self.secondary.add_widget(self.open_from_file)
        self.save_to_file = Button(text="Save Output To File", on_press=lambda x: self.save_to_file_def())
        self.secondary.add_widget(self.save_to_file)
        self.back_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1], background_color=[0, 0, 1, 1],
                                  background_normal='')
        self.back_button.bind(on_press=self.back)
        self.secondary.add_widget(self.back_button)
        self.ok_button = Button(text="Open File",
                                on_press=lambda x: self.open(openFileDialog.GetPath()),
                                background_color=[1, 122 / 255, 0, 1], color=[0, 1, 0, 1])
        self.add_widget(self.secondary)
        self.ev = Clock.schedule_interval(lambda y: self.check(), 0.1)
        self.has_saved = True
        self.cs = Clock.schedule_interval(lambda y: self.checkSave(), 0.1)

    def callback(self, instance):
        self.new = bin(int.from_bytes(self.original.text.encode(), 'big')).replace('b', '')
        if self.out.text != self.new:
            Clock.schedule_once(lambda x: self.send_to_firebase(), 0.4)
        self.out.text = self.new

    def send_to_firebase(self):
        app = MDApp.get_running_app()
        send1 = '{"enc_times":"%s", "total_times":"%s"}' % (
        str(app.stats["enc_times"] + 1), str(app.stats["total_times"] + 1))
        app.stats["enc_times"] += 1
        app.stats["total_times"] += 1
        if manager.screens[1].login_state == "in":
            req = requests.patch(
                "https://data-encoder-default-rtdb.firebaseio.com/" + manager.screens[1].localId + ".json?auth=" +
                manager.screens[1].idToken,
                data=send1)

    def back(self, instance):
        openFileDialog.SetFilename("")
        self.cs.cancel()
        self.ev.cancel()
        try:
            self.check_for_new.cancel()
        except:
            pass
        self.submit_button.disabled = True
        manager.transition.direction = "right"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "binmenu"
        self.out.text = ""
        self.original.text = ""

    def copy(self, instance):
        Clipboard.copy(self.out.text)

    def file_picker(self, instance):
        openFileDialog.ShowModal()
        self.open(openFileDialog.GetPath())

        Window.raise_window()

    def open(self, filename):
        try:
            with open(filename) as f:
                self.original.text = f.read()
            s = Snackbar(text="Successfully imported data from file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                         snackbar_y="25dp",
                         snackbar_x="25dp")
            s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
            s.open()
        except:
            pass

    def save_to_file_def(self):
        if openFileDialog.GetFilename():
            saveFileDialog.SetFilename(f"{os.path.splitext(openFileDialog.GetFilename())[0]} Encoded.txt")
        else:
            saveFileDialog.SetFilename(f"Encoding {random.randint(0, 999999)}.txt")
        saveFileDialog.ShowModal()
        self.write_to_file(saveFileDialog.GetPath())

        Window.raise_window()
        if len(saveFileDialog.GetPath()) > 0:
            self.has_saved = True
            self.save_1 = self.original.text
            self.save_2 = self.out.text
            self.check_for_new = Clock.schedule_interval(lambda y: self.new_check(), 0.1)
        else:
            self.has_saved = False

    def write_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                f.write(self.out.text)
                f.close()
                s = Snackbar(text="Successfully exported data to file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                             snackbar_y="25dp",
                             snackbar_x="25dp")
                s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
                s.open()
        except:
            pass

    def check(self):
        if manager.current == "encbin":
            if len(self.original.text) > 0:
                if self.submit_button.disabled == True:
                    self.submit_button.disabled = False
                return
            self.submit_button.disabled = True

    def new_check(self):
        if self.save_1 != self.original.text or self.save_2 != self.out.text:
            self.has_saved = False
        else:
            self.has_saved = True

    def checkSave(self):
        if self.original.text != "" or self.out.text != "":
            self.has_saved = False


class decodebin(GridLayout):
    def __init__(self, **kwargs):
        super(decodebin, self).__init__(**kwargs)

        self.cols = 1
        self.screen_title = TitleLabel(text="Decoding in Binary", color=[0, 1, 0, 1])

        self.secondary = GridLayout()
        self.secondary.cols = 2
        self.encode_msg = TitleLabel(text="Enter data to decode: ", color=[1, 0, 0, 1])
        self.secondary.add_widget(self.encode_msg)
        self.original = TextInput(foreground_color=[1, 0, 0, 1], background_color=[0, 0, 0, 1],
                                  hint_text="Enter your data here!", hint_text_color=[1, 0, 0, 0.5])
        self.add_widget(self.screen_title)
        self.secondary.add_widget(self.original)
        self.output = TitleLabel(text="Output: ", color=[0, 1, 0, 1])
        self.secondary.add_widget(self.output)
        self.out = TextInput(text="", foreground_color=[0, 1, 0, 1], background_color=[0, 0, 0, 1], readonly=True,
                             hint_text="The output will come here!", cursor_color=[0, 1, 0, 1],
                             hint_text_color=[0, 1, 0, 0.5], allow_copy=True)
        self.secondary.add_widget(self.out)
        self.submit_button = Button(text='Decode!', color=[0, 0, 1, 1], background_color=[0, 1, 0, 1],
                                    background_normal='')
        self.submit_button.disabled = True
        self.submit_button.bind(on_press=self.callback)
        self.secondary.add_widget(self.submit_button)
        self.copy_button = Button(text="Copy Output To Clipboard")
        self.copy_button.bind(on_press=self.copy)
        self.secondary.add_widget(self.copy_button)
        self.open_from_file = Button(text="Get input from file", on_press=self.file_picker)
        self.secondary.add_widget(self.open_from_file)
        self.save_to_file = Button(text="Save Output To File", on_press=lambda x: self.save_to_file_def())
        self.secondary.add_widget(self.save_to_file)
        self.back_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1], background_color=[0, 0, 1, 1],
                                  background_normal='')
        self.back_button.bind(on_press=self.back)
        self.secondary.add_widget(self.back_button)
        self.ok_button = Button(text="Open File",
                                on_press=lambda x: self.open(openFileDialog.GetPath()),
                                background_color=[1, 122 / 255, 0, 1], color=[0, 1, 0, 1])
        self.add_widget(self.secondary)
        self.ev = Clock.schedule_interval(lambda x: self.check(), 0.1)
        self.has_saved = True
        self.cs = Clock.schedule_interval(lambda y: self.checkSave(), 0.1)

    def callback(self, instance):
        try:
            self.n = int(self.original.text.replace(" ", ""), 2)
            self.new = self.n.to_bytes((self.n.bit_length() + 7) // 8, 'big').decode()
            if self.out.text != self.new:
                Clock.schedule_once(lambda x: self.send_to_firebase(), 0.4)
            self.out.text = self.new
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

    def send_to_firebase(self):
        app = MDApp.get_running_app()
        send1 = '{"dec_times":"%s", "total_times":"%s"}' % (
        str(app.stats["dec_times"] + 1), str(app.stats["total_times"] + 1))
        app.stats["dec_times"] += 1
        app.stats["total_times"] += 1
        if manager.screens[1].login_state == "in":
            req = requests.patch(
                "https://data-encoder-default-rtdb.firebaseio.com/" + manager.screens[1].localId + ".json?auth=" +
                manager.screens[1].idToken,
                data=send1)

    def back(self, instance):
        self.cs.cancel()
        self.ev.cancel()
        openFileDialog.SetFilename("")
        try:
            self.check_for_new.cancel()
        except:
            pass
        self.submit_button.disabled = True
        manager.transition.direction = "right"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "binmenu"
        self.out.text = ""
        self.original.text = ""

    def close_popup(self, instance):
        self.popup.dismiss()

    def copy(self, instance):
        Clipboard.copy(self.out.text)

    def file_picker(self, instance):
        openFileDialog.ShowModal()
        self.open(openFileDialog.GetPath())

        Window.raise_window()

    def open(self, filename):
        try:
            with open(filename) as f:
                self.original.text = f.read()
            s = Snackbar(text="Successfully imported data from file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                         snackbar_y="25dp",
                         snackbar_x="25dp")
            s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
            s.open()
        except:
            pass

    def save_to_file_def(self):
        if openFileDialog.GetFilename():
            saveFileDialog.SetFilename(f"{os.path.splitext(openFileDialog.GetFilename())[0]} Decoded.txt")
        else:
            saveFileDialog.SetFilename(f"Decoding {random.randint(0, 999999)}.txt")
        saveFileDialog.ShowModal()
        self.write_to_file(saveFileDialog.GetPath())

        Window.raise_window()
        if len(saveFileDialog.GetPath()) > 0:
            self.has_saved = True
            self.save_1 = self.original.text
            self.save_2 = self.out.text
            self.check_for_new = Clock.schedule_interval(lambda y: self.new_check(), 0.1)
        else:
            self.has_saved = False

    def write_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                f.write(self.out.text)
                f.close()
                s = Snackbar(text="Successfully exported data to file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                             snackbar_y="25dp",
                             snackbar_x="25dp")
                s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
                s.open()
        except:
            pass

    def check(self):
        if manager.current == "decbin":
            if len(self.original.text) > 0:
                if self.submit_button.disabled == True:
                    self.submit_button.disabled = False
                return
            self.submit_button.disabled = True

    def new_check(self):
        if self.save_1 != self.original.text or self.save_2 != self.out.text:
            self.has_saved = False
        else:
            self.has_saved = True

    def checkSave(self):
        if self.original.text != "" or self.out.text != "":
            self.has_saved = False


class credits(GridLayout):
    def __init__(self, **kwargs):
        super(credits, self).__init__(**kwargs)
        self.cols = 1
        self.nam = Label(text="Credits", color=[0, 0, 1, 1])
        self.cre = Label(text="Creator - Akshar Desai", color=[0, 1, 0, 1])
        self.cp = Label(text="Copyright", color=[1, 0, 0, 1])
        self.rl = Label(text="© 2021 Akshar Desai Apps", color=[0, 1, 0, 1])
        self.back = Button(text="Back", color=[255 / 255, 143 / 255, 0, 1], background_color=[0, 0, 1, 1],
                           background_normal='',
                           on_press=lambda x: self.back1())
        self.add_widget(self.nam)
        self.add_widget(self.cre)
        self.add_widget(self.cp)
        self.add_widget(self.rl)
        self.add_widget(self.back)

    def back1(self):
        manager.current = "menu"
        manager.transition.direction = "right"
        manager.transition.duration = MDApp.get_running_app().trans_time


class rot13_menu(GridLayout):
    def __init__(self, **kwargs):
        super(rot13_menu, self).__init__(**kwargs)

        self.cols = 1
        self.menu_text = TitleLabel(text="Rot13 Menu", color=[0, 1, 0, 1])
        self.add_widget(self.menu_text)
        self.choosing = TitleLabel(text="Choose to encode or decode your data!", color=[1, 0, 0, 1])
        self.add_widget(self.choosing)
        self.encode_button = Button(text='Encode', background_color=rgba(232, 84, 250, 0.8), background_normal='')
        self.encode_button.bind(on_press=self.encode)
        self.add_widget(self.encode_button)
        self.decode_button = Button(text='Decode', background_normal='', background_color=rgba(26, 64, 202, 0.3))
        self.decode_button.bind(on_press=self.decode)
        self.add_widget(self.decode_button)
        self.exit_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1],
                                  background_color=rgba(65, 51, 137, 0.9), background_normal='')
        self.exit_button.bind(on_press=self.back)
        self.add_widget(self.exit_button)

    def back(self, instance):
        manager.transition.direction = "right"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "menu"

    def decode(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "decrot13"

    def encode(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "encrot13"


class encoderot13(GridLayout):
    def __init__(self, **kwargs):
        super(encoderot13, self).__init__(**kwargs)

        self.cols = 1
        self.screen_title = TitleLabel(text="Encoding in Rot13", color=[0, 1, 0, 1])

        self.secondary = GridLayout()
        self.secondary.cols = 2
        self.encode_msg = TitleLabel(text="Enter data to encode: ", color=[1, 0, 0, 1])
        self.secondary.add_widget(self.encode_msg)
        self.original = TextInput(foreground_color=[1, 0, 0, 1], background_color=[0, 0, 0, 1],
                                  hint_text="Enter your data here!", hint_text_color=[1, 0, 0, 0.5])

        self.add_widget(self.screen_title)
        self.secondary.add_widget(self.original)
        self.output = TitleLabel(text="Output: ", color=[0, 1, 0, 1])
        self.secondary.add_widget(self.output)
        self.out = TextInput(text="", foreground_color=[0, 1, 0, 1], background_color=[0, 0, 0, 1], readonly=True,
                             hint_text="The output will come here!", cursor_color=[0, 1, 0, 1],
                             hint_text_color=[0, 1, 0, 0.5], allow_copy=True)
        self.secondary.add_widget(self.out)
        self.submit_button = Button(text='Encode!', color=[0, 0, 1, 1], background_color=[0, 1, 0, 1],
                                    background_normal='')
        self.submit_button.disabled = True
        self.submit_button.bind(on_press=self.callback)
        self.secondary.add_widget(self.submit_button)
        self.copy_button = Button(text="Copy Output To Clipboard")
        self.copy_button.bind(on_press=self.copy)
        self.secondary.add_widget(self.copy_button)
        self.open_from_file = Button(text="Get input from file", on_press=self.file_picker)
        self.secondary.add_widget(self.open_from_file)
        self.save_to_file = Button(text="Save Output To File", on_press=lambda x: self.save_to_file_def())
        self.secondary.add_widget(self.save_to_file)
        self.back_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1], background_color=[0, 0, 1, 1],
                                  background_normal='')
        self.back_button.bind(on_press=self.back)
        self.secondary.add_widget(self.back_button)
        self.ok_button = Button(text="Open File",
                                on_press=lambda x: self.open(openFileDialog.GetPath()),
                                background_color=[1, 122 / 255, 0, 1], color=[0, 1, 0, 1])
        self.add_widget(self.secondary)
        self.ev = Clock.schedule_interval(lambda y: self.check(), 0.1)
        self.has_saved = True
        self.cs = Clock.schedule_interval(lambda y: self.checkSave(), 0.1)

    def callback(self, instance):
        self.new = codecs.encode(self.original.text, "rot_13")
        if self.out.text != self.new:
            Clock.schedule_once(lambda x: self.send_to_firebase(), 0.4)
        self.out.text = self.new

    def send_to_firebase(self):
        app = MDApp.get_running_app()
        send1 = '{"enc_times":"%s", "total_times":"%s"}' % (
        str(app.stats["enc_times"] + 1), str(app.stats["total_times"] + 1))
        app.stats["enc_times"] += 1
        app.stats["total_times"] += 1
        if manager.screens[1].login_state == "in":
            req = requests.patch(
                "https://data-encoder-default-rtdb.firebaseio.com/" + manager.screens[1].localId + ".json?auth=" +
                manager.screens[1].idToken,
                data=send1)

    def back(self, instance):
        openFileDialog.SetFilename("")
        self.cs.cancel()
        self.ev.cancel()
        try:
            self.check_for_new.cancel()
        except:
            pass
        self.submit_button.disabled = True
        manager.transition.direction = "right"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "rot13menu"
        self.out.text = ""
        self.original.text = ""

    def copy(self, instance):
        Clipboard.copy(self.out.text)

    def file_picker(self, instance):
        openFileDialog.ShowModal()
        self.open(openFileDialog.GetPath())

        Window.raise_window()

    def open(self, filename):
        try:
            with open(filename) as f:
                self.original.text = f.read()
            s = Snackbar(text="Successfully imported data from file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                         snackbar_y="25dp",
                         snackbar_x="25dp")
            s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
            s.open()
        except:
            pass

    def save_to_file_def(self):
        if openFileDialog.GetFilename():
            saveFileDialog.SetFilename(f"{os.path.splitext(openFileDialog.GetFilename())[0]} Encoded.txt")
        else:
            saveFileDialog.SetFilename(f"Encoding {random.randint(0, 999999)}.txt")
        saveFileDialog.ShowModal()
        self.write_to_file(saveFileDialog.GetPath())

        Window.raise_window()
        if len(saveFileDialog.GetPath()) > 0:
            self.has_saved = True
            self.save_1 = self.original.text
            self.save_2 = self.out.text
            self.check_for_new = Clock.schedule_interval(lambda y: self.new_check(), 0.1)
        else:
            self.has_saved = False

    def write_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                f.write(self.out.text)
                f.close()
                s = Snackbar(text="Successfully exported data to file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                             snackbar_y="25dp",
                             snackbar_x="25dp")
                s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
                s.open()
        except:
            pass

    def check(self):
        if manager.current == "encrot13":
            if len(self.original.text) > 0:
                if self.submit_button.disabled == True:
                    self.submit_button.disabled = False
                return
            self.submit_button.disabled = True

    def new_check(self):
        if self.save_1 != self.original.text or self.save_2 != self.out.text:
            self.has_saved = False
        else:
            self.has_saved = True

    def checkSave(self):
        if self.original.text != "" or self.out.text != "":
            self.has_saved = False


class decoderot13(GridLayout):
    def __init__(self, **kwargs):
        super(decoderot13, self).__init__(**kwargs)

        self.cols = 1
        self.screen_title = TitleLabel(text="Decoding in Rot13", color=[0, 1, 0, 1])

        self.secondary = GridLayout()
        self.secondary.cols = 2
        self.encode_msg = TitleLabel(text="Enter data to decode: ", color=[1, 0, 0, 1])
        self.secondary.add_widget(self.encode_msg)
        self.original = TextInput(foreground_color=[1, 0, 0, 1], background_color=[0, 0, 0, 1],
                                  hint_text="Enter your data here!", hint_text_color=[1, 0, 0, 0.5])
        self.add_widget(self.screen_title)
        self.secondary.add_widget(self.original)
        self.output = TitleLabel(text="Output: ", color=[0, 1, 0, 1])
        self.secondary.add_widget(self.output)
        self.out = TextInput(text="", foreground_color=[0, 1, 0, 1], background_color=[0, 0, 0, 1], readonly=True,
                             hint_text="The output will come here!", cursor_color=[0, 1, 0, 1],
                             hint_text_color=[0, 1, 0, 0.5], allow_copy=True)
        self.secondary.add_widget(self.out)
        self.submit_button = Button(text='Decode!', color=[0, 0, 1, 1], background_color=[0, 1, 0, 1],
                                    background_normal='')
        self.submit_button.disabled = True
        self.submit_button.bind(on_press=self.callback)
        self.secondary.add_widget(self.submit_button)
        self.copy_button = Button(text="Copy Output To Clipboard")
        self.copy_button.bind(on_press=self.copy)
        self.secondary.add_widget(self.copy_button)
        self.open_from_file = Button(text="Get input from file", on_press=self.file_picker)
        self.secondary.add_widget(self.open_from_file)
        self.save_to_file = Button(text="Save Output To File", on_press=lambda x: self.save_to_file_def())
        self.secondary.add_widget(self.save_to_file)
        self.back_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1], background_color=[0, 0, 1, 1],
                                  background_normal='')
        self.back_button.bind(on_press=self.back)
        self.secondary.add_widget(self.back_button)
        self.ok_button = Button(text="Open File",
                                on_press=lambda x: self.open(openFileDialog.GetPath()),
                                background_color=[1, 122 / 255, 0, 1], color=[0, 1, 0, 1])
        self.add_widget(self.secondary)
        self.ev = Clock.schedule_interval(lambda x: self.check(), 0.1)
        self.has_saved = True
        self.cs = Clock.schedule_interval(lambda y: self.checkSave(), 0.1)

    def callback(self, instance):
        try:
            self.new = codecs.encode(self.original.text, "rot_13")
            if self.out.text != self.new:
                Clock.schedule_once(lambda x: self.send_to_firebase(), 0.4)
            self.out.text = self.new
        except Exception:
            layout = GridLayout(cols=1, padding=10)

            popupLabel = Label(text="Invalid Rot13...", color=[1, 0, 0, 1])
            closeButton = Button(text="Close", background_color=[1, 0, 0, 1], color=[1, 1, 1, 1])
            closeButton.bind(on_press=self.close_popup)

            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)

            self.popup = Popup(title='Error',
                               content=layout, size_hint=(None, None), size=(700, 800), separator_color=[1, 0, 0, 1])
            self.popup.open()
            Clock.schedule_once(self.popup.dismiss, 10)

    def send_to_firebase(self):
        app = MDApp.get_running_app()
        send1 = '{"dec_times":"%s", "total_times":"%s"}' % (
        str(app.stats["dec_times"] + 1), str(app.stats["total_times"] + 1))
        app.stats["dec_times"] += 1
        app.stats["total_times"] += 1
        if manager.screens[1].login_state == "in":
            req = requests.patch(
                "https://data-encoder-default-rtdb.firebaseio.com/" + manager.screens[1].localId + ".json?auth=" +
                manager.screens[1].idToken,
                data=send1)

    def back(self, instance):
        openFileDialog.SetFilename("")
        self.cs.cancel()
        self.ev.cancel()
        try:
            self.check_for_new.cancel()
        except:
            pass
        self.submit_button.disabled = True
        manager.transition.direction = "right"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "rot13menu"
        self.out.text = ""
        self.original.text = ""

    def close_popup(self, instance):
        self.popup.dismiss()

    def copy(self, instance):
        Clipboard.copy(self.out.text)

    def file_picker(self, instance):
        openFileDialog.ShowModal()
        self.open(openFileDialog.GetPath())

        Window.raise_window()

    def open(self, filename):
        try:
            with open(filename) as f:
                self.original.text = f.read()
            s = Snackbar(text="Successfully imported data from file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                         snackbar_y="25dp",
                         snackbar_x="25dp")
            s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
            s.open()
        except:
            pass

    def save_to_file_def(self):
        if openFileDialog.GetFilename():
            saveFileDialog.SetFilename(f"{os.path.splitext(openFileDialog.GetFilename())[0]} Decoded.txt")
        else:
            saveFileDialog.SetFilename(f"Decoding {random.randint(0, 999999)}.txt")
        saveFileDialog.ShowModal()
        self.write_to_file(saveFileDialog.GetPath())

        Window.raise_window()
        if len(saveFileDialog.GetPath()) > 0:
            self.has_saved = True
            self.save_1 = self.original.text
            self.save_2 = self.out.text
            self.check_for_new = Clock.schedule_interval(lambda y: self.new_check(), 0.1)
        else:
            self.has_saved = False

    def write_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                f.write(self.out.text)
                f.close()
                s = Snackbar(text="Successfully exported data to file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                             snackbar_y="25dp",
                             snackbar_x="25dp")
                s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
                s.open()
        except:
            pass

    def check(self):
        if manager.current == "decrot13":
            if len(self.original.text) > 0:
                if self.submit_button.disabled == True:
                    self.submit_button.disabled = False
                return
            self.submit_button.disabled = True

    def new_check(self):
        if self.save_1 != self.original.text or self.save_2 != self.out.text:
            self.has_saved = False
        else:
            self.has_saved = True

    def checkSave(self):
        if self.original.text != "" or self.out.text != "":
            self.has_saved = False


class hex_menu(GridLayout):
    def __init__(self, **kwargs):
        super(hex_menu, self).__init__(**kwargs)

        self.cols = 1
        self.menu_text = TitleLabel(text="Hex Menu", color=[0, 1, 0, 1])
        self.add_widget(self.menu_text)
        self.choosing = TitleLabel(text="Choose to encode or decode your data!", color=[1, 0, 0, 1])
        self.add_widget(self.choosing)
        self.encode_button = Button(text='Encode', background_color=rgba(232, 84, 250, 0.8), background_normal='')
        self.encode_button.bind(on_press=self.encode)
        self.add_widget(self.encode_button)
        self.decode_button = Button(text='Decode', background_normal='', background_color=rgba(26, 64, 202, 0.3))
        self.decode_button.bind(on_press=self.decode)
        self.add_widget(self.decode_button)
        self.exit_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1],
                                  background_color=rgba(65, 51, 137, 0.9), background_normal='')
        self.exit_button.bind(on_press=self.back)
        self.add_widget(self.exit_button)

    def back(self, instance):
        manager.transition.direction = "right"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "menu"

    def decode(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "dechex"

    def encode(self, instance):
        manager.transition.direction = "left"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "enchex"


class encodehex(GridLayout):
    def __init__(self, **kwargs):
        super(encodehex, self).__init__(**kwargs)

        self.cols = 1
        self.screen_title = TitleLabel(text="Encoding in Hex", color=[0, 1, 0, 1])

        self.secondary = GridLayout()
        self.secondary.cols = 2
        self.encode_msg = TitleLabel(text="Enter data to encode: ", color=[1, 0, 0, 1])
        self.secondary.add_widget(self.encode_msg)
        self.original = TextInput(foreground_color=[1, 0, 0, 1], background_color=[0, 0, 0, 1],
                                  hint_text="Enter your data here!", hint_text_color=[1, 0, 0, 0.5])

        self.add_widget(self.screen_title)
        self.secondary.add_widget(self.original)
        self.output = TitleLabel(text="Output: ", color=[0, 1, 0, 1])
        self.secondary.add_widget(self.output)
        self.out = TextInput(text="", foreground_color=[0, 1, 0, 1], background_color=[0, 0, 0, 1], readonly=True,
                             hint_text="The output will come here!", cursor_color=[0, 1, 0, 1],
                             hint_text_color=[0, 1, 0, 0.5], allow_copy=True)
        self.secondary.add_widget(self.out)
        self.submit_button = Button(text='Encode!', color=[0, 0, 1, 1], background_color=[0, 1, 0, 1],
                                    background_normal='')
        self.submit_button.disabled = True
        self.submit_button.bind(on_press=self.callback)
        self.secondary.add_widget(self.submit_button)
        self.copy_button = Button(text="Copy Output To Clipboard")
        self.copy_button.bind(on_press=self.copy)
        self.secondary.add_widget(self.copy_button)
        self.open_from_file = Button(text="Get input from file", on_press=self.file_picker)
        self.secondary.add_widget(self.open_from_file)
        self.save_to_file = Button(text="Save Output To File", on_press=lambda x: self.save_to_file_def())
        self.secondary.add_widget(self.save_to_file)
        self.back_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1], background_color=[0, 0, 1, 1],
                                  background_normal='')
        self.back_button.bind(on_press=self.back)
        self.secondary.add_widget(self.back_button)
        self.ok_button = Button(text="Open File",
                                on_press=lambda x: self.open(openFileDialog.GetPath()),
                                background_color=[1, 122 / 255, 0, 1], color=[0, 1, 0, 1])
        self.add_widget(self.secondary)
        self.ev = Clock.schedule_interval(lambda y: self.check(), 0.1)
        self.has_saved = True
        self.cs = Clock.schedule_interval(lambda y: self.checkSave(), 0.1)

    def callback(self, instance):
        self.new = binascii.hexlify(self.original.text.encode('utf-8')).decode("utf-8")
        if self.out.text != self.new:
            Clock.schedule_once(lambda x: self.send_to_firebase(), 0.4)
        self.out.text = self.new

    def send_to_firebase(self):
        app = MDApp.get_running_app()
        send1 = '{"enc_times":"%s", "total_times":"%s"}' % (
        str(app.stats["enc_times"] + 1), str(app.stats["total_times"] + 1))
        app.stats["enc_times"] += 1
        app.stats["total_times"] += 1
        if manager.screens[1].login_state == "in":
            req = requests.patch(
                "https://data-encoder-default-rtdb.firebaseio.com/" + manager.screens[1].localId + ".json?auth=" +
                manager.screens[1].idToken,
                data=send1)

    def back(self, instance):
        openFileDialog.SetFilename("")
        self.cs.cancel()
        self.ev.cancel()
        try:
            self.check_for_new.cancel()
        except:
            pass
        self.submit_button.disabled = True
        manager.transition.direction = "right"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "hexmenu"
        self.out.text = ""
        self.original.text = ""

    def copy(self, instance):
        Clipboard.copy(self.out.text)

    def file_picker(self, instance):
        openFileDialog.ShowModal()
        self.open(openFileDialog.GetPath())

        Window.raise_window()

    def open(self, filename):
        try:
            with open(filename) as f:
                self.original.text = f.read()
            s = Snackbar(text="Successfully imported data from file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                         snackbar_y="25dp",
                         snackbar_x="25dp")
            s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
            s.open()
        except:
            pass

    def save_to_file_def(self):
        if openFileDialog.GetFilename():
            saveFileDialog.SetFilename(f"{os.path.splitext(openFileDialog.GetFilename())[0]} Encoded.txt")
        else:
            saveFileDialog.SetFilename(f"Encoding {random.randint(0, 999999)}.txt")
        saveFileDialog.ShowModal()
        self.write_to_file(saveFileDialog.GetPath())

        Window.raise_window()
        if len(saveFileDialog.GetPath()) > 0:
            self.has_saved = True
            self.save_1 = self.original.text
            self.save_2 = self.out.text
            self.check_for_new = Clock.schedule_interval(lambda y: self.new_check(), 0.1)
        else:
            self.has_saved = False

    def write_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                f.write(self.out.text)
                f.close()
                s = Snackbar(text="Successfully exported data to file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                             snackbar_y="25dp",
                             snackbar_x="25dp")
                s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
                s.open()
        except:
            pass

    def check(self):
        if manager.current == "enchex":
            if len(self.original.text) > 0:
                if self.submit_button.disabled == True:
                    self.submit_button.disabled = False
                return
            self.submit_button.disabled = True

    def new_check(self):
        if self.save_1 != self.original.text or self.save_2 != self.out.text:
            self.has_saved = False
        else:
            self.has_saved = True

    def checkSave(self):
        if self.original.text != "" or self.out.text != "":
            self.has_saved = False


class ImageButton(ButtonBehavior, Image):
    pass


class changeAvatarScreen(MDScreen):
    pass


class decodehex(GridLayout):
    def __init__(self, **kwargs):
        super(decodehex, self).__init__(**kwargs)

        self.cols = 1
        self.screen_title = TitleLabel(text="Decoding in Hex", color=[0, 1, 0, 1])

        self.secondary = GridLayout()
        self.secondary.cols = 2
        self.encode_msg = TitleLabel(text="Enter data to decode: ", color=[1, 0, 0, 1])
        self.secondary.add_widget(self.encode_msg)
        self.original = TextInput(foreground_color=[1, 0, 0, 1], background_color=[0, 0, 0, 1],
                                  hint_text="Enter your data here!", hint_text_color=[1, 0, 0, 0.5])
        self.add_widget(self.screen_title)
        self.secondary.add_widget(self.original)
        self.output = TitleLabel(text="Output: ", color=[0, 1, 0, 1])
        self.secondary.add_widget(self.output)
        self.out = TextInput(text="", foreground_color=[0, 1, 0, 1], background_color=[0, 0, 0, 1], readonly=True,
                             hint_text="The output will come here!", cursor_color=[0, 1, 0, 1],
                             hint_text_color=[0, 1, 0, 0.5], allow_copy=True)
        self.secondary.add_widget(self.out)
        self.submit_button = Button(text='Decode!', color=[0, 0, 1, 1], background_color=[0, 1, 0, 1],
                                    background_normal='')
        self.submit_button.disabled = True
        self.submit_button.bind(on_press=self.callback)
        self.secondary.add_widget(self.submit_button)
        self.copy_button = Button(text="Copy Output To Clipboard")
        self.copy_button.bind(on_press=self.copy)
        self.secondary.add_widget(self.copy_button)
        self.open_from_file = Button(text="Get input from file", on_press=self.file_picker)
        self.secondary.add_widget(self.open_from_file)
        self.save_to_file = Button(text="Save Output To File", on_press=lambda x: self.save_to_file_def())
        self.secondary.add_widget(self.save_to_file)
        self.back_button = Button(text='Back', color=[255 / 255, 143 / 255, 0, 1], background_color=[0, 0, 1, 1],
                                  background_normal='')
        self.back_button.bind(on_press=self.back)
        self.secondary.add_widget(self.back_button)
        self.ok_button = Button(text="Open File",
                                on_press=lambda x: self.open(openFileDialog.GetPath()),
                                background_color=[1, 122 / 255, 0, 1], color=[0, 1, 0, 1])
        self.add_widget(self.secondary)
        self.ev = Clock.schedule_interval(lambda x: self.check(), 0.1)
        self.has_saved = True
        self.cs = Clock.schedule_interval(lambda y: self.checkSave(), 0.1)

    def callback(self, instance):
        try:
            self.new = binascii.unhexlify(self.original.text).decode("utf-8")
            if self.out.text != self.new:
                Clock.schedule_once(lambda x: self.send_to_firebase(), 0.4)
            self.out.text = self.new
        except Exception:
            layout = GridLayout(cols=1, padding=10)

            popupLabel = Label(text="Invalid Hex...", color=[1, 0, 0, 1])
            closeButton = Button(text="Close", background_color=[1, 0, 0, 1], color=[1, 1, 1, 1])
            closeButton.bind(on_press=self.close_popup)

            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)

            self.popup = Popup(title='Error',
                               content=layout, size_hint=(None, None), size=(700, 800), separator_color=[1, 0, 0, 1])
            self.popup.open()
            Clock.schedule_once(self.popup.dismiss, 10)

    def send_to_firebase(self):
        app = MDApp.get_running_app()
        send1 = '{"dec_times":"%s", "total_times":"%s"}' % (
        str(app.stats["dec_times"] + 1), str(app.stats["total_times"] + 1))
        app.stats["dec_times"] += 1
        app.stats["total_times"] += 1
        if manager.screens[1].login_state == "in":
            req = requests.patch(
                "https://data-encoder-default-rtdb.firebaseio.com/" + manager.screens[1].localId + ".json?auth=" +
                manager.screens[1].idToken,
                data=send1)

    def back(self, instance):
        openFileDialog.SetFilename("")
        self.cs.cancel()
        self.ev.cancel()
        try:
            self.check_for_new.cancel()
        except:
            pass
        self.submit_button.disabled = True
        manager.transition.direction = "right"
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.current = "hexmenu"
        self.out.text = ""
        self.original.text = ""

    def close_popup(self, instance):
        self.popup.dismiss()

    def copy(self, instance):
        Clipboard.copy(self.out.text)

    def file_picker(self, instance):
        openFileDialog.ShowModal()
        self.open(openFileDialog.GetPath())

        Window.raise_window()

    def open(self, filename):
        try:
            with open(filename) as f:
                self.original.text = f.read()
            s = Snackbar(text="Successfully imported data from file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                         snackbar_y="25dp",
                         snackbar_x="25dp")
            s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
            s.open()
        except:
            pass

    def save_to_file_def(self):
        if openFileDialog.GetFilename():
            saveFileDialog.SetFilename(f"{os.path.splitext(openFileDialog.GetFilename())[0]} Decoded.txt")
        else:
            saveFileDialog.SetFilename(f"Decoding {random.randint(0, 999999)}.txt")
        saveFileDialog.ShowModal()
        self.write_to_file(saveFileDialog.GetPath())

        Window.raise_window()
        if len(saveFileDialog.GetPath()) > 0:
            self.has_saved = True
            self.save_1 = self.original.text
            self.save_2 = self.out.text
            self.check_for_new = Clock.schedule_interval(lambda y: self.new_check(), 0.1)
        else:
            self.has_saved = False

    def write_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                f.write(self.out.text)
                f.close()
                s = Snackbar(text="Successfully exported data to file!", bg_color=(219 / 255, 10 / 255, 91 / 255, 1),
                             snackbar_y="25dp",
                             snackbar_x="25dp")
                s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
                s.open()
        except:
            pass

    def check(self):
        if manager.current == "dechex":
            if len(self.original.text) > 0:
                if self.submit_button.disabled == True:
                    self.submit_button.disabled = False
                return
            self.submit_button.disabled = True

    def new_check(self):
        if self.save_1 != self.original.text or self.save_2 != self.out.text:
            self.has_saved = False
        else:
            self.has_saved = True

    def checkSave(self):
        if self.original.text != "" or self.out.text != "":
            self.has_saved = False


class creditScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = [0, 0, 0, 1]
        self.add_widget(credits())


class encoderot13screen(MDScreen):
    def __init__(self, **kwargs):
        super(encoderot13screen, self).__init__(**kwargs)
        self.md_bg_color = [0, 0, 0, 1]
        self.cwass = encoderot13()
        self.add_widget(self.cwass)
        self.ids["class1"] = self.cwass
       

    def on_enter(self, *args):
        self.cwass.ev = Clock.schedule_interval(lambda x: self.cwass.check(), 0.1)
        self.cwass.cs = Clock.schedule_interval(lambda y: self.cwass.checkSave(), 0.1)
        titlebar.ids.dec_btn.disabled = True
        titlebar.ids.enc_btn.disabled = False
        

    


class decoderot13screen(MDScreen):
    def __init__(self, **kwargs):
        super(decoderot13screen, self).__init__(**kwargs)
        self.md_bg_color = [0, 0, 0, 1]
        self.cwass = decoderot13()
        self.add_widget(self.cwass)
        self.ids["class1"] = self.cwass
       

    def on_enter(self, *args):
        self.cwass.ev = Clock.schedule_interval(lambda x: self.cwass.check(), 0.1)
        self.cwass.cs = Clock.schedule_interval(lambda y: self.cwass.checkSave(), 0.1)
        titlebar.ids.dec_btn.disabled = False
        titlebar.ids.enc_btn.disabled = True

    


class rot13menuscreen(MDScreen):
    def __init__(self, **kwargs):
        super(rot13menuscreen, self).__init__(**kwargs)
        self.md_bg_color = [0, 0, 0, 1]
        Window.clearcolor = (1, 1, 1, 1)
        self.add_widget(rot13_menu())


class encodehexscreen(MDScreen):
    def __init__(self, **kwargs):
        super(encodehexscreen, self).__init__(**kwargs)
        self.md_bg_color = [0, 0, 0, 1]
        self.cwass = encodehex()
        self.add_widget(self.cwass)
        self.ids["class1"] = self.cwass
       

    def on_enter(self, *args):
        self.cwass.ev = Clock.schedule_interval(lambda x: self.cwass.check(), 0.1)
        self.cwass.cs = Clock.schedule_interval(lambda y: self.cwass.checkSave(), 0.1)
        titlebar.ids.dec_btn.disabled = True
        titlebar.ids.enc_btn.disabled = False
        

    


class decodehexscreen(MDScreen):
    def __init__(self, **kwargs):
        super(decodehexscreen, self).__init__(**kwargs)
        self.md_bg_color = [0, 0, 0, 1]
        self.cwass = decodehex()
        self.add_widget(self.cwass)
        self.ids["class1"] = self.cwass
       

    def on_enter(self, *args):
        self.cwass.ev = Clock.schedule_interval(lambda x: self.cwass.check(), 0.1)
        self.cwass.cs = Clock.schedule_interval(lambda y: self.cwass.checkSave(), 0.1)
        titlebar.ids.dec_btn.disabled = False
        titlebar.ids.enc_btn.disabled = True

    


class hexmenuscreen(MDScreen):
    def __init__(self, **kwargs):
        super(hexmenuscreen, self).__init__(**kwargs)
        self.md_bg_color = [0, 0, 0, 1]
        Window.clearcolor = (1, 1, 1, 1)
        self.add_widget(hex_menu())


class MenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.md_bg_color = [0, 0, 0, 1]
        self.check = False
        Window.clearcolor = (1, 1, 1, 1)
        self.p = Menu()
        self.add_widget(self.p)
        self.titlbar = menu1()
        self.add_widget(self.titlbar)

    def on_leave(self, *args):
        self.titlbar.ids['app_menu'].close_all()

    def on_enter(self, *args):
        if self.check == False:
            Clock.schedule_once(lambda x: self.check_log(), 2.2)
            self.check = True

    def check_log(self):
        if manager.screens[1].login_state == "in":
            s = Snackbar(text="Successfully logged in!", bg_color=(0, 0, 1, 1),
                         snackbar_y="25dp",
                         snackbar_x="25dp")
            s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
            s.open()


class encodeb64screen(MDScreen):
    def __init__(self, **kwargs):
        super(encodeb64screen, self).__init__(**kwargs)
        self.md_bg_color = [0, 0, 0, 1]
        self.cwass = encodeb64()
        self.add_widget(self.cwass)
        self.ids["class1"] = self.cwass
       

    def on_enter(self, *args):
        self.cwass.ev = Clock.schedule_interval(lambda x: self.cwass.check(), 0.1)
        self.cwass.cs = Clock.schedule_interval(lambda y: self.cwass.checkSave(), 0.1)
        titlebar.ids.dec_btn.disabled = True
        titlebar.ids.enc_btn.disabled = False
        

    


class b64menuscreen(MDScreen):
    def __init__(self, **kwargs):
        super(b64menuscreen, self).__init__(**kwargs)

        self.md_bg_color = [0, 0, 0, 1]
        self.add_widget(b64_menu())


class binmenuscreen(MDScreen):
    def __init__(self, **kwargs):
        super(binmenuscreen, self).__init__(**kwargs)
        self.md_bg_color = [0, 0, 0, 1]
        self.add_widget(bin_menu())


class decodeb64screen(MDScreen):
    def __init__(self, **kwargs):
        super(decodeb64screen, self).__init__(**kwargs)
        self.md_bg_color = [0, 0, 0, 1]
        self.cwass = decodeb64()
        self.add_widget(self.cwass)
        self.ids["class1"] = self.cwass
       

    def on_enter(self, *args):
        self.cwass.ev = Clock.schedule_interval(lambda x: self.cwass.check(), 0.1)
        self.cwass.cs = Clock.schedule_interval(lambda y: self.cwass.checkSave(), 0.1)
        titlebar.ids.dec_btn.disabled = False
        titlebar.ids.enc_btn.disabled = True
        

    


class GUI(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from firebaseloginscreen.firebaseloginscreen import FirebaseLoginScreen
        class loginScreen(FirebaseLoginScreen):
            def __init__(self, **kwargs):
                super().__init__()
                self.id = "firebase_login_screen"
                self.remember_user = True
                self.debug = False
                self.require_email_verification = True
                self.web_api_key = os.getenv("token")
                self.name = "login"

            def on_login_success(self, *args):
                if self.login_state == "in":
                    if manager.current == "login":
                        manager.current = "menu"
                        manager.transition.direction = "right"
                        manager.transition.duration = MDApp.get_running_app().trans_time
                        s = Snackbar(text="Successfully logged in!", bg_color=(0, 0, 1, 1),
                                     snackbar_y="25dp",
                                     snackbar_x="25dp")
                        s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
                        s.open()

                    self.r = UrlRequest(
                        url="https://data-encoder-default-rtdb.firebaseio.com/" + self.localId + ".json?auth=" + self.idToken,
                        on_success=lambda x, y: self.set_data(), ca_file=certifi.where(), req_body=None)

            def set_data(self):
                data_in_dict = self.r.result
                app = MDApp.get_running_app()
                app.stats = data_in_dict
                app.stats["enc_times"] = int(app.stats["enc_times"])
                app.stats["dec_times"] = int(app.stats["dec_times"])
                app.stats["total_times"] = int(app.stats["dec_times"])
                MDApp.get_running_app().trans_time = float(data_in_dict["trans_time"])
                manager.screens[-3].p.avatar.source = f'{app.stats["avatar"]}'
                if MDApp.get_running_app().stats["enc_times"] + MDApp.get_running_app().stats["dec_times"] != \
                        MDApp.get_running_app().stats["total_times"]:
                    MDApp.get_running_app().stats["total_times"] = MDApp.get_running_app().stats["enc_times"] + \
                                                                   MDApp.get_running_app().stats["dec_times"]

        global manager
        manager = ScreenManager(size_hint_y=0.96)
        manager.add_widget(splashScreen(name="splash"))
        manager.add_widget(loginScreen())
        manager.add_widget(encodeb64screen(name="encb64"))
        manager.add_widget(b64menuscreen(name="b64menu"))
        manager.add_widget(binmenuscreen(name="binmenu"))
        manager.add_widget(decodeb64screen(name="decb64"))
        manager.add_widget(decodebinscreen(name="decbin"))
        manager.add_widget(encodebinscreen(name="encbin"))
        manager.add_widget(rot13menuscreen(name="rot13menu"))
        manager.add_widget(encoderot13screen(name="encrot13"))
        manager.add_widget(decoderot13screen(name="decrot13"))
        manager.add_widget(encodehexscreen(name="enchex"))
        manager.add_widget(decodehexscreen(name="dechex"))
        manager.add_widget(hexmenuscreen(name="hexmenu"))
        manager.add_widget(MenuScreen(name="menu"))
        manager.add_widget(creditScreen(name="credits"))
        manager.add_widget(changeAvatarScreen(name="avatars"))
        manager.current = "splash"
        Window.clearcolor = (1, 1, 1, 1)
        self.add_widget(manager)
        global titlebar
        titlebar = menu1()
        self.ex = Clock.schedule_interval(lambda x: self.check(), 0.1)
        self.ev = Clock.schedule_interval(lambda x: self.check2(), 0.01)

    def check(self):
        if manager.current == "menu":
            self.add_widget(titlebar)
            Clock.unschedule(self.ex)
    def check2(self):
        if "enc" not in manager.current and "dec" not in manager.current:
            titlebar.ids.enc_btn.disabled = True
            titlebar.ids.dec_btn.disabled = True
            titlebar.ids.go_other.disabled = True
            titlebar.ids.back_to_main.disabled = False
        if "enc" in manager.current:
            titlebar.ids.enc_btn.disabled = False
            titlebar.ids.dec_btn.disabled = True
            titlebar.ids.go_other.disabled = False
            titlebar.ids.back_to_main.disabled = False
        if "dec" in manager.current:
            titlebar.ids.enc_btn.disabled = True
            titlebar.ids.dec_btn.disabled = False
            titlebar.ids.go_other.disabled = False
            titlebar.ids.back_to_main.disabled = False
        if manager.current == "menu":
            titlebar.ids.back_to_main.disabled = True
        if manager.screens[1].login_state == "in":
            titlebar.ids.logout.disabled = False
        if manager.screens[1].login_state == "" or manager.screens[1].login_state == "out":
            titlebar.ids.logout.disabled = True
        if manager.current == "login" or manager.current == "avatars":
            self.remove_widget(titlebar)




class encodebinscreen(MDScreen):
    def __init__(self, **kwargs):
        super(encodebinscreen, self).__init__(**kwargs)
        self.md_bg_color = [0, 0, 0, 1]
        self.cwass = encodebin()
        self.add_widget(self.cwass)
        self.ids["class1"] = self.cwass
       

    def on_enter(self, *args):
        self.cwass.ev = Clock.schedule_interval(lambda x: self.cwass.check(), 0.1)
        self.cwass.cs = Clock.schedule_interval(lambda y: self.cwass.checkSave(), 0.1)
        titlebar.ids.dec_btn.disabled = True
        titlebar.ids.enc_btn.disabled = False
        

    


class decodebinscreen(MDScreen):
    def __init__(self, **kwargs):
        super(decodebinscreen, self).__init__(**kwargs)

        self.md_bg_color = [0, 0, 0, 1]
        self.cwass = decodebin()

        self.add_widget(self.cwass)
        self.ids["class1"] = self.cwass
       

    def on_enter(self, *args):
        self.cwass.ev = Clock.schedule_interval(lambda x: self.cwass.check(), 0.1)
        self.cwass.cs = Clock.schedule_interval(lambda y: self.cwass.checkSave(), 0.1)
        titlebar.ids.dec_btn.disabled = False
        titlebar.ids.enc_btn.disabled = True

    


class Data_Encoder(MDApp):
    def __init__(self, **kwargs):
        super(Data_Encoder, self).__init__(**kwargs)

    def build(self):

        self.trans_time = 1
        self.stats = {"enc_times": 0, "dec_times": 0, "total_times": 0, "trans_time": 1}
        self.frame = wx.Frame(None, -1, 'win.py')
        self.frame.SetSize(0, 0, 500, 900)
        self.frame.SetBackgroundColour('black')
        self.frame.Hide()
        self.app1 = app
        self.exit_popup_open = False
        self.title = f"Data Encoder {version}"
        frame.SetSize(0, 0, 200, 50)
        Window.bind(on_request_close=self.on_request_closeing)
        self.theme_cls.theme_style = 'Dark'
        global top
        top = ScreenManager()
        top.add_widget(GUI(name="gui"))
        top.current = "gui"
        return top

    def on_request_closeing(self, instance):
        self.true_or_false = None
        if self.exit_popup_open == True:
            return True
        else:
            self.exit_popup_open = True
        if "enc" in manager.current or "dec" in manager.current:
            self.curr = manager.current_screen
            if not self.curr.ids.class1.has_saved:
                if self.curr.ids.class1.original.text or self.curr.ids.class1.out.text:
                    layout = GridLayout(cols=1, padding=10)
                    self.exit_app_btn = Button(text="Exit Application", color=[1, 0, 0, 1],
                                               background_color=[0, 0, 0, 1], on_press=lambda x: self.false(),
                                               background_normal="")
                    self.cancel_btn = Button(text="Cancel", color=[0, 1, 0, 1], background_color=[0, 0, 0, 1],
                                             on_press=lambda x: self.true())
                    self.save_then_ex = Button(text="Save To File Then Exit Application",
                                               on_press=lambda x: self.save_to(), color=[0, 1, 0, 1],
                                               background_color=[0, 0, 0, 1])
                    self.labl = Label(
                        text="Are you sure you want to exit? Your current data will not be saved unless you write it to a file.")
                    layout.add_widget(self.labl)
                    layout.add_widget(self.save_then_ex)
                    layout.add_widget(self.exit_app_btn)
                    layout.add_widget(self.cancel_btn)
                    self.popup = Popup(title='Exit Application?',
                                       content=layout, size_hint=(None, None), size=(1400, 1000),
                                       separator_color=[1, 0, 0, 1])
                    self.popup.open()
                    self.ev = Clock.schedule_once(lambda x: self.true(), 10)
                    return True

    def true(self):
        self.exit_popup_open = False
        self.popup.dismiss()
        Clock.unschedule(self.ev)

    def false(self):
        self.stop()


    def save_to(self):
        self.output = self.curr.ids.class1.out.text
        if openFileDialog.GetFilename():
            if self.root.current == "encb64" or "encbin" or "encrot13" or "enchex":
                saveFileDialog.SetFilename(f"{os.path.splitext(openFileDialog.GetFilename())[0]} Encoded.txt")
            else:
                saveFileDialog.SetFilename(f"{os.path.splitext(openFileDialog.GetFilename())[0]} Decoded.txt")
        else:
            if self.root.current == "encb64" or "encbin" or "encrot13" or "enchex":
                saveFileDialog.SetFilename(f"Encoding {random.randint(0, 999999)}.txt")
            else:
                saveFileDialog.SetFilename(f"Decoding {random.randint(0, 999999)}.txt")
        saveFileDialog.ShowModal()
        self.write_to_file(saveFileDialog.GetPath())

    def write_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                f.write(self.output)
                f.close()
                self.stop()
        except:
            Window.raise_window()
            self.popup.dismiss()
            Clock.unschedule(self.ev)
            self.exit_popup_open = False

    def on_start(self):
        avatar_grid = manager.screens[-1].ids["avatar_grid"]
        for root_dir, folders, files in os.walk("avatars"):
            for f in files:
                if f.endswith(".png"):
                    s = f"avatars/{f}"
                    img = ImageButton(source=s, on_release=partial(self.change_avatar, f))
                    avatar_grid.add_widget(img)
        manager.size_hint_y = 1
        Clock.schedule_once(lambda y: self.change_to_men(), 12)  # 12

    def change_avatar(self, widget_name, file):
        manager.screens[-3].p.avatar.source = file.source
        data = '{"avatar":"%s"}' % file.source
        req = requests.patch(
            "https://data-encoder-default-rtdb.firebaseio.com/" + manager.screens[1].localId + ".json?auth=" +
            manager.screens[1].idToken,
            data=data)
        self.go_to("menu", "right")

    def change_to_men(self):
        Window.hide()
        Window.borderless = False
        manager.current = "menu"
        manager.transition = NoTransition()
        Clock.schedule_once(lambda x: self.done(), 0.5)
        manager.transition = SlideTransition()

    def done(self):
        Window.unbind(on_resize=manager.screens[0].thing.rezise)
        Window.unbind(on_maximize=manager.screens[0].thing._pass)
        Window.maximize()
        Window.show()

    def go_to(self, x, direction="left"):
        manager.transition.direction = direction
        manager.transition.duration = MDApp.get_running_app().trans_time
        titlebar.ids['app_menu'].close_all()
        if manager.current == "login" or manager.current == "avatars":
            self.root.current_screen.add_widget(titlebar)
        manager.current = x

    def log(self):
        manager.transition.duration = self.trans_time
        manager.transition.direction = "left"
        manager.current = "login"

    def enc_clip(self):
        text = Clipboard.paste()
        class1 = manager.current_screen.cwass
        class1.original.text = text
        class1.callback("a")
        titlebar.ids['app_menu'].close_all()

    def go_to_other(self):
        titlebar.ids['app_menu'].close_all()
        manager.transition.duration = MDApp.get_running_app().trans_time
        manager.transition.direction = "up"
        manager.current_screen.cwass.original.text = ""
        manager.current_screen.cwass.out.text = ""
        if "enc" in manager.current:
            manager.current = manager.current.replace("enc", "dec")
        elif "dec" in manager.current:
            manager.transition.direction = "down"
            manager.current = manager.current.replace("dec", "enc")

    def back_to_main(self):
        titlebar.ids["app_menu"].close_all()
        if "enc" in manager.current or "dec" in manager.current:
            manager.current_screen.cwass.original.text = ""
            manager.current_screen.cwass.out.text = ""

        manager.transition.duration = self.trans_time
        manager.transition.direction = "right"
        manager.current = "menu"

    def logout(self):
        manager.screens[1].log_out()
        app = MDApp.get_running_app()
        app.stats = {"enc_times": 0, "dec_times": 0, "total_times": 0, "trans_time": 1}
        app.trans_time = 1
        manager.screens[-3].p.avatar.source = "avatars/man-1.png"
        s = Snackbar(text="Successfully logged out!", bg_color=(0, 0, 1, 1),
                     snackbar_y="25dp",
                     snackbar_x="25dp")
        s.size_hint_x = (Window.width - (s.snackbar_x * 2)) / Window.width
        s.open()




if __name__ == '__main__':
    Data_Encoder().run()







