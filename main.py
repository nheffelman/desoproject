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
from kivy.uix.image import AsyncImage
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
from kivymd.uix.button import MDRoundFlatButton, MDFillRoundFlatIconButton, MDRectangleFlatIconButton, MDIconButton
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
from Post import SinglePostScreen
from profilescreen import ProfileScreen
from searchscreen import SearchScreen

global currentPost 
global loggedIn
global user
global publicKey 
global scrollIndex   
loggedIn = False
user = ""
publicKey = ""
scrollIndex = 0

#pickles the current settings
def pickle_settings(settings):
    with open('temp/settings.pickle', 'wb') as handle:
        pickle.dump(settings, handle, protocol=pickle.HIGHEST_PROTOCOL)


#unpickles the current settings
def unpickle_settings():
    if os.path.exists('temp/settings.pickle'):
        with open('temp/settings.pickle', 'rb') as handle:
            settings = pickle.load(handle)

    else:
        settings = {}  
    return settings

#unpickles the current post
def unpickle_post():
    if os.path.exists('temp/post.pickle'):
        with open('temp/post.pickle', 'rb') as handle:
            post = pickle.load(handle)

    else:
        post = {}
    return post
#pickles posts
def pickle_posts(posts):
    with open('temp/posts.pickle', 'wb') as handle:
        pickle.dump(posts, handle, protocol=pickle.HIGHEST_PROTOCOL)


#unpickles posts
def unpickle_posts():
    if os.path.exists('temp/posts.pickle'):
        with open('temp/posts.pickle', 'rb') as handle:
            posts = pickle.load(handle)

    else:
        posts = {}
    return posts
#pickles the current post
def pickle_post(post):
    
    with open('temp/post.pickle', 'wb') as handle:
        pickle.dump(post, handle, protocol=pickle.HIGHEST_PROTOCOL)


# unpickles the user's profile
def unpickle_profile():
    if os.path.exists('temp/profile.pickle'):
        with open('temp/profile.pickle', 'rb') as handle:
            profile = pickle.load(handle)

    else:
        profile = {}
    return profile

# pickles the user's profile
def pickle_profile(profile):

    if not os.path.exists('temp/'):
        os.makedirs('temp')
    with open('temp/profile.pickle', 'wb') as handle:
        pickle.dump(profile, handle, protocol=pickle.HIGHEST_PROTOCOL)

        
#simple custom caching function 
def cached(func):
    func.cache = {}
    @wraps(func)
    def wrapper(*args):
        try:
            return func.cache[args]
        except KeyError:
            func.cache[args] = result = func(*args)
            return result   
    return wrapper
   
@cached
def getCachedProfilePicUrl(key):
	avatar=deso.User().getProfilePicURL(key)
	return avatar
	
#pickles cache
def unpickle_profilePicUrl():
    if os.path.exists('temp/profilePicUrl.pickle'):
        with open('temp/profilePicUrl.pickle', 'rb') as handle:
            getCachedProfilePicUrl.cache = pickle.load(handle)

    else:
        getCachedProfilePicUrl.cache = {}
    return
 
#pickle profile pics cache
def pickle_profilePicUrl(cache):
    if not os.path.exists('temp/'):
        os.makedirs('temp/')
    with open('temp/profilePicUrl.pickle', 'wb') as handle:
        pickle.dump(cache, handle, protocol=pickle.HIGHEST_PROTOCOL)
        toast("profile pic url pickled")

#on start up load càched profile pic urls   
unpickle_profilePicUrl()

class RecloutLayout(MDBoxLayout):
	pass           

class BodyLabel(ButtonBehavior, MDLabel):
    pass

#class for custom comment dialog content
class CommentContent(MDBoxLayout):
    comment = StringProperty()

#class for custom dialog content
class Content(MDBoxLayout):
    quote = StringProperty()

#class for custom nft dialog content
class NFTContent(MDBoxLayout):
    bid = StringProperty()
    nftImage = StringProperty()
    numNftCopies = StringProperty()
    numNftCopiesForSale = StringProperty()
    nftTitle = StringProperty()


# class for Item
class Item(OneLineAvatarListItem):
    divider = None
    source = StringProperty()

# class for the avatar circle
class CircularAvatarImage(MDCard):
    avatar = StringProperty()
    name = StringProperty()

# class for the story creator


class StoryCreator(MDCard):
    avatar = StringProperty()

class PostLayout(MDBoxLayout):
    
    postHashHex = StringProperty()

class Reactions(MDBoxLayout):
    
    liked = BooleanProperty()
    likes = StringProperty()
    comments = StringProperty()
    posted_ago = StringProperty()
    diamonded = BooleanProperty()
    diamonds = StringProperty()
    reclouted = BooleanProperty()
    reclout = StringProperty()
    
# class for the post card
class PostCard(MDBoxLayout):
    def on_post_click(self, postHashHex):
        pickle_post(postHashHex)
        self.sm.current = 'single_post'

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
    reclout = StringProperty()
    postHashHex = StringProperty()
    posted_ago = StringProperty()
    video = StringProperty()
    

#class for the repost card
class RePostCard(MDBoxLayout):
    def on_post_click(self, postHashHex):
        pickle_post(postHashHex)
        self.sm.current = 'single_post'
    profile_pic = StringProperty()
    repostAvatar = StringProperty()
    repostUsername = StringProperty()
    repostBody = StringProperty()
    postHashHex = StringProperty()
    avatar =StringProperty()
    username = StringProperty()
    body = StringProperty()
    likes = StringProperty()
    diamonds = StringProperty()
    reclout = StringProperty()
    comments = StringProperty()
    repostPostHashHex = StringProperty()
    repostPost= StringProperty()
    repostVideo = StringProperty()


    
# Create the signup screen
class SignupScreen(MDScreen):
    pass

# Create the login screen
class LoginScreen(MDScreen):
    pass

#create the login with seed phrase screen
class SeedLoginScreen(MDScreen):
    seedPhrase = StringProperty("")
    userName = StringProperty("")

    def textInput(self, widget):
        self.seedPhrase = widget.text
        
    def nameInput(self, widget):
        self.userName = widget.text

    def onClick(self):
        self.textInput(self.ids.seedphrase)
        self.nameInput(self.ids.userName)
        seedphrase = self.seedPhrase
        if len(seedphrase.split()) != 12:
            toast("Seed phrase must have 12 words")
            return
        #try to get seed hex from seed phrase catch error if seed phrase is invalid
        try:        
            SEED_HEX = Identity.getSeedHexFromSeedPhrase(seedphrase)
        except:
            toast("Invalid seed phrase")
            return
        #get user profile and pickle it
        desoUser = deso.User()
        profile = desoUser.getSingleProfile(username=self.userName).json()

        if 'error' in profile:
            toast(profile['error'])
        #if no error in profile get user identity and make a derived key for signing transactions    
        else:
            settings = {}
            desoIdentity = deso.Identity(publicKey=profile['Profile']['PublicKeyBase58Check'], seedHex=SEED_HEX)
            pickle_profile(profile)
            global user
            global loggedIn
            global publicKey
            loggedIn = True
            user=self.userName
            publicKey=profile['Profile']['PublicKeyBase58Check']
            
            settings['user'] = self.userName
            settings['loggedIn'] = True
            settings['seedHex'] = SEED_HEX
            settings['publicKey'] = publicKey
            

            pickle_settings(settings)

            self.manager.current = 'homepage_read_only'

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
            global user
            global loggedIn
            loggedIn = False
            user=self.userName
            settings = {}
            settings['user'] = self.userName
            settings['loggedIn'] = False
            pickle_settings(settings)
            self.manager.current = 'homepage_read_only'
            
        self.current = 'homepage_read_only'

# Create the homepage read only screen
class HomePageReadOnlyScreen(MDScreen):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

    profile_picture = StringProperty("") #'https://avatars.githubusercontent.com/u/89080192?v=4'
    username = StringProperty("")
    desoprice = StringProperty("")
    avatar = StringProperty("")
    dialog = None
    follow_unfollow = StringProperty("")
    
    def on_enter(self):
        
        profile = unpickle_profile()
        settings = unpickle_settings()
        if 'trending' in settings:
            if settings['trending'] == True:
                self.ids.trending.md_bg_color = "blue"
        else: 
            settings['trending'] = False
            self.ids.following.md_bg_color = "blue"
        pickle_settings(settings)


        username=profile['Profile']['Username']
        self.username = profile['Profile']['Username']
        self.profile_picture = deso.User().getProfilePicURL(
                    profile['Profile']['PublicKeyBase58Check'])
        if not self.ids.timeline.children:
        	
        	self.list_stories()
        	self.list_posts()



    def logout(self):
        settings = {}
        
        pickle_settings(settings)
        global loggedIn
        loggedIn = False
        self.manager.current = 'login'

    #changes to the single read post screen
    def open_post(self, postHashHex):
        pickle_post(postHashHex)

        self.manager.current = 'single_post'

    def home(self):
        settings = unpickle_settings()
        profile = unpickle_profile()
        #change profile and user back to logged in user
        if 'loggedIn' in settings:
            if settings['loggedIn'] == True:
                if 'publicKey' in settings:
                    profile = deso.User().getSingleProfile(publicKey=settings['publicKey']).json()
                    pickle_profile(profile)
                    global loggedIn
                    loggedIn = True
                    self.ids.stories.clear_widgets()
                    self.ids.timeline.clear_widgets()
                    self.profile_picture = getCachedProfilePicUrl(settings['publicKey'])
                    self.list_stories()
                    self.list_posts()
                    self.manager.current = 'homepage_read_only'


    def storie_switcher(self, publicKey):
        desoUser = deso.User()
        profile = desoUser.getSingleProfile(publicKey=publicKey).json()
        if 'error' in profile:
            toast(profile['error'])
        else:
            pickle_profile(profile)
        self.profile_picture = str(getCachedProfilePicUrl(publicKey))
        self.ids.stories.clear_widgets()
        self.ids.timeline.clear_widgets()
        self.list_stories()
        self.list_posts()
        
    #like a post function allows user to like a post, toggles icon to red, updates the like count, and sends a like to the blockchain    
    def like(self, postHashHex, liked, reactions):
        global loggedIn
        if loggedIn != True:
            toast('You must be logged in to like a post')
        else:
            settings=unpickle_settings()

            if settings['loggedIn'] == True:
                              
                if reactions.liked == True:
                    reactions.ids.like.icon = 'heart-outline'
                    reactions.ids.likes.text = str(int(reactions.ids.likes.text) - 1)
                    reactions.liked = False
                    SEED_HEX = settings['seedHex']
                    PUBLIC_KEY = settings['publicKey']
                    desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
                    response = desoSocial.like(postHashHex=postHashHex, isLike=False)
                    print(response.json())

                else:
                    reactions.ids.like.icon = 'heart'
                    reactions.ids.likes.text = str(int(reactions.ids.likes.text) + 1)
                    reactions.liked = True
                    SEED_HEX = settings['seedHex']
                    PUBLIC_KEY = settings['publicKey']
                    desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
                    response = desoSocial.like(postHashHex=postHashHex, isLike=True)
                    print(response.json())


    #when a user presses comment, opens a dialog box to allow user to comment on a post
    def comment(self, postHashHex, reactions):
        global loggedIn
        if loggedIn != True:
            toast('You must be logged in to comment a post')
        else:
            settings=unpickle_settings()
            if settings['loggedIn'] == True:

                
                self.dialog = None
                if not self.dialog:
                    self.dialog = MDDialog(
                        auto_dismiss=False,
                        pos_hint={"center_x": 0.5, "center_y": .8},
                        size_hint=(0.8, 0.6),
                        title="Comment",
                        type="custom",
                        content_cls=CommentContent(),
                        buttons=[
                            MDRoundFlatButton(
                                text="CANCEL", on_release=lambda widget: self.dialog.dismiss()
                            ),
                            MDRoundFlatButton(
                                text="COMMENT", on_release= lambda widget, postHashHex=postHashHex: self.postComment(postHashHex, reactions)
                            )],
                        
    
                    )
                    self.dialog.open()

    def postComment(self, postHashHex, reactions):    

            
        settings=unpickle_settings()
        SEED_HEX = settings['seedHex']
        PUBLIC_KEY = settings['publicKey']
        desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
        comment_response = desoSocial.submitPost(parentStakeID=postHashHex, body=self.dialog.content_cls.ids.comment.text, ).json()
        print(comment_response)
        self.dialog.dismiss()
        self.dialog = None
        if 'error' in comment_response:
            return False
        else:
            reactions.comments = str(int(reactions.comments) + 1)
            


    #diamond a post function allows user to like a post, toggles icon to red, updates the like count, and sends a diamond to the blockchain
    def diamond(self, postHashHex, diamonded, reactions):
        global loggedIn
        if loggedIn != True:
            toast('You must be logged in to diamond a post')
        else:
            settings=unpickle_settings()
            if settings['loggedIn'] == True:

                PUBLIC_KEY = settings['publicKey']
                post = deso.Posts()
                post.readerPublicKey = PUBLIC_KEY
                post = post.getSinglePost(postHashHex=postHashHex).json()

                if post['PostFound']['PosterPublicKeyBase58Check']:
                    SEED_HEX = settings['seedHex']
                    receiverPublicKey = post['PostFound']['PosterPublicKeyBase58Check']
                    if receiverPublicKey != PUBLIC_KEY:
                        if reactions.diamonded == False:
                            desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
                            response = desoSocial.diamond(postHashHex=postHashHex, receiverPublicKey=receiverPublicKey)
                            print(response.json())
                            reactions.ids.diamond.icon = 'diamond'
                            reactions.diamonds = str(int(reactions.diamonds) + 1)
                            reactions.diamonded = True
                        else:
                            toast('You have already diamonded this post')
                    else: 
                        toast('You cannot diamond your own post')

                
    #use a MDDIalog to ask user if they want to repost or quote post
    def clout_or_quoteclout_dialog(self, postHashHex, reactions):
        if not self.dialog:
            self.dialog = MDDialog(
            title="Would you like to reclout or quoteclout this post?",
            type="simple",
            items=[
                Item(text="ReClout", source="assets/reclout.png", on_release= lambda *x: self.recloutpressed(postHashHex, reactions)),
                Item(text="QuoteClout", source="assets/quoteclout.png", on_release= lambda *x: self.quotecloutpressed(postHashHex, reactions)),
            ],
            )
            self.dialog.open()

    # if user selects quoteclout, open a dialog box to enter a quote, else return error to reclout function
    def quotecloutpressed(self, postHashHex, reactions):
        self.dialog.dismiss()
        self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
            title="Enter a quote",
            type="custom",
            content_cls=Content(),
            buttons=[
                MDRoundFlatButton(text="CANCEL", on_release=lambda widget: self.dialog.dismiss()),
                MDRoundFlatButton(text="QUOTE", on_release= lambda *x: self.quoteclout(postHashHex, reactions)),
            ],
            )
            self.dialog.open()

    #if user selects quoteclout, send a quoteclout to the blockchain and close the dialog box, else return error to reclout function
    def quoteclout(self, postHashHexToQuote, reactions):
        
        settings=unpickle_settings()
        SEED_HEX = settings['seedHex']
        PUBLIC_KEY = settings['publicKey']
        desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
        
        quoteclout_response = desoSocial.quote(postHashHexToQuote=postHashHexToQuote, body=self.dialog.content_cls.ids.quote.text, ).json()
        self.dialog.dismiss()
        self.dialog = None
        print(quoteclout_response)
        if 'error' in quoteclout_response:
            return False
        else:
            reactions.ids.reclout.icon = 'repeat-variant'
            reactions.reclouted = str(int(reactions.reclouted) + 1)       

    #if user selects reclout, send a reclout to the blockchain and close the dialog box, else return error to reclout function
    def recloutpressed(self, postHashHexToRepost, reactions):

        self.dialog.dismiss()
        self.dialog = None
        settings=unpickle_settings()
        SEED_HEX = settings['seedHex']
        PUBLIC_KEY = settings['publicKey']
        desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
        reclout_response = desoSocial.repost(postHashHexToRepost).json(), 'repost response'
        print(reclout_response)

        if 'error' in reclout_response:
            return False
        else:
            reactions.ids.reclout.icon = 'repeat-variant'
            reactions.reclouted = str(int(reactions.reclouted) + 1)       


    #reclout a post function allows user to reclout a post, toggles icon reposted, updates the reclout count, and sends a reclout to the blockchain        
    def reclout(self, postHashHex, reactions):
        global loggedIn
        if loggedIn != True:
            toast('You must be logged in to reclout a post')
        else:
            settings=unpickle_settings()
            if settings['loggedIn'] == True:

                if self.clout_or_quoteclout_dialog(postHashHex, reactions) == False:
                    toast('An error occured reclouting this post')
                else:
                    #update the icon and reclout count
                    reactions.ids.reclout.icon = 'repeat-variant'
                    reactions.reclout = str(int(reactions.reclout) + 1)                        
                            
    def unfollow(self, whoToUnfollow):
        settings=unpickle_settings()
        SEED_HEX = settings['seedHex']
        PUBLIC_KEY = settings['publicKey']
        desoSocial = deso.Social(nodeURL="https://diamondapp.com/api/v0/", publicKey=PUBLIC_KEY, seedHex=SEED_HEX)   
        response = desoSocial.follow(whoToUnfollow, isFollow=False).json() 
        print(response)
    
    def follow(self, whoToFollow):
        settings=unpickle_settings()
        SEED_HEX = settings['seedHex']
        PUBLIC_KEY = settings['publicKey']
        desoSocial = deso.Social(nodeURL="https://diamondapp.com/api/v0/", publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
        response = desoSocial.follow(whoToFollow, isFollow=True).json() 
        print(response)
        
    def callback_for_menu_items(self, *args):
        toast(args[0])
        if args[0] == "Follow":
            self.follow(args[1])
        elif args[0] == "Unfollow":
            self.unfollow(args[1])
        elif args[0] == "View Feed":
            self.storie_switcher(args[1])
            
    #function to change 3dots data(self, following)
    def change_3dots_data(self, following):
        if following == True:
            data = {
            "Unfollow": "account-minus",
            "View Feed": "account-eye",
            "Report": "alert-circle",
            "Cancel": "cancel",
            }
        else:
            data = {
            "Follow": "account-plus",
            "View Feed": "account-eye",
            "Report": "alert-circle",
            "Cancel": "cancel",
            }
        return data

    def toast_3dots(self, data, posterPublicKey):
        
        bottom_sheet_menu = MDListBottomSheet()
        data = data
        for item in data.items():
            bottom_sheet_menu.add_item(
                item[0],    
                lambda x, y=item[0], posterPublicKey=posterPublicKey: self.callback_for_menu_items(y, posterPublicKey),
                icon=item[1],
                

            )
                
        bottom_sheet_menu.open()

            
    #function for nft modal
    def open_nft_modal(self, postHashHex, nftImageURL, numNftCopiesForSale, numNftCopies, nftTitle):
        self.nftmodal = MDDialog(
            title=nftTitle,
            type="custom",
            content_cls=NFTContent(nftImage = nftImageURL, numNftCopiesForSale = numNftCopiesForSale, numNftCopies = numNftCopies),
            
            buttons=[
                MDRoundFlatButton(text="CANCEL", on_release=lambda widget: self.nftmodal.dismiss()),
                MDRoundFlatButton(text="BUY", on_release= lambda widget, postHashHex=postHashHex: self.buy_nft(postHashHex)),
            ],
        )
        self.nftmodal.open()
    def buy_nft(self, postHashHex):
        pass

    def slideout_profile_pressed(self):
        settings = unpickle_settings()
        if 'publicKey' in settings:
            settings['profileKey'] = settings['publicKey']
            pickle_settings(settings)
            self.manager.current = 'profile'
        else:
            toast('You must be logged in to view your profile')

    def user_profile_pressed(self, profileKey):
        setting = unpickle_settings()
        setting['profileKey'] = profileKey
        pickle_settings(setting)
        self.manager.current = 'profile'
        

    def profile_pressed(self, profileKey):
        setting = unpickle_settings()
        setting['profileKey'] = profileKey
        pickle_settings(setting)
        self.manager.current = 'profile'

    def trending_pressed(self):
        settings = unpickle_settings()
        settings['trending'] = True
        pickle_settings(settings)
        self.ids.trending.md_bg_color = "blue"
        self.ids.following.md_bg_color = "white"
        self.ids.timeline.clear_widgets()
        self.list_posts()

    def following_pressed(self):
        settings = unpickle_settings()
        settings['trending'] = False
        pickle_settings(settings)
        self.ids.trending.md_bg_color = "white"
        self.ids.following.md_bg_color = "blue"
        self.ids.timeline.clear_widgets()
        self.list_posts()

    def list_stories(self):
        
        profile = unpickle_profile()
        desoMetadata = deso.Metadata()
        # getDiamondLevelMap takes optional inDesoNanos argument which is by default True.
        price = desoMetadata.getExchangeRate().json()
        # toast(str(price))
        dollars = price['USDCentsPerDeSoExchangeRate']/100

        self.desoprice = str(dollars)
        # load 10 posts for the user or 10 posts for the stateless user
        posts = deso.Posts()
        if profile:

            posts.readerPublicKey = profile['Profile']['PublicKeyBase58Check']
            userposts = posts.getPostsStateless(numToFetch=10, getPostsForFollowFeed=True)
        else:
            posts.reaerPublicKey = None
            userposts = deso.Posts().getPostsStateless(numToFetch=10)
        
        
        for post in userposts.json()['PostsFound']:
            circle=CircularAvatarImage(
                avatar=getCachedProfilePicUrl(post['PosterPublicKeyBase58Check']),
                #name=post['ProfileEntryResponse']['Username'],
                )
            circle.bind(on_press=lambda widget, userid=post['ProfileEntryResponse']['PublicKeyBase58Check']: self.storie_switcher(userid))
            self.ids.stories.add_widget(circle)

    #monitors the scrollview and calls refresh when it reaches the bottom
    def touch_up_value(self, *args):

        if self.ids.mainScrollView.scroll_y  <= 0:
            toast('refreshing')
            if self.ids.timeline.children:
                self.refresh_posts(target_widget=self.ids.timeline.children[-1])
    
    #pickles ref and sets the current screen search                   
    def ref_pressed(self, ref):
        settings = unpickle_settings()
        settings['ref'] = ref
        pickle_settings(settings)
        self.manager.current = 'search'
        
    def refresh_posts(self, target_widget=None):
        
        self.ids.timeline.clear_widgets()
        trigger = Clock.create_trigger(self.list_posts())
        trigger()
        self.ids.mainScrollView.scroll_y = 1
        #self.ids.mainScrollView.scroll_to(target_widget)



      #  scrollIndex += 10
        #Clock.schedule_once(lambda *x : self.ids.mainScrollView.scroll_y(1))

    def get_posts(self):
        profile = unpickle_profile()
        print(profile)
        settings = unpickle_settings()
        cached_posts = unpickle_posts()
        

        #get the users following list
        following = []
        if 'publicKey' in settings:
            desoUser = deso.User()
            followingResponse = desoUser.getFollowsStateless(publicKey = settings['publicKey']).json()
            for publicKey in followingResponse['PublicKeyToProfileEntry']:
                        following.append(publicKey)      

        profileKey = None
        userKey = None
        viewerKey = None

        #get the current viewers public key            
        profileKey = profile['Profile']['PublicKeyBase58Check']
        print('profilekey is ' + profileKey)

        #get the current users public key
        if 'publicKey' in settings:
            userKey = settings['publicKey']   
            print('userkey is ' + userKey)

        #if user is viewing his own feed
        if profileKey != None and userKey != None and profileKey == userKey:
            #check to see if trending is selected
            print('checking if trending is selected or following')
            if 'trending' in settings:
                print('settings trending = ', settings['trending'])
                if settings['trending'] == True:
                    self.ids.trending.md_bg_color = "blue"
                    viewerKey = 'trending'
                    print('trending is selected')
                else: 
                    #following is selected, get the following list for the chosen viewer
                    self.ids.following.md_bg_color = "blue" 
                    viewerKey = userKey 
                    print('following is selected for userkey')
            else:
                #following is selected, get the following list for the chosen viewer
                self.ids.following.md_bg_color = "blue" 
                viewerKey = userKey 
                print('following is selected for userkey')

        #if user is viewing someone elses feed or is not logged in
        else: 
            #get the public key of the profile being viewed or  select trending if no profile is selected
            if profileKey:                
                viewerKey = profileKey
                print('user is viewing someone elses feed')
            else:
                viewerKey = 'trending'
                print('user is not logged in')

        #check to see if there are any cached posts
        if viewerKey in cached_posts:
            print('cached posts found')
            userposts = []
            reversed = cached_posts[viewerKey]
            reversed.reverse()
            #iterate through the cached posts and add them to the userposts list
            for i in range(9):
                if reversed != []:
                    userposts.append(reversed.pop())
            #if there are more posts in the cache then reverse the list and save it to the cache
            if len(reversed) > 0:
                reversed.reverse()
                cached_posts[viewerKey] = reversed
                pickle_posts(cached_posts)
            #else remove the viewer key from the cache
            else:
                del cached_posts[viewerKey]
                pickle_posts(cached_posts)

        #if there are no cached posts
        else:
            print('no cached posts found')
            #if the viewer key is trending
            if viewerKey == 'trending':
                print('trending')
                #get trending posts for the stateless user
                posts = deso.Posts()
                posts.readerPublicKey = None
                userposts = posts.getHotFeed(responseLimit=100).json()['HotFeedPage']
                print(userposts)
                
                #save the posts to the cache
                cached_posts[viewerKey] = userposts[9:]
                pickle_posts(cached_posts)
                #get the first 9 posts
                userposts = userposts[:9]
            #if the viewer key is a public key
            else:
                print('following')
                #get the posts for the viewer key
                posts = deso.Posts()
                posts.readerPublicKey = viewerKey
                userposts = posts.getPostsStateless(getPostsForFollowFeed=True, numToFetch=100).json()['PostsFound']
                #save the posts to the cache
                cached_posts[viewerKey] = userposts[9:]
                pickle_posts(cached_posts)
                #get the first 9 posts
                userposts = userposts[:9]
                      
            
        return userposts,following
    
    def list_posts(self):
               
        userposts, following = self.get_posts()
        
        for post in userposts:

            #If this is a repost of another post, get the original post and extra body text
            nftImage = ''
            if post['IsNFT']:
                pass
            
            #layout for the post
            layout = PostLayout(orientation='vertical', size_hint_x = 1, adaptive_height = True, postHashHex=str(post['PostHashHex']),)
            #layout for the post header
            header = MDBoxLayout(orientation='horizontal', adaptive_height=True, size_hint_x = 1)
            #one line avatar list item
            username=str(post["ProfileEntryResponse"]['Username'])
            avatar = getCachedProfilePicUrl(post['ProfileEntryResponse']['PublicKeyBase58Check'])
            #avatar=deso.User().getProfilePicURL(
                    #post['ProfileEntryResponse']['PublicKeyBase58Check'])

            olali = OneLineAvatarListItem(text=username, divider = None, _no_ripple_effect = True)
            ilw = ImageLeftWidget(source=avatar, radius = [20, ])         
            ilw.bind(on_press=lambda widget, profileKey = post['ProfileEntryResponse']['PublicKeyBase58Check']: self.user_profile_pressed(profileKey))
                                 
            #add the avatar to the list item
            olali.add_widget(ilw)
            
            #add the three dots to the header
            #add data to dots menu 
            if post['PosterPublicKeyBase58Check'] in following:
                data = self.change_3dots_data(following=True)
            else:
                data = self.change_3dots_data(following=False)
            three_dots = MDIconButton(icon='dots-vertical')
            
            three_dots.bind(on_press=lambda widget, data=data, post=post: self.toast_3dots(data, post['PosterPublicKeyBase58Check']))
            
            #add the one line avatar list item to the header
            header.add_widget(olali)
            header.add_widget(three_dots)
            
            #add the header to the layout
            layout.add_widget(header)
            layout.height += header.height
            
            body=str(post['Body'])

            #get the post body hotlinks            
            newText = []
            textList = body.split()
            for i in textList:
            	if(i.startswith("#")) or (i.startswith("@")):
            		i = i.replace(i, ('[ref='+i+'][color=0000ff]'+i+'[/color][/ref]'))
            	newText.append(i)
            	
            body = ' '.join(newText)
	
            urls = re.findall(r'(https?://[^\s]+)', body)

            #separate the links from the body text make labels for the text and cards for the links, then add them to the layout
            previewHeight = 0
            for url in urls:
                beforeUrl = body.split(url,1)[0]

                if beforeUrl !='':
                    bodyLabel = BodyLabel(text=beforeUrl, padding=[20, 20], markup = True)
                    bodyLabel.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex),
                                    on_ref_press = lambda widget, ref: self.ref_pressed(ref))
                    layout.add_widget(bodyLabel)
                    layout.height += bodyLabel.height

                body = body.split(url,1)[1] 
                
                try:
                    preview = link_preview(url)
                except:
                    preview = None
                if preview:
                    
                    if preview.image:

                        preview_image = MDCard(size_hint_y=None, height=450, radius=[18,0])
                        aImage = AsyncImage(source=preview.image, allow_stretch=True, keep_ratio=True)
                        preview_image.add_widget(aImage)
                        preview_image.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))

                        if preview.title:
                            title = MDLabel(text=preview.title, halign =  "center", font_style = 'H6')
                            preview_image.add_widget(title)
                            
                        
                        layout.add_widget(preview_image)    
                        layout.height += preview_image.height
                else:
                    urlLabel = MDLabel(text=url, halign =  "center" )
                    layout.add_widget(urlLabel)
                    layout.height += urlLabel.height
                    previewHeight -= 250
            #add any remaining body to the layout
            if body != '':
                bodyLabel = BodyLabel(text=body, padding= [20,20], markup = True)
                bodyLabel.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex),
                                    on_ref_press = lambda widget, ref: self.ref_pressed(ref))
            	#add the body card to the layout
                layout.add_widget(bodyLabel)
                layout.height += bodyLabel.height
            
            #create a card for the post Image
            postImage = ''
            imageHeight = 0
            if post['ImageURLs']:                 
                
                #swiper = MDSwiper(swipe_on_scroll = True, size_hint_y = None, height = 300, radius=(18, 18,18, 18), ) 
                for image in post['ImageURLs']:
                    card = MDCard(size_hint_y=None, height=450, radius=[18,0])
                    aImage = AsyncImage(source=image, allow_stretch=True, keep_ratio=True)
                    card.add_widget(aImage)
                    
                    card.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
                    #swiperBox.add_widget(swiper)
                    
                    layout.add_widget(card)
                    layout.height += card.height 
            if post['VideoURLs']:


                postVideo = post['VideoURLs'][0]
                player = VideoPlayer(size_hint_y = None, source=postVideo, state='pause', options={'allow_stretch': True})
                player.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
                layout.add_widget(player)
                layout.height += player.height

            #check if post is nft
                if post['IsNFT']:

                    #bind a mdiconbutton to the postcard to open the nft modal
                    nftButton = MDFillRoundFlatIconButton(icon='nfc-variant', text='NFT', pos_hint={'center_x': 0.45, 'center_y': 0.5}, size_hint=(0.8, None))
                    nftButton.bind(on_press=lambda widget, postHashHex=post['PostHashHex'], nftImageURL=post['ImageURLs'][0],
                        numNftCopies = str(post['NumNFTCopies']), nftTitle=str(post['Body']), numNftCopiesForSale = str(post['NumNFTCopiesForSale']): 
                        self.open_nft_modal(postHashHex, nftImageURL, numNftCopies, numNftCopiesForSale, nftTitle))
                    layout.add_widget(nftButton)
                    layout.height += nftButton.height
            
            #if the post is a reclout add the reclout layout
            if post['RepostedPostEntryResponse'] != None:

                recloutLayout = RecloutLayout(orientation = 'horizontal')
                leftLayout = MDBoxLayout(orientation = 'vertical', size_hint_x = .2, size_hint_y = None)
                rightLayout = MDBoxLayout(orientation = 'vertical', size_hint_x = .8, adaptive_height = True, spacing = 25)
                
                #make the header
                #layout for the post header
                header = MDBoxLayout(orientation='horizontal', adaptive_height=True, size_hint_x = 1)
                #one line avatar list item
                repostUsername = post['RepostedPostEntryResponse']['ProfileEntryResponse']['Username']
                repostAvatar = getCachedProfilePicUrl(post['RepostedPostEntryResponse']['PosterPublicKeyBase58Check'])

                olali = OneLineAvatarListItem(text=repostUsername, divider = None, _no_ripple_effect = True)
                ilw = ImageLeftWidget(source=repostAvatar, radius = [20, ]) 
                ilw.bind(on_press=lambda widget, profileKey = post['RepostedPostEntryResponse']['PosterPublicKeyBase58Check']: self.user_profile_pressed(profileKey))         
                #add the avatar to the list item
                olali.add_widget(ilw)
                #add the three dots to the header
                #add data to dots menu 
                if post['RepostedPostEntryResponse']['PosterPublicKeyBase58Check'] in following:
                    data = self.change_3dots_data(following=True)
                else:
                    data = self.change_3dots_data(following=False)
                three_dots = MDIconButton(icon='dots-vertical')
                three_dots.bind(on_press=lambda widget, data=data, post=post: self.toast_3dots(data, post['PosterPublicKeyBase58Check']))
                
                #add the one line avatar list item to the header
                header.add_widget(olali)
                header.add_widget(three_dots)
                #add the header to the right layout
                rightLayout.add_widget(header)
                rightLayout.height += header.height
                    
                #get the reclout post body and find any links
                body=str(post['RecloutedPostEntryResponse']['Body'])
                #finds all hot links in the body
                newText = []
                textList = body.split()
                for i in textList:
                    if(i.startswith("#")) or (i.startswith("@")):
                        i = i.replace(i, ('[ref='+i+'][color=0000ff]'+i+'[/color][/ref]'))
                    newText.append(i)            	
                body = ' '.join(newText)
                #separate html links from the body text make labels for the text and cards for the links, then add them to the layout
                urls = re.findall(r'(https?://[^\s]+)', body)                
                repostPreviewHeight = 0
                previewImages = []
                for url in urls:
                    beforeUrl = body.split(url,1)[0]

                    if beforeUrl != '':
                        bodyLabel = BodyLabel(text=beforeUrl, padding = [25,25], markup=True)
                        bodyLabel.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex),
                                       on_ref_press = lambda widget, ref: self.ref_pressed(ref))
                        rightLayout.add_widget(bodyLabel)
                        rightLayout.height += bodyLabel.height * 1.5
                    body = body.split(url,1)[1] 
                    #find the image for the link
                    repostPreviewHeight += 300
                    try:
                        preview = link_preview(url)
                    except:
                        preview = None
                    if preview:
                        
                        if preview.image:
                            previewImages.append(preview.image)

                            preview_image = MDCard(size_hint_y=None, height=450, radius=[18,0])
                            aImage = AsyncImage(source=preview.image, allow_stretch=True, keep_ratio=True)
                            preview_image.add_widget(aImage)
                            preview_image.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))

                            if preview.title:
                                title = MDLabel(text=preview.title, halign =  "center", font_style = 'H6')
                                preview_image.add_widget(title)
                      
                            
                            preview_image.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
                            rightLayout.add_widget(preview_image)  
                            rightLayout.height += preview_image.height
                    else:
                        urlLabel = MDLabel(text=url, halign =  "center", theme_text_color = "Custom" , text_color = (0, 0, 1, 1) )
                        rightLayout.add_widget(urlLabel)
                        rightLayout.height += urlLabel.height
                        repostPreviewHeight += 25
                #add any remaining body to the layout
                if body != '':
                    bodyLabel = BodyLabel(text=body, markup = True)
                    bodyLabel.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex),
                                   on_ref_press = lambda widget, ref: self.ref_pressed(ref))
                    #add the body card to the layout
                    rightLayout.add_widget(bodyLabel)
                    rightLayout.height += bodyLabel.height * 1.5

                #create a card for the post Image
                postImage = ''
                repostImageHeight = 0

                if post['RecloutedPostEntryResponse']['ImageURLs']:                 
                    if post['RecloutedPostEntryResponse']['ImageURLs'][0] in previewImages:
                        repostImageHeight = 0

                    else:
                        repostImageHeight = 0
                        #swiper = MDSwiper(swipe_on_scroll = False, size_hint_y = None, height = 300, radius=(18, 18,18, 18), ) 
                        for image in post['RecloutedPostEntryResponse']['ImageURLs']:

                            card = MDCard(size_hint_y=None, height=450, radius=[18,0])
                            aImage = AsyncImage(source=image, allow_stretch=True, keep_ratio=True)
                            card.add_widget(aImage)
                            
                            card.height += aImage.height
                            card.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
                            
                            rightLayout.add_widget(card)
                            rightLayout.height += card.height

                #check if repost is nft, if so add a button to the right layout
                if post['RepostedPostEntryResponse']['IsNFT']:

                    #bind a mdiconbutton to the right layout to open the nft modal                    
                    image = ''
                    if post['RepostedPostEntryResponse']['ImageURLs']:
                        image = post['RepostedPostEntryResponse']['ImageURLs'][0]
                    nftButton = MDRectangleFlatIconButton(icon='nfc-variant', width="420", text='NFT', pos_hint={'center_x': 0.45, 'center_y': 0.5})
                    nftButton.bind(on_press=lambda widget, postHashHex=post['PostHashHex'], nftImageURL=image,
                        numNftCopies = str(post['NumNFTCopies']), nftTitle=str(post['Body']), numNftCopiesForSale = str(post['NumNFTCopiesForSale']): 
                        self.open_nft_modal(postHashHex, nftImageURL, numNftCopies, numNftCopiesForSale, nftTitle))
                    rightLayout.add_widget(nftButton)
                    rightLayout.height += nftButton.height
                
                recloutLayout.add_widget(leftLayout)
                recloutLayout.add_widget(rightLayout)
                recloutLayout.height += rightLayout.height

               
                #add the reclout layout to the timeline
                layout.add_widget(recloutLayout)
                layout.height += recloutLayout.height
            

            #declare the icons
            recloutIcon = 'repeat'
            diamondIcon = 'diamond-outline'
            likeIcon = 'heart-outline'

            #get the number of reactions
            comments=str(post['CommentCount'])
            likes=str(post['LikeCount'])
            diamonds=str(post['DiamondCount'])
            reclout=str(post['RepostCount'])
            reclouted = False
            diamonded = False
            liked = False

            if post['PostEntryReaderState']:
                recloutedByReader = post['PostEntryReaderState']['RepostedByReader']
                if recloutedByReader == True:
                    recloutIcon = 'repeat-variant'
                    reclouted = True
                
                diamondedByReader = post['PostEntryReaderState']['DiamondLevelBestowed']
                if diamondedByReader != 0:
                    diamondIcon = 'diamond'
                    diamonded = True
                
                likedByReader = post['PostEntryReaderState']['LikedByReader']
                if likedByReader == True:
                    likeIcon = 'heart'
                    liked = True

            #add the reactions to the layout
            reactions = Reactions(
                comments=comments,
                likes=likes,
                diamonds=diamonds,
                reclout=reclout,
                reclouted=reclouted,
                diamonded=diamonded,
                liked=liked,
            )
            #add the icons to the reactions, i have to pass in reactions to the functions so that i find the objects and can change the icons
            reactions.ids.like.icon = likeIcon
            reactions.ids.like.bind(on_press=lambda widget, reactions=reactions, liked=liked, postHashHex=post['PostHashHex']: self.like(postHashHex, liked, reactions))
            reactions.ids.comment.bind(on_press=lambda widget, reactions=reactions, postHashHex=post['PostHashHex']: self.comment(postHashHex, reactions))
            reactions.ids.reclout.icon = recloutIcon
            reactions.ids.reclout.bind(on_press=lambda widget, reactions=reactions, reclouted=reclouted, postHashHex=post['PostHashHex']: self.clout_or_quoteclout_dialog(postHashHex, reactions))
            reactions.ids.diamond.icon = diamondIcon
            reactions.ids.diamond.bind(on_press=lambda widget, reactions=reactions, diamonded=diamonded, postHashHex=post['PostHashHex']: self.diamond(postHashHex, liked, reactions))
            
            
            #add the reactions to the layout
            layout.add_widget(reactions)
            layout.height += reactions.height


            #add the layout to the timeline
            self.ids.timeline.add_widget(layout)
            
        pickle_profilePicUrl(getCachedProfilePicUrl.cache)
                
        
        
        
  #class that allows user to create a post add a video and image and child posts to the post and post to the blockchain
class CreatePostScreen(MDScreen):
    userName = StringProperty("")
    postHashHex = StringProperty("")
    postBody = StringProperty("")
    postImage = ListProperty([])
    postVideo = ListProperty([])
    mediaType = StringProperty("")

    def __init__(self, **kwargs):
            super().__init__(**kwargs)
            Window.bind(on_keyboard=self.events)
            self.manager_open = False
            self.file_manager = MDFileManager(
                exit_manager=self.exit_manager,
                preview= True,
                select_path=self.select_path
            )
    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
        
        self.manager_open = True

    def select_path(self, path: str):
        '''
        It will be called when you click on the file name
        or the catalog selection button.

        :param path: path to the selected directory or file;
        '''
        if self.mediaType == 'video':
            self.postVideo.append(path)
            video = VideoPlayer(source=path, state='pause', options={'allow_stretch': True})
            video.on_image_overlay_play = 'assets/preview.png'
            self.ids.previewBox.add_widget(video)
        if self.mediaType == 'image':
            self.postImage.append(path)
            img = FitImage(source=path)
            self.ids.previewBox.add_widget(img)
        self.mediaType = ''
        self.exit_manager()
        toast(path)
        

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def on_enter(self):
        settings = unpickle_settings()
        if settings['loggedIn'] != True:
            self.manager.current = 'login'
        else:
            profile = unpickle_profile()

            
            username = profile['Profile']['Username']
            circle=CircularAvatarImage(
                avatar=deso.User().getProfilePicURL(
                    profile['Profile']['PublicKeyBase58Check']))   
            Box = MDBoxLayout()
            Box.add_widget(circle)
            label = MDLabel(text=username, halign='left', theme_text_color='Primary')
            Box.add_widget(label)
            self.ids.userBox.add_widget(Box)

    #function to add a video to the post
    def select_video(self):
        self.mediaType = "video"
        self.file_manager.show(os.path.expanduser("~"))
        self.manager_open = True
    
    #function to add an image to the post
    def select_image(self):
        self.mediaType = "image"
        self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
        self.manager_open = True

    #function to create a post, get all text, images, gifs, and videos and post to the blockchain
    def post(self):
        
        toast(text=self.ids.postBox.text)
        postBody = self.ids.postBox.text
       # postImage = self.ids.postImage.source
       # postVideo = self.ids.postVideo.source
        settings=unpickle_settings()

        if settings['loggedIn'] == True:
            #upload images to images.bitclout.com
            imageURLs = []
            for imagePath in self.postImage:
                SEED_HEX = settings['seedHex']
                PUBLIC_KEY = settings['publicKey']
                desoMedia = deso.Media(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
                imageFileList = [('file', ('screenshot.jpg', open(imagePath, "rb"), 'image/png'))]
                responseURL = desoMedia.uploadImage(imageFileList)
                print(responseURL.json()['ImageURL'], 'image url')
                

                imageURLs.append(responseURL.json()['ImageURL'])
            SEED_HEX = settings['seedHex']
            PUBLIC_KEY = settings['publicKey']
            desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
            post_response = desoSocial.submitPost(body=postBody, imageURLs=imageURLs ).json()
            print(post_response)

            self.clearPostWidgets()
            self.manager.current = 'homepage_read_only'
        else:
            self.manager.current = 'login'

    def clearPostWidgets(self):
        self.ids.previewBox.clear_widgets()
        self.ids.postBox.text = ''
        self.ids.userBox.clear_widgets()
        self.postImage = []
        self.postVideo = []
        self.postBody = ''
        self.mediaType = ''

class NotificationsScreen(MDScreen):
    #toast test
    def toast(self, transactionType):
        toast(transactionType)
    #topappbar callback
    def callback(self, instance):
        if str(instance.icon)=='arrow-left':
            self.ids.notificationsList.clear_widgets()
            self.manager.current = 'homepage_read_only'
    def on_enter(self):
        settings = unpickle_settings()
        desoUser = deso.User()
        if settings['publicKey'] != True:
            publicKey = settings['publicKey']
            notifications = desoUser.getNotifications(publicKey, numToFetch=10).json()
        if not 'error' in notifications:
            for notification in notifications['Notifications']:

                transactionType = notification['Metadata']['TxnType']
                txnType = {
                    'LIKE': 'liked your post', 
                    'REPOST': 'reposted your post',
                    'FOLLOW': 'followed you',
                    'CREATOR_COIN': 'sent you some creator coin',
                    'SUBMIT_POST': 'replied to your post',
                    'HODL': 'hodled you',
                    'SEND': 'sent you some DESO',
                    'ACCEPT': 'accepted your follow request',
                    'REJECT': 'rejected your follow request',
                    'BLOCK': 'blocked you',
                    'UNBLOCK': 'unblocked you',
                    'MINT': 'minted some creator coin',
                    'BURN': 'burned some creator coin',
                    'EXCHANGE': 'exchanged some DESO',
                    'CREATE_NFT': 'created an NFT',
                    'UPDATE_NFT': 'updated an NFT',
                    'BASIC_TRANSFER': 'sent you a diamond',
                    'DAO_COIN_TRANSFER': 'sent you some DAO coin',
                    'DAO_COIN_LIMIT_ORDER': 'bought some DAO coin',
                }
                txnIcon = {
                    'LIKE': 'thumb-up',
                    'REPOST': 'repeat',
                    'FOLLOW': 'account-plus',
                    'CREATOR_COIN': 'coin',
                    'SUBMIT_POST': 'comment-text',
                    'HODL': 'hand-heart',
                    'SEND': 'send',
                    'ACCEPT': 'check',
                    'REJECT': 'close',
                    'BLOCK': 'block-helper',
                    'UNBLOCK': 'block-helper',
                    'MINT': 'plus-circle-multiple',
                    'BURN': 'minus-circle-multiple',
                    'EXCHANGE': 'swap-horizontal',
                    'CREATE_NFT': 'image',
                    'UPDATE_NFT': 'image',
                    'BASIC_TRANSFER': 'diamond',
                    'DAO_COIN_TRANSFER': 'hand-coin',
                    'DAO_COIN_LIMIT_ORDER': 'hand-coin',

                }
                transactorPublicKey = notification['Metadata']['TransactorPublicKeyBase58Check']
                desoUser = deso.User()
                transactorProfile = desoUser.getSingleProfile(publicKey=transactorPublicKey).json()


                transactorUsername = transactorProfile['Profile']['Username']
                transactorPic = getCachedProfilePicUrl(transactorPublicKey)
                if not transactorPic:
                    transactorPic = 'https://bitclout.com/assets/img/default_profile_pic.png'

                notificationCard = OneLineAvatarIconListItem(
                    ImageLeftWidget(
                        source=transactorPic
                    ),
                    IconRightWidget(
                        icon=txnIcon[transactionType]
                    ),
                    text= transactorUsername + ' ' + txnType[transactionType],
                    on_press = lambda x, transactionType=transactionType, notification=notification: self.transactionCallback(transactionType, notification)
                    
                )
                self.ids.notificationsList.add_widget(notificationCard)
    
    def transactionCallback(self, transactionType, notification):


        if transactionType == 'LIKE':
            postHashHex = notification['Metadata']['LikeTxindexMetadata']['PostHashHex']
            pickle_post(postHashHex)
            self.manager.current = 'single_post'
        elif transactionType == 'SUBMIT_POST':
            postHashHex = notification['Metadata']['SubmitPostTxindexMetadata']['PostHashBeingModifiedHex']
            pickle_post(postHashHex)
            self.manager.current = 'single_post'    
        elif transactionType == 'BASIC_TRANSFER':
            postHashHex = notification['Metadata']['BasicTransferTxindexMetadata']['PostHashHex']
            pickle_post(postHashHex)
            self.manager.current = 'single_post'



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
        sm.add_widget(NotificationsScreen(name='notifications'))
        sm.add_widget(SinglePostScreen(name='single_post'))
        sm.add_widget(ProfileScreen(name='profile')),
        sm.add_widget(SeedLoginScreen(name='seed_login'))
        sm.add_widget(SearchScreen(name='search'))
        sm.add_widget(CreatePostScreen(name='create_post'))

        
        #check to see if logged in and go to homepage
        settings=unpickle_settings()

        if settings:
            global loggedIn
            loggedIn = True
            sm.current = 'homepage_read_only'

        return sm
    



# Run the app
if __name__ == '__main__':
    MainApp().run()
