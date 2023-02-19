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


class PostScreen(Screen):
    profile_picture = StringProperty("")
    username = StringProperty("")
    desoprice = StringProperty("")
    postHashHex = StringProperty("")
    posted_ago = StringProperty("")

    
    def on_enter(self):    
        postHashHex = unpickle_post()
        post = deso.Posts().getSinglePost(postHashHex=postHashHex).json()
        print(post)
        profile = deso.User().getSingleProfile(publicKey=post['PostFound']['PosterPublicKeyBase58Check']).json()
        
        profile_picture = deso.User().getProfilePicURL(post['PostFound']['PosterPublicKeyBase58Check'])