from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.videoplayer import VideoPlayer
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.fitimage import FitImage
from kivymd.uix.widget import MDWidget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.theming import ThemeManager
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import (
    MDCardSwipe, MDCardSwipeLayerBox, MDCardSwipeFrontBox, MDCard
)
from kivymd.uix.list import MDList, OneLineListItem, OneLineAvatarIconListItem, ImageLeftWidget, IconRightWidget
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
from Post import SinglePostScreen

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
    if os.path.exists('temp/settings.pickle'):
        with open('temp/settings.pickle', 'rb') as handle:
            settings = pickle.load(handle)
            print("settings unpickled")
    else:
        settings = {}  
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
    if not os.path.exists('temp/settings.pickle'):
        os.makedirs('temp')
    with open('temp/profile.pickle', 'wb') as handle:
        pickle.dump(profile, handle, protocol=pickle.HIGHEST_PROTOCOL)
        #print("profile pickled")

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
        #print(profile)
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
    profile_picture = StringProperty("") #'https://avatars.githubusercontent.com/u/89080192?v=4'
    username = StringProperty("")
    desoprice = StringProperty("")
    avatar = StringProperty("")
    dialog = None
    follow_unfollow = StringProperty("")
    
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
        
        pickle_settings(settings)
        global loggedIn
        loggedIn = False
        self.manager.current = 'login'

    #changes to the single read post screen
    def open_post(self, postHashHex):
        pickle_post(postHashHex)
        print('posthashhex was pickled', postHashHex)
        self.manager.current = 'single_post'

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
            print(settings)
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
    #comment a post function allows user to comment a post, updates the comment count, and sends a comment to the blockchain
    def comment(self, postHashHex):
        global loggedIn
        if loggedIn != True:
            toast('You must be logged in to comment a post')
        else:
            settings=unpickle_settings()
            if settings['loggedIn'] == True:
                print(postHashHex, "posthashhex in comment function")
                
                self.dialog = None
                if not self.dialog:
                    self.dialog = MDDialog(
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
                                text="COMMENT", on_release= lambda widget, postHashHex=postHashHex: self.postComment(postHashHex)
                            )],
                        
    
                    )
                    self.dialog.open()

    def postComment(self, postHashHex):
        for self.post in self.ids.timeline.children:
            #print(self.post.postHashHex)
            if self.post.postHashHex == postHashHex:
                settings=unpickle_settings()
                SEED_HEX = settings['seedHex']
                PUBLIC_KEY = settings['publicKey']
                desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
                #print(self.dialog.content_cls.ids.comment.text)
                comment_response = desoSocial.submitPost(parentStakeID=postHashHex, body=self.dialog.content_cls.ids.comment.text, ).json()
                self.dialog.dismiss()
                self.dialog = None
                print(comment_response)
                if 'error' in comment_response:
                    return False
                self.post.comments = str(int(self.post.comments) + 1)

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
    def unfollow(self, posterPublicKey):
        settings=unpickle_settings()
        SEED_HEX = settings['seedHex']
        PUBLIC_KEY = settings['publicKey']
        desoSocial = deso.Social(nodeURL="https://diamondapp.com/api/v0/", publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
        print(desoSocial.follow(posterPublicKey, isFollow=False).json())
        print('unfollow', posterPublicKey)
    
    def follow(self, posterPublicKey):
        pass
    def callback_for_menu_items(self, *args):
        toast(args[0])
        if args[0] == "Follow":
            self.follow(args[1])
        elif args[0] == "Unfollow":
            self.unfollow(args[1])

    #function to change 3dots data(self, following)
    def change_3dots_data(self, following):
        if following == True:
            data = {
            "Unfollow": "account-minus",
            "Share": "share-variant",
            "Report": "alert-circle",
            "Cancel": "cancel",
            }
        else:
            data = {
            "Follow": "account-plus",
            "Share": "share-variant",
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
        # print(dollars)
        self.desoprice = str(dollars)
        # load 10 posts for the user or 10 posts for the stateless user
        posts = deso.Posts()
        if profile:
            print(profile['Profile']['PublicKeyBase58Check'])
            posts.readerPublicKey = profile['Profile']['PublicKeyBase58Check']
            userposts = posts.getPostsStateless(numToFetch=10, getPostsForFollowFeed=True)
        else:
            posts.reaerPublicKey = None
            userposts = deso.Posts().getPostsStateless(numToFetch=10)
        
        
        for post in userposts.json()['PostsFound']:
            circle=CircularAvatarImage(
                avatar=deso.User().getProfilePicURL(
                    post['PosterPublicKeyBase58Check']),
                #name=post['ProfileEntryResponse']['Username'],
                )
            circle.bind(on_press=lambda widget, userid=post['ProfileEntryResponse']['PublicKeyBase58Check']: self.storie_switcher(userid))
            self.ids.stories.add_widget(circle)

    #monitors the scrollview and calls refresh when it reaches the bottom
    def touch_up_value(self, *args):
        #print(self.ids.mainScrollView.scroll_y)
        if self.ids.mainScrollView.scroll_y  <= 0:
            self.refresh_posts()
            toast("refreshing")

    def refresh_posts(self):
        pass
        
    def get_posts(self):
        profile = unpickle_profile()
        settings = unpickle_settings()
        following = []
        #if theres a user public Key get the users following list
        if 'publicKey' in settings:
            desoUser = deso.User()
            followingResponse = desoUser.getFollowsStateless(publicKey = settings['publicKey']).json()
            for publicKey in followingResponse['PublicKeyToProfileEntry']:
                        following.append(publicKey)         
        
        posts = deso.Posts()
        #if trending feed true or if theres no profile get trending posts
        if 'trending' in settings:
            if settings['trending'] == True:
                self.ids.trending.md_bg_color = "blue"
                posts.readerPublicKey = None
                userposts = posts.getHotFeed(numToFetch=10)
                
            else:
                self.ids.following.md_bg_color = "blue"        
                if profile:
                    posts.readerPublicKey = profile['Profile']['PublicKeyBase58Check']
                    userposts = posts.getPostsStateless(numToFetch=10, getPostsForFollowFeed=True)
        
        #if theres no profile get trending posts                         
        else:
            posts.readerPublicKey = None
            userposts = posts.getHotFeed(numToFetch=10)

        return userposts,following

    def list_posts(self):
               
        userposts, following = self.get_posts()
            
        for post in userposts.json()['PostsFound']:
            #print(post)
            #If this is a repost of another post, get the original post and extra body text
            nftImage = ''
            if post['IsNFT']:
                pass#print('caught nft', post)
            if post['RepostedPostEntryResponse'] != None:
                #print('repost found', post)
                postVideo = ''
                if post['VideoURLs']:
                    print('video found *****************8', post['VideoURLs'])
                    #print(post)
                    postVideo = post['VideoURLs'][0]
                repostBody = post['RecloutedPostEntryResponse']['Body']
                repostImage = ''
                print(post['RecloutedPostEntryResponse']['ImageURLs'],'*****************************')
                if post['RecloutedPostEntryResponse']['ImageURLs']:
                    repostImage = post['RecloutedPostEntryResponse']['ImageURLs'][0]
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
                #print('postHashHex', str(post['PostHashHex'])),
                repostcard=(RePostCard(
                username=post["ProfileEntryResponse"]['Username'],
                avatar=deso.User().getProfilePicURL(post['ProfileEntryResponse']['PublicKeyBase58Check']),                
                likes=str(post['LikeCount']),
                comments=str(post['CommentCount']),
                diamonds=str(post['DiamondCount']),
                repostVideo=postVideo,
                reclout=str(post['RepostCount']),
                postHashHex=str(post['PostHashHex']),           
                repostUsername = post['RepostedPostEntryResponse']['ProfileEntryResponse']['Username'],
                repostAvatar=deso.User().getProfilePicURL(post['RepostedPostEntryResponse']['PosterPublicKeyBase58Check']),
                #repostPostHashHex=str(post['PostHashHex']),
                repostPostHashHex=str(post['RepostedPostEntryResponse']['PostHashHex']),
                #repostBody=str(post['RepostedPostEntryResponse']['Body']),
                repostPost=repostImage,                
                ))
                print('added repostImage', repostImage)
                #check if has nft, if so add a button to the postcard
                if post['RepostedPostEntryResponse']['IsNFT']:
                    print('adding nft button', post['RepostedPostEntryResponse'])
                    #bind a mdiconbutton to the postcard to open the nft modal                    
                    nftButton = MDRectangleFlatIconButton(icon='nfc-variant', width="420", text='NFT', pos_hint={'center_x': 0.45, 'center_y': 0.5})
                    nftButton.bind(on_press=lambda widget, postHashHex=post['PostHashHex'], nftImageURL=repostImage,
                        numNftCopies = str(post['NumNFTCopies']), nftTitle=str(post['Body']), numNftCopiesForSale = str(post['NumNFTCopiesForSale']): 
                        self.open_nft_modal(postHashHex, nftImageURL, numNftCopies, numNftCopiesForSale, nftTitle))
                    repostcard.ids.nftButtonBox.add_widget(nftButton)
                #bind the posthashhex to the repostcard for each post in the time, nftTitle=str(post['Body'])line
                if post['PosterPublicKeyBase58Check'] in following:
                    data = self.change_3dots_data(following=True)
                else: 
                    data = self.change_3dots_data(following=False)
                repostcard.ids.dots.bind(on_press=lambda widget: self.toast_3dots(data, post['PosterPublicKeyBase58Check']))
                repostcard.ids.like.icon = likeIcon
                repostcard.ids.like.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.like(postHashHex))
                repostcard.ids.comment.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.comment(postHashHex))
                repostcard.ids.reclout.icon = recloutIcon
                repostcard.ids.reclout.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.reclout(postHashHex))
                repostcard.ids.diamond.icon = diamondIcon
                repostcard.ids.diamond.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.diamond(postHashHex))
                repostcard.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
                if post['Body']:
                    bodyCard = MDCard()
                    bodyCard.add_widget(MDLabel(text=str(post['Body'])[:288]))
                    bodyCard.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
                    repostcard.ids.bodyBox.add_widget(bodyCard)
                if post['RecloutedPostEntryResponse']['Body']:
                    bodyCard = MDCard()
                    bodyCard.add_widget(MDLabel(text=str(post['RecloutedPostEntryResponse']['Body'])[:288]))
                    bodyCard.bind(on_press= lambda widget, postHashHex=post['RecloutedPostEntryResponse']['PostHashHex']: self.open_post(postHashHex))
                    repostcard.ids.repostBodyBox.add_widget(bodyCard)
                if repostImage:
                    imageCard = MDCard(FitImage(source=repostImage, size_hint_y=1, radius=(18, 18,18, 18),), radius=18, md_bg_color="grey",
                     pos_hint={"center_x": .5, "center_y": .5}, size_hint=(0.8, 1.7))
                    imageCard.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex)),
                    repostcard.ids.mediaBox.add_widget(imageCard)
                if postVideo:
                    player = VideoPlayer(source=postVideo, state='pause', options={'allow_stretch': True})
                    repostcard.ids.mediaBox.add_widget(player)
                self.ids.timeline.add_widget(repostcard)

                #print('repost body', repostBody)

            #else this is a regular post add all info and card to the timeline
            else:
                
                
                postVideo = ''
                if post['VideoURLs']:
                    print('video found *****************8', post['VideoURLs'][0])
                    #print(post)
                    postVideo = post['VideoURLs'][0]
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
                    #body=str(post['Body']),
                    readmore=readmore,
                    #post=postImage, 
                    video=postVideo,
                    diamonds=str(post['DiamondCount']),
                    reclout=str(post['RepostCount']),
                    #posted_ago = str(post['TimeStampNanos']), doesn;t work
                ))
                print('added postImage', postImage)
                #bind the posthashhex to the postcard for each post in the timeline
                #check if has nft, if so add a button to the postcard
                if post['IsNFT']:
                    print('adding nft button')
                    #bind a mdiconbutton to the postcard to open the nft modal
                    nftButton = MDFillRoundFlatIconButton(icon='nfc-variant', text='NFT', pos_hint={'center_x': 0.45, 'center_y': 0.5}, size_hint=(0.8, 0.4))
                    nftButton.bind(on_press=lambda widget, postHashHex=post['PostHashHex'], nftImageURL=postImage,
                        numNftCopies = str(post['NumNFTCopies']), nftTitle=str(post['Body']), numNftCopiesForSale = str(post['NumNFTCopiesForSale']): 
                        self.open_nft_modal(postHashHex, nftImageURL, numNftCopies, numNftCopiesForSale, nftTitle))
                    postcard.ids.nftButtonBox.add_widget(nftButton)
                #add data to dots menu 
                if post['PosterPublicKeyBase58Check'] in following:
                    data = self.change_3dots_data(following=True)
                else:
                    data = self.change_3dots_data(following=False)
                postcard.ids.dots.bind(on_press=lambda widget: self.toast_3dots(data, post['PosterPublicKeyBase58Check']))
                postcard.ids.like.icon = likeIcon
                postcard.ids.like.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.like(postHashHex))
                postcard.ids.comment.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.comment(postHashHex))
                postcard.ids.reclout.icon = recloutIcon
                postcard.ids.reclout.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.reclout(postHashHex))
                postcard.ids.diamond.icon = diamondIcon
                postcard.ids.diamond.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.diamond(postHashHex))
                #postcard.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
                if post['Body']:
                    bodyCard = MDCard()
                    bodyCard.add_widget(MDLabel(text=post['Body'][:288]))
                    bodyCard.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
                    postcard.ids.bodyBox.add_widget(bodyCard)
                if postImage:
                    imageCard = MDCard(FitImage(source=postImage, size_hint_y=1, radius=(18, 18,18, 18),), radius=18, md_bg_color="grey",
                     pos_hint={"center_x": .5, "center_y": .5}, size_hint=(0.8, 1.7))
                    imageCard.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex)),
                    postcard.ids.mediaBox.add_widget(imageCard)
                if postVideo:
                    player = VideoPlayer(source=postVideo, state='pause', options={'allow_stretch': True})
                    postcard.ids.mediaBox.add_widget(player)
                self.ids.timeline.add_widget(postcard)
        
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
            print(profile)
            
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
        print(settings, 'settings&&&&&&&&&&&&&&&&&&&')
        if settings['loggedIn'] == True:
            #upload images to images.bitclout.com
            imageURLs = []
            for imagePath in self.postImage:
                SEED_HEX = settings['seedHex']
                PUBLIC_KEY = settings['publicKey']
                desoMedia = deso.Media(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
                imageFileList = [('file', ('screenshot.jpg', open(imagePath, "rb"), 'image/png'))]
                responseURL = desoMedia.uploadImage(imageFileList)
                print(responseURL.json(), '*******************responseURL')
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
                print(notification)
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
                print('transactorProfile', transactorProfile)
                print('large profile pic', transactorProfile['Profile']['ExtraData']['LargeProfilePicURL'])
                transactorUsername = transactorProfile['Profile']['Username']
                transactorPic = transactorProfile['Profile']['ExtraData']['LargeProfilePicURL']
                if not transactorPic:
                    transactorPic = 'https://bitclout.com/assets/img/default_profile_pic.png'
                print(transactorUsername)
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
        print(transactionType)
        print(notification)
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
        sm.add_widget(SeedLoginScreen(name='seed_login'))
        sm.add_widget(CreatePostScreen(name='create_post'))

        
        #check to see if logged in and go to homepage
        settings=unpickle_settings()
        print('settings are here', settings)
        if settings:
            global loggedIn
            loggedIn = True
            sm.current = 'homepage_read_only'

        return sm
    



# Run the app
if __name__ == '__main__':
    MainApp().run()
