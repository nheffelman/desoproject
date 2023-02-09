from kivy.app import App
from kivy.uix.videoplayer import VideoPlayer



url = "https://www.appsloveworld.com/wp-content/uploads/2018/10/640.mp4"

import requests





class VideoPlayerApp(App):
    def build(self):
        player = VideoPlayer(source=url, state='play',
            options={'allow_stretch': True})
        return player

if __name__ == '__main__':
    VideoPlayerApp().run()
