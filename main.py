import json
import deso
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.toast.kivytoast.kivytoast import toast
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty


reader = ''

class CircularAvatarImage(MDCard):
    avatar = StringProperty()
    name = StringProperty()


class StoryCreator(MDCard):
    avatar = StringProperty()


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


class HomePage(MDScreen):
    profile_picture = 'https://avatars.githubusercontent.com/u/89080192?v=4'
    def toaster(self, pkb):
    	global reader
    	
    	reader = pkb
    	
    	self.ids.stories.clear_widgets()
    	self.list_stories()
    	self.ids.timeline.clear_widgets()
    	self.list_posts()
    	
    def on_enter(self):
        self.list_stories()
        self.list_posts()

    def list_stories(self):
        global reader
        desoMetadata = deso.Metadata()
        price = desoMetadata.getExchangeRate().json()# getDiamondLevelMap takes optional inDesoNanos argument which is by default True.
        toast(str(price))
        dollars = price['USDCentsPerDeSoExchangeRate']/100
        self.ids.desoprice.text = str(dollars)
        if reader: 
        	toast('using reader' + reader)
        	userposts = deso.Posts().getPostsStateless(numToFetch=10, readerPublicKey = reader, getPostsForFollowFeed = True)
        else:
        	userposts = deso.Posts().getPostsStateless(numToFetch=10)
        for post in userposts.json()['PostsFound']:
            	self.ids.stories.add_widget(CircularAvatarImage(
                avatar = deso.User().getProfilePicURL(post['ProfileEntryResponse']['PublicKeyBase58Check']),
                name = post["ProfileEntryResponse"]['Username'],
                    #avatar=data[name]['avatar'],
                    #name=name,
                    on_press=lambda x: self.toaster(post['ProfileEntryResponse']['PublicKeyBase58Check'])
             
                ))

    def list_posts(self):
        global reader
        if reader: 
        	toast('using reader' + reader)
        	userposts = deso.Posts().getPostsStateless(numToFetch=10, readerPublicKey = reader, getPostsForFollowFeed = True)
        else:
        	userposts = deso.Posts().getPostsStateless(numToFetch=10)
        
        for post in userposts.json()['PostsFound']:
        	readmore = ''
        	if len(post['Body']) > 144:
        		readmore = '  -- read more --'
        	postImage = ''
        	if post['ImageURLs']:
        		postImage = post['ImageURLs'][0]
        	self.ids.timeline.add_widget(PostCard(
        username = post["ProfileEntryResponse"]['Username'],
        
        avatar = deso.User().getProfilePicURL(post['ProfileEntryResponse']['PublicKeyBase58Check']),
        likes = str(post['LikeCount']),
        comments = str(post['CommentCount']),
        body = str(post['Body']),
        readmore = readmore,
        post = postImage,
        diamonds = str(post['DiamondCount']),
        repost = str(post['RepostCount'])
        ))


class MainApp(MDApp):
    def build(self):
        
        Builder.load_file('home_page.kv')
        return HomePage()

    def on_start(self):
        self.root.dispatch('on_enter')


if __name__ == "__main__":
    MainApp().run()
