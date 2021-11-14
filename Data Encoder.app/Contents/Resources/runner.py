from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
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
from kivy.config import Config

with open("source.txt") as f:
    data = f.read()

n = int(data.replace(" ", ""), 2)
decoded = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

exec(decoded)