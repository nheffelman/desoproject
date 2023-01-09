from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.theming import ThemeManager
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
from kivymd.uix.card import MDCard
import deso
from kivy.properties import StringProperty
import pickle


# unpickles the user's profile
def unpickle_profile():
    with open('profile.pickle', 'rb') as handle:
        profile = pickle.load(handle)
        print("profile unpickled")
    return profile

# pickles the user's profile


def pickle_profile(profile):
    with open('profile.pickle', 'wb') as handle:
        pickle.dump(profile, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("profile pickled")


# Create the screen manager
sm = ScreenManager()

# class for the avatar circle


class CircularAvatarImage(MDCard):
    avatar = StringProperty()
    name = StringProperty()

# class for the story creator


class StoryCreator(MDCard):
    avatar = StringProperty()

# class for the post card


class PostCard(MDCard):
    profile_pic = StringProperty()
    avatar = StringProperty()
    username = StringProperty()
    post = StringProperty()
    caption = StringProperty()
    likes = StringProperty()
    comments = StringProperty()
    posted_ago = StringProperty()
    body = StringProperty()
    readmore = StringProperty()
    diamonds = StringProperty()
    repost = StringProperty()

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
    profile_picture = 'https://avatars.githubusercontent.com/u/89080192?v=4'
    username = StringProperty("")
    desoprice = StringProperty("")

    def on_enter(self):
        profile = unpickle_profile()
        print(profile['Profile']['Username'])
        self.username = profile['Profile']['Username']
        self.list_stories()
        self.list_posts()

    def list_stories(self):
        profile = unpickle_profile()
        desoMetadata = deso.Metadata()
        # getDiamondLevelMap takes optional inDesoNanos argument which is by default True.
        price = desoMetadata.getExchangeRate().json()
        # toast(str(price))
        dollars = price['USDCentsPerDeSoExchangeRate']/100
        # print(dollars)
        self.desoprice = str(dollars)
        # load 10 posts for the user or 10 posts for the stateless user
        if profile:
            print(profile['Profile']['PublicKeyBase58Check'])
            posts = deso.Posts()
            posts.readerPublicKey = profile['Profile']['PublicKeyBase58Check']

            userposts = posts.getPostsStateless(
                numToFetch=10, getPostsForGlobalWhitelist=True)
        else:
            userposts = deso.Posts().getPostsStateless(numToFetch=10)
        sm.current = 'username_login'
        print('anything?', userposts.json())
        for post in userposts.json()['PostsFound']:
            self.ids.stories.add_widget(CircularAvatarImage(
                avatar=deso.User().getProfilePicURL(
                    post['PosterPublicKeyBase58Check']),
                name=post['ProfileEntryResponse']['Username'],
                # avatar=data[name]['avatar'],
                # name=name,
                on_press=lambda x: self.toaster(
                    post['ProfileEntryResponse']['PublicKeyBase58Check'])

            ))

    def list_posts(self):
        profile = unpickle_profile()
        if profile:
            print(profile['Profile']['PublicKeyBase58Check'])
            posts = deso.Posts()
            posts.readerPublicKey = profile['Profile']['PublicKeyBase58Check']
            userposts = deso.Posts().getPostsStateless(numToFetch=10)
        else:
            userposts = deso.Posts().getPostsStateless(numToFetch=10)

        print(userposts)
        for post in userposts.json()['PostsFound']:
            readmore = ''
            if len(post['Body']) > 144:
                readmore = '  -- read more --'
            postImage = ''
            if post['ImageURLs']:
                postImage = post['ImageURLs'][0]
            self.ids.timeline.add_widget(PostCard(
                username=post["ProfileEntryResponse"]['Username'],

                avatar=deso.User().getProfilePicURL(
                    post['ProfileEntryResponse']['PublicKeyBase58Check']),
                likes=str(post['LikeCount']),
                comments=str(post['CommentCount']),
                body=str(post['Body']),
                readmore=readmore,
                post=postImage,
                diamonds=str(post['DiamondCount']),
                repost=str(post['RepostCount'])
            ))


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
