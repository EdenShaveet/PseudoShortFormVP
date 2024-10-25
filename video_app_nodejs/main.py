from kivy.app import App
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import NumericProperty

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
        self.size_hint_y = None
        self.height = Window.height

        #initialize video player with video paused and muted
        self.video_player = VideoPlayer(source=video_source, state='pause', options={'eos': 'loop'})
        self.video_player.size_hint = (1, 1)
        self.video_player.allow_fullscreen = False
        self.video_player.volume = 0  #mute audio (default)

        self.add_widget(self.video_player)

    def play_video(self):
        """Play video and unmute audio."""
        self.video_player.state = 'play'
        self.video_player.volume = 1  #turn on audio

    def pause_video(self):
        """Pause video and mute audio."""
        self.video_player.state = 'pause'
        self.video_player.volume = 0  #mute audio

class PagingScrollView(ScrollView):
    current_index = NumericProperty(0)

    def __init__(self, **kwargs):
        super(PagingScrollView, self).__init__(**kwargs)
        self.total_videos = len(videos)
        self.bind(scroll_y=self.check_snap_position)
        self.snapping = False  #track if video snapping to prevent double snapping

    def check_snap_position(self, *args):
        if self.snapping:
            return

        #find central position and determine which video is closest
        page_height = 1 / (self.total_videos - 1)
        target_index = int(round(self.scroll_y / page_height))
        target_index = max(0, min(self.total_videos - 1, target_index))

        #if current scroll position is close to target position, snap video into place
        central_y = target_index * page_height
        if abs(self.scroll_y - central_y) < 0.5: #threshold for responsiveness
            self.snapping = True
            Clock.schedule_once(lambda dt: self.snap_to_index(target_index), 0.1)

    def snap_to_index(self, index):
        """Scroll to a specific video index, play it, and pause others."""
        self.current_index = index
        self.scroll_y = index / (self.total_videos - 1)
        self.snapping = False  #reset snapping state

        #play the vid at current index and pause all others
        for i, video_card in enumerate(self.children[0].children):
            if i == index:
                video_card.play_video()
            else:
                video_card.pause_video()

class VideoApp(App):
    def build(self):
        Window.size = (dp(360), dp(640))  #simulate a mobile screen size (may need to adjusy when we get our study device)

        #create PagingScrollView instance for snapping behavior
        scroll_view = PagingScrollView()
        layout = BoxLayout(orientation='vertical', size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        #add video cards
        for video in videos:
            video_card = VideoCard(video_source=video["source"])
            layout.add_widget(video_card)

        #add layout to PagingScrollView
        scroll_view.add_widget(layout)

        return scroll_view

#main method
if __name__ == "__main__":
    VideoApp().run()
