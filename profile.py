#profile screen for the app

from linkpreview import link_preview
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.videoplayer import VideoPlayer
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.fitimage import FitImage
from kivymd.uix.swiper import MDSwiper, MDSwiperItem
from kivymd.uix.widget import MDWidget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.theming import ThemeManager
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.card import (
    MDCardSwipe, MDCardSwipeLayerBox, MDCardSwipeFrontBox, MDCard
)
from kivymd.uix.list import MDList, OneLineListItem, OneLineAvatarIconListItem, ImageLeftWidget, IconRightWidget
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRoundFlatButton, MDFillRoundFlatIconButton, MDRectangleFlatIconButton, MDIconButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.bottomsheet import MDListBottomSheet
import deso
from deso import Identity
from kivy.properties import StringProperty, ListProperty, BooleanProperty, ObjectProperty
import pickle
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem
import os
import re
from functools import lru_cache, wraps
from kivy.uix.widget import Widget

from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.videoplayer import VideoPlayer
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.fitimage import FitImage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.theming import ThemeManager
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRoundFlatButton, MDFillRoundFlatIconButton, MDRectangleFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.bottomsheet import MDListBottomSheet
import deso
from deso import Identity
from kivy.properties import StringProperty, ListProperty 
import pickle
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem
import os
