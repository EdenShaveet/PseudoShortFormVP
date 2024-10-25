from kivy.app import App
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.widget import Widget


# Video Data
videos = [
    {"id": "1", "source": "assets/video1.mp4"},
    {"id": "2", "source": "assets/video2.mp4"},
    {"id": "3", "source": "assets/video3.mp4"},
]


class VideoCard(BoxLayout):
    def __init__(self, video_source, **kwargs):
        super(VideoCard, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None  #Ensures each video takes up full height of mobile phone screen
        self.height = Window.height

        self.video_player = VideoPlayer(source=video_source, state='play', options={'eos': 'loop'})
        self.video_player.size_hint = (1, 1)
        self.video_player.allow_fullscreen = False

        self.add_widget(self.video_player)


class VideoApp(App):
    def build(self):
        Window.size = (dp(360), dp(640))  #Simulate a mobile screen size

        #Create ScrollView instance for manual scrolling
        scroll_view = ScrollView()
        layout = BoxLayout(orientation='vertical', size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        #Add video cards
        for video in videos:
            video_card = VideoCard(video_source=video["source"])
            layout.add_widget(video_card)

        #Add layout to ScrollView
        scroll_view.add_widget(layout)

        return scroll_view

#Run main method
if __name__ == "__main__":
    VideoApp().run()