from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.theming import ThemeManager
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRoundFlatButton
import deso
from deso import Identity
from kivy.properties import StringProperty
import pickle
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem


global currentPost 
global loggedIn
global user
global publicKey    
loggedIn = False
user = ""
publicKey = ""

#pickles the current settings
def pickle_settings(settings):
    with open('temp/settings.pickle', 'wb') as handle:
        pickle.dump(settings, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("settings pickled")

#unpickles the current settings
def unpickle_settings():
    with open('temp/settings.pickle', 'rb') as handle:
        settings = pickle.load(handle)
        print("settings unpickled")
    return settings

#unpickles the current post
def unpickle_post():
    with open('temp/post.pickle', 'rb') as handle:
        post = pickle.load(handle)
        print("post unpickled")
    return post
#pickles the current post
def pickle_post(post):
    with open('temp/post.pickle', 'wb') as handle:
        pickle.dump(post, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("post pickled")

# unpickles the user's profile
def unpickle_profile():
    with open('temp/profile.pickle', 'rb') as handle:
        profile = pickle.load(handle)
        #print("profile unpickled")
    return profile

# pickles the user's profile
def pickle_profile(profile):
    with open('temp/profile.pickle', 'wb') as handle:
        pickle.dump(profile, handle, protocol=pickle.HIGHEST_PROTOCOL)
        #print("profile pickled")

#class for custom dialog content
class Content(MDBoxLayout):
    quote = StringProperty()

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
    reclout = StringProperty()
    postHashHex = StringProperty()
    posted_ago = StringProperty()
    

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
        #print(self.seedPhrase, 'seed phrase')
        SEED_HEX = Identity.getSeedHexFromSeedPhrase(seedphrase)
        #print(SEED_HEX, 'seed hex')
        #print(self.userName, 'username')
        #get user profile and pickle it
        desoUser = deso.User()
        profile = desoUser.getSingleProfile(username=self.userName).json()
        #print(profile)
        if 'error' in profile:
            toast(profile['error'])
        else:
            pickle_profile(profile)
            global user
            global loggedIn
            global publicKey
            loggedIn = True
            user=self.userName
            publicKey=profile['Profile']['PublicKeyBase58Check']
            settings = {}
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
        postImage = ''
        if post['PostFound']['ImageURLs']:
            postImage = post['PostFound']['ImageURLs'][0]
            
        #print(post)
        self.ids.username.text = post['PostFound']['ProfileEntryResponse']['Username']
        
        self.ids.singlePost.add_widget(PostCard(     
        avatar=deso.User().getProfilePicURL(
                    post['PostFound']['PosterPublicKeyBase58Check']),
        username = post['PostFound']['ProfileEntryResponse']['Username'],
        body=str(post['PostFound']['Body']),
        post = postImage,
        likes = str(post['PostFound']['LikeCount']),
        comments = str(post['PostFound']['CommentCount']),
        #posted_ago = post['PostFound']['PostEntryReaderState']['TimeAgo'],
        diamonds = str(post['PostFound']['DiamondCount']),
        reclout = str(post['PostFound']['RecloutCount']),
        postHashHex = post['PostFound']['PostHashHex']
        ))
        self.ids.appbar.add_widget(CircularAvatarImage(
                avatar=deso.User().getProfilePicURL(
                    post['PostFound']['PosterPublicKeyBase58Check']),
                name=post['PostFound']['ProfileEntryResponse']['Username'],
    
        ))          

# Create the homepage read only screen
class HomePageReadOnlyScreen(MDScreen):
    profile_picture = StringProperty("") #'https://avatars.githubusercontent.com/u/89080192?v=4'
    username = StringProperty("")
    desoprice = StringProperty("")
    avatar = StringProperty("")
    dialog = None
    
    def on_enter(self):
        profile = unpickle_profile()
        print(profile)
        print(profile['Profile']['Username'])
        username=profile['Profile']['Username']
        self.username = profile['Profile']['Username']
        self.profile_picture = deso.User().getProfilePicURL(
                    profile['Profile']['PublicKeyBase58Check'])
        self.list_stories()
        self.list_posts()
        print(user, 'printed user here')

    def logout(self):
        settings = {}
        settings['loggedIn'] = False
        pickle_settings(settings)
        global loggedIn
        loggedIn = False
        self.manager.current = 'login'

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
        
    #like a post function allows user to like a post, toggles icon to red, updates the like count, and sends a like to the blockchain    
    def like(self, postHashHex):
        global loggedIn
        if loggedIn != True:
            toast('You must be logged in to like a post')
        else:
            settings=unpickle_settings()
            if settings['loggedIn'] == True:
                print(postHashHex, "posthashhex in like function")
                for self.post in self.ids.timeline.children:
                    #print(self.post.postHashHex)
                    if self.post.postHashHex == postHashHex:
                        if self.post.ids.like.icon == 'heart':
                            self.post.ids.like.icon = 'heart-outline'
                            self.post.likes = str(int(self.post.likes) - 1)
                            SEED_HEX = settings['seedHex']
                            PUBLIC_KEY = settings['publicKey']
                            desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
                            print(desoSocial.like(postHashHex, isLike=False).json())
                        else:
                            self.post.ids.like.icon = 'heart'
                            self.post.likes = str(int(self.post.likes) + 1)
                            SEED_HEX = settings['seedHex']
                            PUBLIC_KEY = settings['publicKey']
                            desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
                            print(desoSocial.like(postHashHex, isLike=True).json())

                        break 
     #diamond a post function allows user to like a post, toggles icon to red, updates the like count, and sends a diamond to the blockchain
    def diamond(self, postHashHex):
        global loggedIn
        if loggedIn != True:
            toast('You must be logged in to diamond a post')
        else:
            settings=unpickle_settings()
            if settings['loggedIn'] == True:
                print(postHashHex, "posthashhex in diamond function")
                for self.post in self.ids.timeline.children:
                    print(self.post.postHashHex)
                    if self.post.postHashHex == postHashHex:   
                        post = deso.Posts()
                        post = post.getSinglePost(postHashHex=postHashHex).json()      
                        if post['PostFound']['PosterPublicKeyBase58Check']:              
                            self.post.ids.diamond.icon = 'diamond'
                            self.post.diamonds = str(int(self.post.diamonds) + 1)
                            SEED_HEX = settings['seedHex']
                            PUBLIC_KEY = settings['publicKey']
                            receiverPublicKey = post['PostFound']['PosterPublicKeyBase58Check']
                            desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
                            print(desoSocial.diamond(postHashHex, receiverPublicKey,  diamondLevel=1).json())
                            toast('You have successfully diamonded this post')
                        else: 
                            toast('You cannot diamond your own post')
                        

                        break

    #use a MDDIalog to ask user if they want to repost or quote post
    def clout_or_quoteclout_dialog(self, postHashHex):
        if not self.dialog:
            self.dialog = MDDialog(
            title="Would you like to reclout or quoteclout this post?",
            type="simple",
            items=[
                Item(text="ReClout", source="assets/reclout.png", on_release= lambda widget, postHashHex=postHashHex: self.recloutpressed(postHashHex)),
                Item(text="QuoteClout", source="assets/quoteclout.png", on_release= lambda widget, postHashHex=postHashHex: self.quotecloutpressed(postHashHex)),
            ],
            )
            self.dialog.open()

    # if user selects quoteclout, open a dialog box to enter a quote, else return error to reclout function
    def quotecloutpressed(self, postHashHex):
        self.dialog.dismiss()
        self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
            title="Enter a quote",
            type="custom",
            content_cls=Content(),
            buttons=[
                MDRoundFlatButton(text="CANCEL", on_release=lambda widget: self.dialog.dismiss()),
                MDRoundFlatButton(text="QUOTE", on_release= lambda widget, postHashHex=postHashHex: self.quoteclout(postHashHex)),
            ],
            )
            self.dialog.open()

    #if user selects quoteclout, send a quoteclout to the blockchain and close the dialog box, else return error to reclout function
    def quoteclout(self, postHashHexToQuote):
        
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

    #if user selects reclout, send a reclout to the blockchain and close the dialog box, else return error to reclout function
    def recloutpressed(self, postHashHexToRepost):
        #print(postHashHexToRepost, 'posthashhex in recloutpressed')
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


    #reclout a post function allows user to reclout a post, toggles icon reposted, updates the reclout count, and sends a reclout to the blockchain        
    def reclout(self, postHashHex):
        global loggedIn
        if loggedIn != True:
            toast('You must be logged in to reclout a post')
        else:
            settings=unpickle_settings()
            if settings['loggedIn'] == True:
                #print(postHashHex, "posthashhex in reclout function")
                if self.clout_or_quoteclout_dialog(postHashHex) == False:
                    toast('An error occured reclouting this post')
                else:
                    #update the icon and reclout count
                    for self.post in self.ids.timeline.children:
                    #    print(self.post.postHashHex)
                        if self.post.postHashHex == postHashHex:
                            self.post.ids.reclout.icon = 'repeat-variant'
                            self.post.reclout = str(int(self.post.reclout) + 1)
                        
                            break

    def toast_3dots(self):
        toast('3 dots pressed')
            

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

            userposts = posts.getPostsStateless(readerPublicKey = profile['Profile']['PublicKeyBase58Check'],numToFetch=10, getPostsForFollowFeed=True)
        else:
            userposts = deso.Posts().getPostsStateless(numToFetch=10)
        
        
        for post in userposts.json()['PostsFound']:
            circle=CircularAvatarImage(
                avatar=deso.User().getProfilePicURL(
                    post['PosterPublicKeyBase58Check']),
                name=post['ProfileEntryResponse']['Username'],
                )
            circle.bind(on_press=lambda widget, userid=post['ProfileEntryResponse']['PublicKeyBase58Check']: self.storie_switcher(userid))
            self.ids.stories.add_widget(circle)

    def list_posts(self):
        profile = unpickle_profile()
        if profile:
            print(profile['Profile']['PublicKeyBase58Check'])
            posts = deso.Posts()
            posts.readerPublicKey = profile['Profile']['PublicKeyBase58Check']
            userposts = posts.getPostsStateless(readerPublicKey = profile['Profile']['PublicKeyBase58Check'],numToFetch=10, getPostsForFollowFeed=True)
        else:
            userposts = deso.Posts().getPostsStateless(numToFetch=10)

        
        for post in userposts.json()['PostsFound']:
            #print(post)
            #If this is a repost of another post, get the original post and extra body text

            if post['RepostedPostEntryResponse'] != None:
                print('repost found', post)
                repostBody = post['RepostedPostEntryResponse']['Body']
                repostImage=""
                if post['RepostedPostEntryResponse']['ImageURLs'] != None:
                    repostImage = post['RepostedPostEntryResponse']['ImageURLs'][0]
                reposterUsername=username=post["ProfileEntryResponse"]['Username']
                reposterAvatar=deso.User().getProfilePicURL(post['ProfileEntryResponse']['PublicKeyBase58Check'])
                postcard=(PostCard(
                username = post['RepostedPostEntryResponse']['ProfileEntryResponse']['Username'],
                avatar=deso.User().getProfilePicURL(post['RepostedPostEntryResponse']['PosterPublicKeyBase58Check']),
                postHashHex=str(post['PostHashHex']),
                #repostPostHashHex=post['RepostedPostEntryResponse']['PostHashHex'],
                likes=str(post['LikeCount']),
                comments=str(post['CommentCount']),
                body=str(post['RepostedPostEntryResponse']['Body']),
                readmore=readmore,
                post=repostImage,
                diamonds=str(post['DiamondCount']),
                reclout=str(post['RepostCount'])
                ))
                repostcard=(PostCard(
                username = reposterUsername,
                avatar=reposterAvatar,
                postHashHex=str(post['PostHashHex']),
                body=repostBody,
                ))
                box=MDBoxLayout(orientation='vertical')
                box.add_widget(repostcard)
                box.add_widget(postcard)
                self.ids.timeline.add_widget(box)
                print('repost body', repostBody)
            #else this is a regular post add all info and card to the timeline
            else:
                
                readmore = ''
                if len(post['Body']) > 144:
                    readmore = '  -- read more --'
                postImage = ''
                if post['ImageURLs']:
                    postImage = post['ImageURLs'][0]
                recloutedByReader = post['PostEntryReaderState']['RepostedByReader']
                if recloutedByReader == True:
                    recloutIcon = 'repeat-variant'
                else:
                    recloutIcon = 'repeat'
                diamondedByReader = post['PostEntryReaderState']['DiamondLevelBestowed']
                if diamondedByReader == 0:
                    diamondIcon = 'diamond-outline'
                else:
                    diamondIcon = 'diamond'
                likedByReader = post['PostEntryReaderState']['LikedByReader']
                if likedByReader == True:
                    likeIcon = 'heart'
                else:
                    likeIcon = 'heart-outline'
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
                    reclout=str(post['RepostCount']),
                    #posted_ago = str(post['TimeStampNanos']), doesn;t work
                ))
                #bind the posthashhex to the postcard for each post in the timeline
                postcard.ids.dots.bind(on_press=lambda widget: self.toast_3dots())
                postcard.ids.like.icon = likeIcon
                postcard.ids.like.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.like(postHashHex))
                postcard.ids.reclout.icon = recloutIcon
                postcard.ids.reclout.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.reclout(postHashHex))
                postcard.ids.diamond.icon = diamondIcon
                postcard.ids.diamond.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.diamond(postHashHex))
                postcard.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
                self.ids.timeline.add_widget(postcard)

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
        sm.add_widget(SeedLoginScreen(name='seed_login'))
        sm.add_widget(PostScreen(name='post'))
        
        #check to see if logged in and go to homepage
        settings=unpickle_settings()
        print('settings are here', settings)
        if settings['loggedIn']:
            global loggedIn
            loggedIn = True
            sm.current = 'homepage_read_only'

        return sm

    



# Run the app
if __name__ == '__main__':
    MainApp().run()
