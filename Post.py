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

global loggedIn
global user
global publicKey    
loggedIn = False

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


# class for the post card
class SinglePostCard(MDBoxLayout):
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
class SingleRePostCard(MDBoxLayout):
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


    


#class for reading a single post
class SinglePostScreen(MDScreen):
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
        settings = unpickle_settings()
        global loggedIn
        loggedIn = settings['loggedIn']
        username=profile['Profile']['Username']
        self.username = profile['Profile']['Username']
        self.profile_picture = deso.User().getProfilePicURL(
                    profile['Profile']['PublicKeyBase58Check'])
        self.list_post()

    #clear widgets on leave
    def on_leave(self):
        self.ids.singlePost.clear_widgets()
        
    def logout(self):
        settings = {}        
        pickle_settings(settings)
        global loggedIn
        loggedIn = False
        self.manager.current = 'login'

    
            
    #like a post function allows user to like a post, toggles icon to red, updates the like count, and sends a like to the blockchain    
    def like(self, postHashHex):
        global loggedIn
        if loggedIn != True:
            toast('You must be logged in to like a post')
        else:
            settings=unpickle_settings()
            #print(settings)
            if settings['loggedIn'] == True:
                #print(postHashHex, "posthashhex in like function")
                for self.post in self.ids.singlePost.children:
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
                        title="Comment",
                        type="custom",
                        content_cls=CommentContent(),
                        buttons=[
                            MDRoundFlatButton(
                                text="CANCEL", on_release=lambda widget: self.dialog.dismiss()
                            ),
                            MDRoundFlatButton(
                                text="COMMENT", on_release= lambda widget, postHashHex=postHashHex: self.postComment(postHashHex)
                            ),
                        ],
                    )
                    self.dialog.open()

    def postComment(self, postHashHex):
        global loggedIn
        if loggedIn != True:
            toast('You must be logged in to diamond a post')
        else:
        
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
            for self.post in self.ids.singlePost.children:
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
                for self.post in self.ids.singlePost.children:
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
        global loggedIn
        if loggedIn != True:
            toast('You must be logged in to diamond a post')
        else:
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
                    for self.post in self.ids.singlePost.children:            
                        self.post.ids.reclout.icon = 'repeat-variant'
                        self.post.reclout = str(int(self.post.reclout) + 1)                        

    def unfollow(self, posterPublicKey):
        global loggedIn
        if loggedIn != True:
            toast('You must be logged in to diamond a post')
        else:
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
            content_cls=NFTContent(nftImage = str(nftImageURL), numNftCopiesForSale = numNftCopiesForSale, numNftCopies = numNftCopies),
            
            buttons=[
                MDRoundFlatButton(text="CANCEL", on_release=lambda widget: self.nftmodal.dismiss()),
                MDRoundFlatButton(text="BUY", on_release= lambda widget, postHashHex=postHashHex: self.buy_nft(postHashHex)),
            ],
        )
        self.nftmodal.open()
    def buy_nft(self, postHashHex):
        pass

    def list_post(self):
        PostHashHex = unpickle_post()
        profile = unpickle_profile()

        desopost = deso.Posts()
        post = desopost.getSinglePost(postHashHex=PostHashHex).json()
        if 'error' in post:
            toast('An error occured getting this post')
        else: 
            if profile:
                print(profile['Profile']['PublicKeyBase58Check'])
                
                desoUser = deso.User()
                followingResponse = desoUser.getFollowsStateless(username = profile['Profile']['Username']).json()
                following = []
                for publicKey in followingResponse['PublicKeyToProfileEntry']:
                    following.append(publicKey)
                
            
        
                
            print(post)
            post = post['PostFound']
            #If this is a repost of another post, get the original post and extra body text
            nftImage = ''
            print(post)
            if post['IsNFT']:
                pass#print('caught nft', post)
            if post['RepostedPostEntryResponse'] != None:
                #print('repost found', post)
                postVideo = ''
                if post['VideoURLs']:
                    print('video found *****************8', post['VideoURLs'])
                    #print(post)
                    postVideo = post['VideoURLs'][0]
                repostBody = post['RepostedPostEntryResponse']['Body']
                repostImage=[]
                if post['RepostedPostEntryResponse']['ImageURLs'] != None:
                    repostImage = post['RepostedPostEntryResponse']['ImageURLs']
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
                print('postHashHex', str(post['PostHashHex'])),
                repostcard=(SingleRePostCard(
                username=post["ProfileEntryResponse"]['Username'],
                avatar=deso.User().getProfilePicURL(post['ProfileEntryResponse']['PublicKeyBase58Check']),
                
                body=str(post['Body']),
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
                repostBody=str(post['RepostedPostEntryResponse']['Body']),
                          
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
                repostcard.ids.dots.bind(on_press=lambda widget: self.toast_3dots(data, post['PosterPublicKeyBase58Check']))
                repostcard.ids.like.icon = likeIcon
                repostcard.ids.like.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.like(postHashHex))
                repostcard.ids.comment.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.comment(postHashHex))
                repostcard.ids.reclout.icon = recloutIcon
                repostcard.ids.reclout.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.reclout(postHashHex))
                repostcard.ids.diamond.icon = diamondIcon
                repostcard.ids.diamond.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.diamond(postHashHex))
                repostcard.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
                repostcard.ids.bodyCard.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
                if repostImage:
                    for image in repostImage:
                        imageCard = MDCard(FitImage(source=image, size_hint_y=1, radius=(18, 18,18, 18),), radius=18, md_bg_color="grey",
                        pos_hint={"center_x": .5, "center_y": .5}, size_hint=(0.8, 3.4))
                        repostcard.ids.mediaBox.add_widget(imageCard)
                if postVideo:
                    player = VideoPlayer(source=postVideo, state='pause', options={'allow_stretch': True})
                    repostcard.ids.mediaBox.add_widget(player)
                self.ids.singlePost.add_widget(repostcard)
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
                postImage = []
                if post['ImageURLs']:
                    postImage = post['ImageURLs']
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
                postcard=(SinglePostCard(
                    username=post["ProfileEntryResponse"]['Username'],
                    avatar=deso.User().getProfilePicURL(
                        post['ProfileEntryResponse']['PublicKeyBase58Check']),
                    postHashHex=str(post['PostHashHex']),
                    likes=str(post['LikeCount']),
                    comments=str(post['CommentCount']),
                    body=str(post['Body']),
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
                postcard.ids.dots.bind(on_press=lambda widget: self.toast_3dots(data, post['PosterPublicKeyBase58Check']))
                postcard.ids.like.icon = likeIcon
                postcard.ids.like.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.like(postHashHex))
                postcard.ids.comment.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.comment(postHashHex))
                postcard.ids.reclout.icon = recloutIcon
                postcard.ids.reclout.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.reclout(postHashHex))
                postcard.ids.diamond.icon = diamondIcon
                postcard.ids.diamond.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.diamond(postHashHex))
                #postcard.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
                postcard.ids.bCard.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
                if postImage:
                    for image in postImage:
                        imageCard = MDCard(FitImage(source=image, size_hint_y=1, radius=(18, 18,18, 18),), radius=18, md_bg_color="grey",
                        pos_hint={"center_x": .5, "center_y": .5}, size_hint=(0.8, 3.4))
                        postcard.ids.mediaBox.add_widget(imageCard)
                if postVideo:
                    player = VideoPlayer(source=postVideo, state='pause', options={'allow_stretch': True})
                    postcard.ids.mediaBox.add_widget(player)
                self.ids.singlePost.add_widget(postcard)
