from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.theming import ThemeManager
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
import deso
from kivy.properties import StringProperty
import pickle

#unpickles the user's profile
def unpickle_profile():
    with open('profile.pickle', 'rb') as handle:
        profile = pickle.load(handle)
        print("profile unpickled")
    return profile

#pickles the user's profile
def pickle_profile(profile):
    with open('profile.pickle', 'wb') as handle:
        pickle.dump(profile, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("profile pickled")


# Create the screen manager
sm = ScreenManager()

# Create the signup screen
class SignupScreen(Screen):
    pass

# Create the login screen
class LoginScreen(Screen):
    pass
# Create the username login screen
class UserNameLoginScreen(Screen):
    userName = StringProperty("")
    def textInput(self, widget):
        self.userName = widget.text
    def onClick(self):
        self.textInput(self.ids.username)
        desoUser = deso.User()
        profile = desoUser.getSingleProfile(username=self.userName).json()
        if 'error' in profile:
            toast(profile['error'])
        else:
            pickle_profile(profile)
            self.manager.current = 'homepage_read_only'

        
        sm.current = 'homepage_read_only'
        


# Create the homepage read only screen
class HomePageReadOnlyScreen(Screen):
    username = StringProperty("")
    def on_enter(self):
        profile = unpickle_profile()
        print(profile['Profile']['Username'])
        self.username = profile['Profile']['Username']


# Create the screen manager
sm = ScreenManager()
# Add the screens to the screen manager
sm.add_widget(SignupScreen(name='signup'))
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(UserNameLoginScreen(name='username_login'))
sm.add_widget(HomePageReadOnlyScreen(name='homepage_read_only'))


# Create the main app
class MainApp(MDApp):
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        screen = Builder.load_file('signup.kv')
        return screen

# Set the signup screen as the default
sm.current = 'login'        


# Run the app
if __name__ == '__main__':
    MainApp().run()