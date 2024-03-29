from linkpreview import link_preview
import webbrowser
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
from kivy.uix.image import AsyncImage
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.card import (
    MDCardSwipe, MDCardSwipeLayerBox, MDCardSwipeFrontBox, MDCard
)
from kivymd.uix.list import MDList, OneLineListItem, OneLineAvatarIconListItem, ImageLeftWidget, IconRightWidget
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRoundFlatButton, MDFillRoundFlatIconButton, MDRectangleFlatIconButton, MDIconButton, MDFillRoundFlatButton, MDFlatButton
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
        
#unpickles the current settings
def unpickle_settings():
    if os.path.exists('temp/settings.pickle'):
        with open('temp/settings.pickle', 'rb') as handle:
            settings = pickle.load(handle)
            
    else:
        settings = {}  
    return settings

#pickles transactions
def pickle_transactions(transactions):
    with open('temp/transactions.pickle', 'wb') as handle:
        pickle.dump(transactions, handle, protocol=pickle.HIGHEST_PROTOCOL)


#unpickles transactions
def unpickle_transactions():
    if os.path.exists('temp/transactions.pickle'):
        with open('temp/transactions.pickle', 'rb') as handle:
            transactions = pickle.load(handle)

    else:
        transactions = {}  
    return transactions

#unpickles the current post
def unpickle_post():
    with open('temp/post.pickle', 'rb') as handle:
        post = pickle.load(handle)
        
    return post
#pickles the current post
def pickle_post(post):
    
    with open('temp/post.pickle', 'wb') as handle:
        pickle.dump(post, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
# unpickles the user's profile
def unpickle_profile():
    with open('temp/profile.pickle', 'rb') as handle:
        profile = pickle.load(handle)
        
    return profile

# pickles the user's profile
def pickle_profile(profile):
    if not os.path.exists('temp/settings.pickle'):
        os.makedirs('temp')
    with open('temp/profile.pickle', 'wb') as handle:
        pickle.dump(profile, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
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

#pickle profile pics cache
def pickle_profilePicUrl(cache):
    if not os.path.exists('temp/'):
        os.makedirs('temp/')
    with open('temp/profilePicUrl.pickle', 'wb') as handle:
        pickle.dump(cache, handle, protocol=pickle.HIGHEST_PROTOCOL)
        

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

class CommentLabel(ButtonBehavior, MDLabel):
    pass

# class for the avatar circle
class CircularAvatarImage(MDCard):
    avatar = StringProperty()
    name = StringProperty()

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
    bookmarks = StringProperty()
    bookmarked = BooleanProperty()

class RecloutLayout(MDBoxLayout):
	pass           

class LineEllipse3(Widget):
    points = ListProperty()

class TreeLabel(ButtonBehavior, MDLabel):
    text = StringProperty()

class PostLayout(MDBoxLayout):
    
    postHashHex = StringProperty()

#class for custom comment dialog content
class CommentContent(MDBoxLayout):
    comment = StringProperty()

#class for custom dialog content
class Content(MDBoxLayout):
    quote = StringProperty()

#class for custom dialog content for links
class LinkContent(MDBoxLayout):
    image = StringProperty()
    title = StringProperty()
    url = StringProperty()

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




#class for reading a single post
class EditTreeScreen(MDScreen):
    profile_picture = StringProperty("") #'https://avatars.githubusercontent.com/u/89080192?v=4'
    username = StringProperty("")
    desoprice = StringProperty("")
    avatar = StringProperty("")
    dialog = None
    follow_unfollow = StringProperty("")
    txnHashHex = StringProperty("")
    
    def on_enter(self):
        profile = unpickle_profile()        
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

    def save(self, postHashHex):
        pass

    def delete(self, postHashHex):
        pass


    def change_post(self, postHashHex):
        pickle_post(postHashHex)
        self.ids.singlePost.clear_widgets()
        self.list_post()

    def open_post(self, postHashHex):
        pickle_post(postHashHex)

        self.manager.current = 'single_post'

    def transactions(self):
        if self.dialog:
            self.dialog.dismiss()
        self.manager.current = 'transactions' 

    #determines to show dialog and saves all transactions to pickle file
    def transaction_function(self, transaction, settings):
        transactions = unpickle_transactions()               
        if 'publicKey' in settings:
            publicKey = settings['publicKey']
            if publicKey in transactions:
                if transaction in transactions[publicKey]:
                    pass
                else:
                    transactions[publicKey].append(transaction)
            else:
                transactions[publicKey] = [transaction]
        pickle_transactions(transactions)

        #check settings to see if transaction dialog is true, show the transaction dialog
        if 'transaction_dialog' in settings:
            if settings['transaction_dialog'] == True:
                self.transaction_dialog = True
            else:
                self.transaction_dialog = False
        else:
            settings['transaction_dialog'] = True
            self.transaction_dialog = True
            pickle_settings(settings)
        if self.transaction_dialog:
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Transaction",
                    text=str(transaction)[:288],
                    type="simple",
                    buttons=[
                        MDFlatButton(
                            text="Transactions",
                            theme_text_color="Custom",
                            on_release=lambda x: self.transactions(), 
                        ),
                        MDFlatButton(
                            text="Close",
                            theme_text_color="Custom",
                            #text_color=self.theme_cls.primary_color,
                            on_release=lambda x: self.dialog.dismiss(),

                        ),
                    ],
                )
            self.dialog.open()
        return


	#expands comments to display sub comments
    def expand_comment(self, postHashHex, commentLayout):
        profile = unpickle_profile()
        userposts, following  = self.get_posts()
        desopost = deso.Posts()
        desopost.readerPublicKey = profile['Profile']['PublicKeyBase58Check']
        post = desopost.getSinglePost(postHashHex=postHashHex).json()

        if 'error' in post:
            toast('An error occured getting this post')
        else:            
            post = post['PostFound']
            nftImage = ''
            if post['IsNFT']:
                pass
        
        #iterate through the comments in the post if there are any
            if post['Comments']:
                for comment in post['Comments']:

                    #create a post comments layout
                    subCommentLayout = MDBoxLayout(orientation='vertical', adaptive_height=True, spacing=30)
                    
                    header = MDBoxLayout(orientation='horizontal', adaptive_height=True, size_hint_x = 1)
                    #one line avatar list item
                    username=str(comment["ProfileEntryResponse"]['Username'])
                    avatar = getCachedProfilePicUrl(comment['ProfileEntryResponse']['PublicKeyBase58Check'])
                    olali = OneLineAvatarListItem(text=username, divider = None, _no_ripple_effect = True)
                    ilw = ImageLeftWidget(source=avatar, radius = [20, ])                              
                    #add the avatar to the list item
                    olali.add_widget(ilw)
                    
                    #add the three dots to the header
                    #add data to dots menu 
                    if post['PosterPublicKeyBase58Check'] in following:
                        data = self.change_3dots_data(following=True)
                    else:
                        data = self.change_3dots_data(following=False)
                    three_dots = MDIconButton(icon='dots-vertical')
                    three_dots.bind(on_press=lambda widget: self.toast_3dots(data, post['PosterPublicKeyBase58Check']))

                                       
                    #add the one line avatar list item to the header
                    header.add_widget(olali)
                    header.add_widget(three_dots)
                    
                    #add the header to the comment layout
                    subCommentLayout.add_widget(header)
                    subCommentLayout.height += header.height


                    #get the post body and find any links
                    body=str(comment['Body'])
                    lineCount = 1
                    lineCount += body.count('\n')
                    postLength = len(body)
                    recloutHeight = 0

                    urls = re.findall(r'(https?://[^\s]+)', body)
                    #separate the links from the body text make labels for the text and cards for the links, then add them to the layout
                    previewHeight = 0
                    for url in urls:
                        beforeUrl = body.split(url,1)[0]

                        if beforeUrl !='':
                            bodyLabel = TreeLabel(text=beforeUrl, padding=[20, 20])
                            bodyLabel.bind(on_press= lambda widget, commentLayout=subCommentLayout, postHashHex=comment['PostHashHex']: self.expand_comment(postHashHex, commentLayout))
                            subCommentLayout.add_widget(bodyLabel)
                            subCommentLayout.height += bodyLabel.height

                        body = body.split(url,1)[1] 
                        
                        try:
                            preview = link_preview(url)
                        except:
                            preview = None
                        if preview:
                            
                            if preview.image:

                                preview_image = MDCard(size_hint_y = None, radius=18)
                                fitimage = FitImage(size_hint_y = None ,source=preview.image, height = 300, radius=(18, 18,18, 18),)
                                preview_image.add_widget(fitimage)
                                preview_image.bind(on_press= lambda widget, commentLayout=subCommentLayout, postHashHex=comment['PostHashHex']: self.expand_comment(postHashHex, commentLayout))
                                preview_image.height = 300
                                subCommentLayout.add_widget(preview_image)    
                                subCommentLayout.height += preview_image.height
                        else:
                            urlLabel = MDLabel(text=url, halign =  "center" )
                            subCommentLayout.add_widget(urlLabel)
                            subCommentLayout.height += urlLabel.height
                            previewHeight -= 250
                    #add any remaining body to the layout
                    if body != '':
                        bodyLabel = TreeLabel(text=body, padding= [20,20])
                        bodyLabel.bind(on_press= lambda widget, commentLayout=subCommentLayout, postHashHex=comment['PostHashHex']: self.expand_comment(postHashHex, commentLayout))
                        #add the body card to the layout
                        subCommentLayout.add_widget(bodyLabel)
                        subCommentLayout.height += bodyLabel.height
                    
                    #create a card for the post Image
                    postImage = ''
                    imageHeight = 0
                    if comment['ImageURLs']:                 
                        
                        #swiper = MDSwiper(swipe_on_scroll = True, size_hint_y = None, height = 300, radius=(18, 18,18, 18), ) 
                        for image in comment['ImageURLs']:
                            card = MDCard(size_hint_y = None, radius=18)
                            fitimage = FitImage(size_hint_y = None, source=image, height = 300, radius=(18, 18,18, 18),)
                            card.add_widget(fitimage)
                            #swiper.add_widget(swiperItem)
                        #imageHeight = 300
                            bodyLabel.bind(on_press= lambda widget, commentLayout=subCommentLayout, postHashHex=comment['PostHashHex']: self.expand_comment(postHashHex, commentLayout))
                            #swiperBox.add_widget(swiper)
                            card.height = 300
                            subCommentLayout.add_widget(card)
                            subCommentLayout.height += card.height 
                    if comment['VideoURLs']:


                        postVideo = comment['VideoURLs'][0]
                        player = VideoPlayer(size_hint_y = None, source=postVideo, state='pause', options={'allow_stretch': True})
                        bodyLabel.bind(on_press= lambda widget, commentLayout=subCommentLayout, postHashHex=comment['PostHashHex']: self.expand_comment(postHashHex, commentLayout))
                        subCommentLayout.add_widget(player)
                        subCommentLayout.height += player.height

                    #check if post is nft
                        if comment['IsNFT']:

                            #bind a mdiconbutton to the postcard to open the nft modal
                            nftButton = MDFillRoundFlatIconButton(icon='nfc-variant', text='NFT', pos_hint={'center_x': 0.45, 'center_y': 0.5}, size_hint=(0.8, None))
                            nftButton.bind(on_press=lambda widget, postHashHex=comment['PostHashHex'], nftImageURL=comment['ImageURLs'][0],
                                numNftCopies = str(comment['NumNFTCopies']), nftTitle=str(comment['Body']), numNftCopiesForSale = str(comment['NumNFTCopiesForSale']): 
                                self.open_nft_modal(postHashHex, nftImageURL, numNftCopies, numNftCopiesForSale, nftTitle))
                            subCommentLayout.ids.nftButtonBox.add_widget(nftButton)
                            subCommentLayout.height += nftButton.height

                    #declare the icons
                    recloutIcon = 'repeat'
                    diamondIcon = 'diamond-outline'
                    likeIcon = 'heart-outline'

                    #get the number of reactions
                    comments=str(comment['CommentCount'])
                    likes=str(comment['LikeCount'])
                    diamonds=str(comment['DiamondCount'])
                    reclout=str(comment['RepostCount'])
                    reclouted = False
                    diamonded = False
                    liked = False

                    if comment['PostEntryReaderState']:
                        recloutedByReader = comment['PostEntryReaderState']['RepostedByReader']
                        if recloutedByReader == True:
                            recloutIcon = 'repeat-variant'
                            reclouted = True
                        
                        diamondedByReader = comment['PostEntryReaderState']['DiamondLevelBestowed']
                        if diamondedByReader != 0:
                            diamondIcon = 'diamond'
                            diamonded = True
                        
                        likedByReader = comment['PostEntryReaderState']['LikedByReader']
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
                    reactions.ids.like.bind(on_press=lambda widget, reactions=reactions, liked=liked, postHashHex=comment['PostHashHex']: self.like(postHashHex, liked, reactions))
                    reactions.ids.comment.bind(on_press=lambda widget, reactions=reactions, liked=liked, postHashHex=comment['PostHashHex']: self.comment(postHashHex, reactions))
                    reactions.ids.reclout.icon = recloutIcon
                    reactions.ids.reclout.bind(on_press=lambda widget, reactions=reactions, reclouted=reclouted, postHashHex=comment['PostHashHex']: self.reclout(postHashHex, reclouted, reactions))
                    reactions.ids.diamond.icon = diamondIcon
                    reactions.ids.diamond.bind(on_press=lambda widget, reactions=reactions, diamonded=diamonded, postHashHex=comment['PostHashHex']: self.diamond(postHashHex, liked, reactions))
                    
                    
                    #add the reactions to the layout
                    subCommentLayout.add_widget(reactions)
                    subCommentLayout.height += reactions.height

                    #create a layouts to hold the subcomment
                    emptyLayout = MDBoxLayout(orientation = 'horizontal', adaptive_height = True)
                    leftLayout = MDBoxLayout(orientation = 'vertical', size_hint_x = .15, adaptive_height = True)
                    

                    rightLayout = MDBoxLayout(orientation = 'vertical', size_hint_x = .85, adaptive_height = True, spacing = 25)

                    #leftLayout.height += subCommentLayout.height

                    
                    emptyLayout.add_widget(leftLayout)
                    rightLayout.add_widget(subCommentLayout)
                    rightLayout.height += subCommentLayout.height

                    emptyLayout.add_widget(rightLayout)
                    leftLayout.height += subCommentLayout.height
                    emptyLayout.height += subCommentLayout.height

                    line = LineEllipse3()
                    line.points = [                    
                        leftLayout.width/2, leftLayout.height,
                        leftLayout.width/2, 50,                    
                        leftLayout.width, 50,
                        ]
                    leftLayout.add_widget(line)
                    

                    commentLayout.add_widget(emptyLayout)
                    commentLayout.height += subCommentLayout.height

        
    
            
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
                    self.transaction_function(response.json(), settings)

                else:
                    reactions.ids.like.icon = 'heart'
                    reactions.ids.likes.text = str(int(reactions.ids.likes.text) + 1)
                    reactions.liked = True
                    SEED_HEX = settings['seedHex']
                    PUBLIC_KEY = settings['publicKey']
                    desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
                    response = desoSocial.like(postHashHex=postHashHex, isLike=True)
                    self.transaction_function(response.json(), settings)


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

    #comment a post function allows user to comment a post, updates the comment count, and sends a comment to the blockchain
    def postComment(self, postHashHex, reactions):    

            
        settings=unpickle_settings()
        SEED_HEX = settings['seedHex']
        PUBLIC_KEY = settings['publicKey']
        desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
        response = desoSocial.submitPost(parentStakeID=postHashHex, body=self.dialog.content_cls.ids.comment.text, ).json()
        print(response)
        self.dialog.dismiss()
        self.dialog = None
        if 'error' in response:
            self.transaction_function(response, settings)
            return False
        else:
            reactions.comments = str(int(reactions.comments) + 1)
            self.transaction_function(response, settings)

    def bookmark(self, postHashHex, bookmarked, reactions):
        global loggedIn
        if loggedIn != True:
            toast('You must be logged in to bookmark a post')
        else:   
            settings=unpickle_settings()
            if settings['loggedIn'] == True:
                if reactions.bookmarked == True:
                    reactions.ids.bookmark.icon = 'bookmark-outline'
                    reactions.bookmarked = False
                else:
                    reactions.ids.bookmark.icon = 'bookmark'
                    reactions.bookmarked = True
                    PUBLIC_KEY = settings['publicKey']
                    SEED_HEX = settings['seedHex']
                    association = deso.Associations(publicKey=PUBLIC_KEY, seedHex=SEED_HEX, readerPublicKey=PUBLIC_KEY)
                    response = association.createPostAssociation(transactorKey=PUBLIC_KEY, postHashHex=postHashHex, associationType='bookmarked', associationValue='True').json()
                    if not 'error' in response:
                        association_to_add = association.getPostAssociationsByID(association_id=response['TxnHashHex']).json()
                        if not 'error' in association_to_add:
                            posts = unpickle_posts()
                            if ('bookmarks'+PUBLIC_KEY) in posts:
                                posts['bookmarks'+PUBLIC_KEY].append(association_to_add)
                            else:
                                posts['bookmarks'+PUBLIC_KEY] = [association_to_add]
                            pickle_posts(posts)
                            self.transaction_function(response, settings)
                        else:
                            toast('something went wrong with the block chain response')
                    else:
                        toast('something went wrong creating the bookmark')
                    
                    

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
                    print('receiverPublicKey', receiverPublicKey, post['PostFound']['PosterPublicKeyBase58Check'] )
                    if receiverPublicKey != PUBLIC_KEY:
                        if reactions.diamonded == False:
                            desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
                            response = desoSocial.diamond(postHashHex=postHashHex, receiverPublicKey=receiverPublicKey)
                            print(response.json())
                            reactions.ids.diamond.icon = 'diamond'
                            reactions.diamonds = str(int(reactions.diamonds) + 1)
                            reactions.diamonded = True
                            self.transaction_function(response.json(), settings)
                        else:
                            toast('You have already diamonded this post')
                    else: 
                        toast('You cannot diamond your own post')

    #use a MDDIalog to ask user if they want to repost or quote post
    def clout_or_quoteclout_dialog(self, postHashHex, reclouted, reactions):
        if not self.dialog:
            self.dialog = MDDialog(
            title="Would you like to reclout or quoteclout this post?",
            type="simple",
            items=[
                Item(text="ReClout", source="assets/reclout.png", on_release= lambda *x: self.recloutpressed(postHashHex, reclouted, reactions)),
                Item(text="QuoteClout", source="assets/quoteclout.png", on_release= lambda *x: self.quotecloutpressed(postHashHex, reclouted, reactions)),
            ],
            )
            self.dialog.open()

    # if user selects quoteclout, open a dialog box to enter a quote, else return error to reclout function
    def quotecloutpressed(self, postHashHex, reclouted, reactions):
        self.dialog.dismiss()
        self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
            title="Enter a quote",
            type="custom",
            content_cls=Content(),
            buttons=[
                MDRoundFlatButton(text="CANCEL", on_release=lambda widget: self.dialog.dismiss()),
                MDRoundFlatButton(text="QUOTE", on_release= lambda *x: self.quoteclout(postHashHex, reclouted, reactions)),
            ],
            )
            self.dialog.open()

    #if user selects quoteclout, send a quoteclout to the blockchain and close the dialog box, else return error to reclout function
    def quoteclout(self, postHashHexToQuote, reclouted, reactions):
        
        settings=unpickle_settings()
        SEED_HEX = settings['seedHex']
        PUBLIC_KEY = settings['publicKey']
        desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
        
        quoteclout_response = desoSocial.quote(postHashHexToQuote=postHashHexToQuote, body=self.dialog.content_cls.ids.quote.text, ).json()
        
        self.dialog.dismiss()
        self.dialog = None

        if 'error' in quoteclout_response:
            self.transaction_function(quoteclout_response, settings)
            return False
        self.transaction_function(quoteclout_response, settings)

    #if user selects reclout, send a reclout to the blockchain and close the dialog box, else return error to reclout function
    def recloutpressed(self, postHashHexToRepost, reclouted, reactions):

        self.dialog.dismiss()
        self.dialog = None
        settings=unpickle_settings()
        SEED_HEX = settings['seedHex']
        PUBLIC_KEY = settings['publicKey']
        desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
        reclout_response = desoSocial.repost(postHashHexToRepost).json(), 'repost response'

        if 'error' in reclout_response:
            self.transaction_function(reclout_response, settings)
            return False
        self.transaction_function(reclout_response, settings)


    #reclout a post function allows user to reclout a post, toggles icon reposted, updates the reclout count, and sends a reclout to the blockchain        
    def reclout(self, postHashHex, reclouted, reactions):
        global loggedIn
        if loggedIn != True:
            toast('You must be logged in to reclout a post')
        else:
            settings=unpickle_settings()
            if settings['loggedIn'] == True:

                if self.clout_or_quoteclout_dialog(postHashHex, reclouted, reactions) == False:
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
        self.transaction_function(response.json(), settings)
    
    def follow(self, whoToFollow):
        settings=unpickle_settings()
        SEED_HEX = settings['seedHex']
        PUBLIC_KEY = settings['publicKey']
        desoSocial = deso.Social(nodeURL="https://diamondapp.com/api/v0/", publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
        response = desoSocial.follow(whoToFollow, isFollow=True).json() 
        self.transaction_function(response.json(), settings)

    def storie_switcher(self, publicKey):
        desoUser = deso.User()
        profile = desoUser.getSingleProfile(publicKey=publicKey).json()
        if 'error' in profile:
            toast(profile['error'])
        else:
            pickle_profile(profile)
        
        home = self.manager.get_screen('homepage_read_only')
        home.ids.stories.clear_widgets()
        home.list_stories()
        home.ids.timeline.clear_widgets()
        home.list_posts()
        self.manager.current = 'homepage_read_only'

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

    def home_pressed(self):
        home = self.manager.get_screen('homepage_read_only')
        home.home()
        self.manager.current = 'homepage_read_only'
    
    #goto profile page for logged in user
    def profile_pressed(self, profileKey):
        settings = unpickle_settings()
        settings['profileKey'] = profileKey
        pickle_settings(settings)
        self.manager.current = 'profile'


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

    #function to open a link in the browser but first opens a modal to confirm the user wants to leave the app

    def open_link(self, url, title, image):     
        
        self.linkModal = MDDialog(
            title='Leave app and open link in browser?',
            type="custom",
            content_cls=LinkContent(title=title, image=image),
            buttons=[
                MDRoundFlatButton(text="CANCEL", on_release=lambda widget: self.linkModal.dismiss()),
                MDRoundFlatButton(text="OPEN", on_release=lambda widget, url=url: self.open_browser(url)),
            ],
        )
        self.linkModal.open()

    #function to open browser with url
    def open_browser(self, url):
        webbrowser.open(url)
        self.linkModal.dismiss()

    #pickles ref and sets the current screen search                   
    def ref_pressed(self, ref):
        settings = unpickle_settings()
        settings['ref'] = ref
        pickle_settings(settings)
        self.manager.current = 'search'


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

    
    def get_posts(self):
        profile = unpickle_profile()
        settings = unpickle_settings()
        cached_posts = unpickle_posts()

        #get the users following list
        following = []
        userposts = None
        if 'publicKey' in settings:
            desoUser = deso.User()
            followingResponse = desoUser.getFollowsStateless(publicKey = settings['publicKey']).json()
            for publicKey in followingResponse['PublicKeyToProfileEntry']:
                        following.append(publicKey)         
        
            
        return userposts,following

    def list_post(self):
        userposts, following = self.get_posts()
        PostHashHex = unpickle_post()
        profile = unpickle_profile()
        desopost = deso.Posts()
        desopost.readerPublicKey = profile['Profile']['PublicKeyBase58Check']
        post = desopost.getSinglePost(postHashHex=PostHashHex).json()
        print('posthashhex =',  PostHashHex)
        self.txnHashHex = PostHashHex
        print('post =', post)
        if 'error' in post:
            toast('An error occured getting this post')
        else:            
            post = post['PostFound']
            nftImage = ''
                        
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
            ilw.bind(on_press=lambda widget, profileKey = post['ProfileEntryResponse']['PublicKeyBase58Check']: self.profile_pressed(profileKey))                       
            #add the avatar to the list item
            olali.add_widget(ilw)
            
            #add the three dots to the header
            #add data to dots menu 
            if post['PosterPublicKeyBase58Check'] in following:
                data = self.change_3dots_data(following=True)
            else:
                data = self.change_3dots_data(following=False)

            #create an edit button
            save = MDIconButton(icon='content-save')
            save.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.save(postHashHex))
                            
            #create delete button
            delete = MDIconButton(icon='delete')
            delete.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.delete(postHashHex))
            
            #add the one line avatar list item to the header
            header.add_widget(olali)
            header.add_widget(save)
            header.add_widget(delete)
                        
            #add the header to the layout
            layout.add_widget(header)
            layout.height += header.height

            #get the post body and find any links
            body=str(post['Body'])
            
            #finds all hot links in the body
            newText = []
            textList = body.split()
            for i in textList:
                if(i.startswith("#")) or (i.startswith("@")):
                    i = i.replace(i, ('[ref='+i+'][color=0000ff]'+i+'[/color][/ref]'))
                newText.append(i)            	
            body = ' '.join(newText)
            
            #separate the links from the body text make labels for the text and cards for the links, then add them to the layout
            urls = re.findall(r'(https?://[^\s]+)', body)
            previewHeight = 0
            for url in urls:
                beforeUrl = body.split(url,1)[0]
                if beforeUrl !='':
                    bodyLabel = TreeLabel(text=beforeUrl, padding=[20, 20], markup=True)
                    bodyLabel.bind(on_ref_press = lambda widget, ref: self.ref_pressed(ref))
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
                
                        if preview.title:
                            title = CommentLabel(text=preview.title, halign =  "center", font_style = 'H6')  
                            title.bind(on_press= lambda widget, url=url, title=preview.title, image=preview.image: self.open_link(url,title,image))                   
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
                bodyLabel = TreeLabel(text=body, padding= [20,20], markup=True)
                bodyLabel.bind(on_ref_press = lambda widget, ref: self.ref_pressed(ref))
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
                    
                    layout.add_widget(card)
                    layout.height += card.height 

            if post['VideoURLs']:
                postVideo = post['VideoURLs'][0]
                player = VideoPlayer(size_hint_y = None, source=postVideo, state='pause', options={'allow_stretch': True})
                #player.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
                layout.add_widget(player)
                layout.height += player.height            
            
            
            #check if post is a reclout
            #if the post is a reclout add the reclout layout
            if post['RepostedPostEntryResponse'] == None:
                print('not a reclout')
            else:                
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
                ilw.bind(on_press=lambda widget, profileKey = post['RepostedPostEntryResponse']['PosterPublicKeyBase58Check']: self.profile_pressed(profileKey))

                #add the avatar to the list item
                olali.add_widget(ilw)
                #add the three dots to the header
                #add data to dots menu 
                if post['RepostedPostEntryResponse']['PosterPublicKeyBase58Check'] in following:
                    data = self.change_3dots_data(following=True)
                else:
                    data = self.change_3dots_data(following=False)
                three_dots = MDIconButton(icon='dots-vertical')
                three_dots.bind(on_press=lambda widget, data=data, post=post: self.toast_3dots(data, post['RepostedPostEntryResponse']['PosterPublicKeyBase58Check']))
                
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

                #separate the links from the body text make labels for the text and cards for the links, then add them to the layout
                urls = re.findall(r'(https?://[^\s]+)', body)                
                
                previewImages = []
                for url in urls:
                    beforeUrl = body.split(url,1)[0]

                    if beforeUrl != '':
                        bodyLabel = TreeLabel(text=beforeUrl, padding = [25,25], markup=True)
                        bodyLabel.bind(on_press= lambda widget, postHashHex=post['RepostedPostEntryResponse']['PostHashHex']: self.change_post(postHashHex),
                                       on_ref_press = lambda widget, ref: self.ref_pressed(ref))
                        rightLayout.add_widget(bodyLabel)
                        rightLayout.height += bodyLabel.height * 1.5
                    body = body.split(url,1)[1] 
                    #find the image for the link
                    
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
                                title = CommentLabel(text=preview.title, halign =  "center", font_style = 'H6')  
                                title.bind(on_press= lambda widget, url=url, title=preview.title, image=preview.image: self.open_link(url,title,image))                   
                                preview_image.add_widget(title)
                                rightLayout.add_widget(preview_image)
                            else:

                                preview_image.bind(on_press= lambda widget, postHashHex=post['PostHashHex']: self.open_post(postHashHex))
                                rightLayout.add_widget(preview_image)
                            
                    else:
                        urlLabel = MDLabel(text=url, halign =  "center", theme_text_color = "Custom" , text_color = (0, 0, 1, 1) )
                        rightLayout.add_widget(urlLabel)
                        rightLayout.height += urlLabel.height
                        
                #add any remaining body to the layout
                if body != '':
                    bodyLabel = TreeLabel(text=body, padding = [25,25], markup=True)
                    bodyLabel.bind(on_press= lambda widget, postHashHex=post['RepostedPostEntryResponse']['PostHashHex']: self.change_post(postHashHex),
                                   on_ref_press = lambda widget, ref: self.ref_pressed(ref))
                    #add the body card to the layout
                    rightLayout.add_widget(bodyLabel)
                    rightLayout.height += bodyLabel.height * 1.5

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
                            
                            card.bind(on_press= lambda widget, postHashHex=post['RepostedPostEntryResponse']['PostHashHex']: self.change_post(postHashHex))
                            
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
            bookmarkIcon = 'bookmark-outline'
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
            bookmarks='1'
            bookmarked = False
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
                bookmarked=bookmarked,
                bookmarks=bookmarks,
                reclouted=reclouted,
                diamonded=diamonded,
                liked=liked,
            )
            #add the icons to the reactions, i have to pass in reactions to the functions so that i find the objects and can change the icons
            reactions.ids.like.icon = likeIcon
            reactions.ids.like.bind(on_press=lambda widget, reactions=reactions, liked=liked, postHashHex=post['PostHashHex']: self.like(postHashHex, liked, reactions))
            reactions.ids.comment.bind(on_press=lambda widget, reactions=reactions, liked=liked, postHashHex=post['PostHashHex']: self.comment(postHashHex, reactions))
            reactions.ids.reclout.icon = recloutIcon
            reactions.ids.reclout.bind(on_press=lambda widget, reactions=reactions, reclouted=reclouted, postHashHex=post['PostHashHex']: self.reclout(postHashHex, reclouted, reactions))
            reactions.ids.diamond.icon = diamondIcon
            reactions.ids.diamond.bind(on_press=lambda widget, reactions=reactions, diamonded=diamonded, postHashHex=post['PostHashHex']: self.diamond(postHashHex, diamonded, reactions))
            reactions.ids.bookmark.icon = bookmarkIcon
            reactions.ids.bookmark.bind(on_press=lambda widget, reactions=reactions, bookmarked=bookmarked, postHashHex=post['PostHashHex']: self.bookmark(postHashHex, bookmarked, reactions))
            
            #add the reactions to the layout
            layout.add_widget(reactions)
            layout.height += reactions.height

            #create a box layout to make a comment
            newCommentLayout = MDBoxLayout(orientation='horizontal', adaptive_height=True, spacing=30)
            
            #add the users avatar to the comment layout
            profile = unpickle_profile()
            username = profile['Profile']['Username']
            circle=CircularAvatarImage(
            avatar=deso.User().getProfilePicURL(
            profile['Profile']['PublicKeyBase58Check']))   
            newCommentLayout.add_widget(circle)

            #add a label to the comment layout
            commentLabel = CommentLabel(text='Make a Comment', valign='center')  
            commentLabel.bind(on_press=lambda widget, reactions=reactions, postHashHex=post['PostHashHex']: self.comment(postHashHex, reactions))
            newCommentLayout.add_widget(commentLabel)

            #add a reply button to the comment layout
            replyButton = MDFillRoundFlatButton(text='Reply', valign='center', pos_hint={'center_x': 0.45, 'center_y': 0.5})
            replyButton.bind(on_press=lambda widget, postHashHex=post['PostHashHex']: self.comment(postHashHex, reactions))
            newCommentLayout.add_widget(replyButton)
            
            #add the comment layout to layout
            layout.add_widget(newCommentLayout)

            #iterate through the comments in the post if there are any
            if post['Comments']:
                for comment in post['Comments']:

                    #create a post comments layout
                    commentLayout = MDBoxLayout(orientation='vertical', adaptive_height=True, spacing=30)
                    
                    header = MDBoxLayout(orientation='horizontal', adaptive_height=True, size_hint_x = 1)
                    #one line avatar list item
                    username=str(comment["ProfileEntryResponse"]['Username'])
                    avatar = getCachedProfilePicUrl(comment['ProfileEntryResponse']['PublicKeyBase58Check'])
                    olali = OneLineAvatarListItem(text=username, divider = None, _no_ripple_effect = True)
                    ilw = ImageLeftWidget(source=avatar, radius = [20, ]) 
                    ilw.bind(on_press=lambda widget, profileKey = comment['ProfileEntryResponse']['PublicKeyBase58Check']: self.profile_pressed(profileKey))                             
                    #add the avatar to the list item
                    olali.add_widget(ilw)
                    
                    #add the three dots to the header
                    #add data to dots menu 
                    if post['PosterPublicKeyBase58Check'] in following:
                        data = self.change_3dots_data(following=True)
                    else:
                        data = self.change_3dots_data(following=False)
                    three_dots = MDIconButton(icon='dots-vertical')
                    three_dots.bind(on_press=lambda widget: self.toast_3dots(data, post['PosterPublicKeyBase58Check']))
                    
                    #add the one line avatar list item to the header
                    header.add_widget(olali)
                    header.add_widget(three_dots)
                    
                    #add the header to the comment layout
                    commentLayout.add_widget(header)
                    commentLayout.height += header.height


                    #get the post body and find any links
                    body=str(comment['Body'])
                    
                    #finds all hot links in the body
                    newText = []
                    textList = body.split()
                    for i in textList:
                        if(i.startswith("#")) or (i.startswith("@")):
                            i = i.replace(i, ('[ref='+i+'][color=0000ff]'+i+'[/color][/ref]'))
                        newText.append(i)            	
                    body = ' '.join(newText)
                    
                    #separate the links from the body text make labels for the text and cards for the links, then add them to the layout
                    urls = re.findall(r'(https?://[^\s]+)', body)
                    previewHeight = 0
                    for url in urls:
                        beforeUrl = body.split(url,1)[0]

                        if beforeUrl !='':
                            bodyLabel = TreeLabel(text=beforeUrl, padding=[20, 20], markup=True)
                            bodyLabel.bind(on_press= lambda widget, commentLayout=commentLayout, postHashHex=comment['PostHashHex']: self.expand_comment(postHashHex, commentLayout),
                                           on_ref_press = lambda widget, ref: self.ref_pressed(ref))
                            commentLayout.add_widget(bodyLabel)
                            commentLayout.height += bodyLabel.height

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
                        
                                if preview.title:
                                    title = CommentLabel(text=preview.title, halign =  "center", font_style = 'H6')  
                                    title.bind(on_press= lambda widget, url=url, title=preview.title, image=preview.image: self.open_link(url,title,image))                   
                                    preview_image.add_widget(title)
                                preview_image.bind(on_press= lambda widget, postHashHex=comment['PostHashHex']: self.expand_comment(postHashHex))
                                preview_image.height = 300
                                commentLayout.add_widget(preview_image)    
                                commentLayout.height += preview_image.height
                        else:
                            urlLabel = MDLabel(text=url, halign =  "center" )
                            commentLayout.add_widget(urlLabel)
                            commentLayout.height += urlLabel.height
                            previewHeight -= 250
                    #add any remaining body to the layout
                    if body != '':
                        bodyLabel = TreeLabel(text=body, padding= [20,20], markup=True)
                        bodyLabel.bind(on_press= lambda widget, commentLayout=commentLayout, postHashHex=comment['PostHashHex']: self.expand_comment(postHashHex, commentLayout),
                                       on_ref_press = lambda widget, ref: self.ref_pressed(ref))
                        #add the body card to the layout
                        commentLayout.add_widget(bodyLabel)
                        commentLayout.height += bodyLabel.height
                    
                    #create a card for the post Image
                    postImage = ''
                    imageHeight = 0
                    if comment['ImageURLs']:                 
                        
                        #swiper = MDSwiper(swipe_on_scroll = True, size_hint_y = None, height = 300, radius=(18, 18,18, 18), ) 
                        for image in comment['ImageURLs']:
                            card = MDCard(size_hint_y=None, height=450, radius=[18,0])
                            aImage = AsyncImage(source=image, allow_stretch=True, keep_ratio=True)
                            card.add_widget(aImage)
                            #swiper.add_widget(swiperItem)
                        #imageHeight = 300
                            card.bind(on_press= lambda widget, commentLayout=commentLayout, postHashHex=comment['PostHashHex']: self.expand_comment(postHashHex, commentLayout))
                            #swiperBox.add_widget(swiper)
                            card.height = 300
                            commentLayout.add_widget(card)
                            commentLayout.height += card.height 
                    if comment['VideoURLs']:


                        postVideo = comment['VideoURLs'][0]
                        player = VideoPlayer(size_hint_y = None, source=postVideo, state='pause', options={'allow_stretch': True})
                        player.bind(on_press= lambda widget, commentLayout=commentLayout, postHashHex=comment['PostHashHex']: self.expand_comment(postHashHex, commentLayout))
                        commentLayout.add_widget(player)
                        commentLayout.height += player.height

                    #check if post is nft
                        if comment['IsNFT']:

                            #bind a mdiconbutton to the postcard to open the nft modal
                            nftButton = MDFillRoundFlatIconButton(icon='nfc-variant', text='NFT', pos_hint={'center_x': 0.45, 'center_y': 0.5}, size_hint=(0.8, None))
                            nftButton.bind(on_press=lambda widget, postHashHex=comment['PostHashHex'], nftImageURL=comment['ImageURLs'][0],
                                numNftCopies = str(comment['NumNFTCopies']), nftTitle=str(comment['Body']), numNftCopiesForSale = str(comment['NumNFTCopiesForSale']): 
                                self.open_nft_modal(postHashHex, nftImageURL, numNftCopies, numNftCopiesForSale, nftTitle))
                            commentLayout.ids.nftButtonBox.add_widget(nftButton)
                            commentLayout.height += nftButton.height

                    

                    #declare the icons
                    recloutIcon = 'repeat'
                    diamondIcon = 'diamond-outline'
                    likeIcon = 'heart-outline'

                    #get the number of reactions
                    comments=str(comment['CommentCount'])
                    likes=str(comment['LikeCount'])
                    diamonds=str(comment['DiamondCount'])
                    reclout=str(comment['RepostCount'])
                    reclouted = False
                    diamonded = False
                    liked = False

                    if comment['PostEntryReaderState']:
                        recloutedByReader = comment['PostEntryReaderState']['RepostedByReader']
                        if recloutedByReader == True:
                            recloutIcon = 'repeat-variant'
                            reclouted = True
                        
                        diamondedByReader = comment['PostEntryReaderState']['DiamondLevelBestowed']
                        if diamondedByReader != 0:
                            diamondIcon = 'diamond'
                            diamonded = True
                        
                        likedByReader = comment['PostEntryReaderState']['LikedByReader']
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
                    reactions.ids.like.bind(on_press=lambda widget, reactions=reactions, liked=liked, postHashHex=comment['PostHashHex']: self.like(postHashHex, liked, reactions))
                    reactions.ids.comment.bind(on_press=lambda widget, reactions=reactions, liked=liked, postHashHex=comment['PostHashHex']: self.comment(postHashHex, reactions))
                    reactions.ids.reclout.icon = recloutIcon
                    reactions.ids.reclout.bind(on_press=lambda widget, reactions=reactions, reclouted=reclouted, postHashHex=comment['PostHashHex']: self.reclout(postHashHex, reclouted, reactions))
                    reactions.ids.diamond.icon = diamondIcon
                    reactions.ids.diamond.bind(on_press=lambda widget, reactions=reactions, diamonded=diamonded, postHashHex=comment['PostHashHex']: self.diamond(postHashHex, liked, reactions))
                    
                    
                    #add the reactions to the layout
                    commentLayout.add_widget(reactions)
                    commentLayout.height += reactions.height
                    layout.add_widget(commentLayout)
            


            
            
            #add the layout to the timeline
            self.ids.singlePost.add_widget(layout)
                
            pickle_profilePicUrl(getCachedProfilePicUrl.cache)
                    


        