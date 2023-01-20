from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.theming import ThemeManager
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
import deso
from kivy.properties import StringProperty
import pickle

global currentPost 

#unpickles the current post
def unpickle_post():
    with open('post.pickle', 'rb') as handle:
        post = pickle.load(handle)
        print("post unpickled")
    return post
#pickles the current post
def pickle_post(post):
    with open('post.pickle', 'wb') as handle:
        pickle.dump(post, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("post pickled")

# unpickles the user's profile
def unpickle_profile():
    with open('profile.pickle', 'rb') as handle:
        profile = pickle.load(handle)
        #print("profile unpickled")
    return profile

# pickles the user's profile


def pickle_profile(profile):
    with open('profile.pickle', 'wb') as handle:
        pickle.dump(profile, handle, protocol=pickle.HIGHEST_PROTOCOL)
        #print("profile pickled")



# class for the avatar circle


class CircularAvatarImage(MDCard):
    avatar = StringProperty()
    name = StringProperty()

# class for the story creator


class StoryCreator(MDCard):
    avatar = StringProperty()

# class for the post card


class PostCard(MDCard):
    def on_post_click(self, postHashHex):
        pickle_post(postHashHex)
        self.sm.current = 'single_post_read_only'

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
    postHashHex = StringProperty()
    

# Create the signup screen


class SignupScreen(MDScreen):
    pass

# Create the login screen


class LoginScreen(MDScreen):
    pass
# Create the username login screen


class UserNameLoginScreen(MDScreen):
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

        self.current = 'homepage_read_only'

#create the single post read only screen
class SinglePostReadOnlyScreen(MDScreen):
    def on_enter(self):
        self.ids.singlePost.clear_widgets()
        self.list_post()

    def list_post(self):
        currentPost = unpickle_post()
        post = deso.Posts()
        post = post.getSinglePost(postHashHex=currentPost).json()
        
        #print(post)
        self.ids.username.text = post['PostFound']['ProfileEntryResponse']['Username']
        
        self.ids.singlePost.add_widget(PostCard(     
        username = post['PostFound']['ProfileEntryResponse']['Username'],
        post = post['PostFound']['PostHashHex'],
        caption = post['PostFound']['Body'],
        likes = str(post['PostFound']['LikeCount']),
        comments = str(post['PostFound']['CommentCount']),
        #posted_ago = post['PostFound']['PostEntryReaderState']['TimeAgo'],
        diamonds = str(post['PostFound']['DiamondCount']),
        repost = str(post['PostFound']['RecloutCount']),
        postHashHex = post['PostFound']['PostHashHex']
        ))
        
          

# Create the homepage read only screen
class HomePageReadOnlyScreen(MDScreen):
    profile_picture = 'https://avatars.githubusercontent.com/u/89080192?v=4'
    username = StringProperty("")
    desoprice = StringProperty("")
    
    def on_enter(self):
        self.ids.timeline.clear_widgets()
        profile = unpickle_profile()
        print(profile['Profile']['Username'])
        self.username = profile['Profile']['Username']
        self.list_stories()
        self.list_posts()

    #changes to the single read post screen
    def open_post(self, postHashHex):
        pickle_post(postHashHex)
        print('posthashhex was pickled', postHashHex)
        self.manager.current = 'single_post_read_only'

    def storie_switcher(self, publicKey):
        desoUser = deso.User()
        profile = desoUser.getSingleProfile(publicKey=publicKey).json()
        if 'error' in profile:
            toast(profile['error'])
        else:
            pickle_profile(profile)
        self.ids.stories.clear_widgets()
        self.ids.timeline.clear_widgets()
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

            userposts = posts.getPostsStateless(readerPublicKey=profile['Profile']['PublicKeyBase58Check'],
                numToFetch=10, getPostsForFollowFeed=True)
        else:
            userposts = deso.Posts().getPostsStateless(numToFetch=10)
        
        
        for post in userposts.json()['PostsFound']:
            self.ids.stories.add_widget(CircularAvatarImage(
                avatar=deso.User().getProfilePicURL(
                    post['PosterPublicKeyBase58Check']),
                name=post['ProfileEntryResponse']['Username'],
                # avatar=data[name]['avatar'],
                # name=name,
                on_press=lambda x: self.storie_switcher(
                    post['ProfileEntryResponse']['PublicKeyBase58Check'])

            ))

    def list_posts(self):
        profile = unpickle_profile()
        if profile:
            print(profile['Profile']['PublicKeyBase58Check'])
            posts = deso.Posts()
            posts.readerPublicKey = profile['Profile']['PublicKeyBase58Check']
            userposts = posts.getPostsStateless(readerPublicKey=profile['Profile']['PublicKeyBase58Check'],
                numToFetch=10, getPostsForFollowFeed=True)
        else:
            userposts = deso.Posts().getPostsStateless(numToFetch=10)

        
        for post in userposts.json()['PostsFound']:
            
            readmore = ''
            if len(post['Body']) > 144:
                readmore = '  -- read more --'
            postImage = ''
            if post['ImageURLs']:
                postImage = post['ImageURLs'][0]
            postcard=(PostCard(
                username=post["ProfileEntryResponse"]['Username'],

                avatar=deso.User().getProfilePicURL(
                    post['ProfileEntryResponse']['PublicKeyBase58Check']),
                postHashHex=str(post['PostHashHex']),
                likes=str(post['LikeCount']),
                comments=str(post['CommentCount']),
                body=str(post['Body']),
                readmore=readmore,
                post=postImage,
                diamonds=str(post['DiamondCount']),
                repost=str(post['RepostCount']),
            ))
            #bind the posthashhex to the postcard for each post in the timeline
            postcard.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
            self.ids.timeline.add_widget(postcard)



# Create the main app
class MainApp(MDApp):

    def build(self):
        # Set the theme
        self.theme_cls.theme_style = "Light"
        # Create the screen manager
        sm = ScreenManager()
        Builder.load_file('signup.kv')# Add the screens to the screen manager
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(UserNameLoginScreen(name='username_login'))
        sm.add_widget(HomePageReadOnlyScreen(name='homepage_read_only'))
        sm.add_widget(SinglePostReadOnlyScreen(name='single_post_read_only'))

        return sm

    



# Run the app
if __name__ == '__main__':
    MainApp().run()
