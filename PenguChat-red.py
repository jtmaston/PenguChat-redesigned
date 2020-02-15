from kivy.config import Config
from kivy.app import App
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from easygui import fileopenbox
import bcrypt
from imagecropper import create_thumbnail
from Comms.client import kbQueue
from Comms.client import ClientFactory
from twisted.internet import reactor


class ChatApp(App):
    def build(self):
        super(ChatApp, self).build()
        self.root.current = 'login'

    def __init__(self):
        """Set login page size and screen"""
        super(ChatApp, self).__init__()
        Config.set('graphics', 'width', '500')
        Config.set('graphics', 'height', '700')
        self.placeholder = Image(source="Assets/placehold.png")
        self.pfp_byte_arr = None

    def on_request_close(self, timestamp):
        reactor.stop()
        self.stop()

    def sign_up_redirect(self):
        self.root.current = 'signup'

    def sign_up(self):
        pwd = self.root.ids.passwd.text
        pwd_r = self.root.ids.passwd_r.text
        username = self.root.ids.username.text
        if pwd == pwd_r and self.pfp_byte_arr.getvalue() is not None:
            salt = bcrypt.gensalt()
            pwd = bcrypt.hashpw(pwd.encode(), salt)
            command = {'command': 'register', 'args': (username, pwd, salt, self.pfp_byte_arr.getvalue())}
            reactor.connectTCP("localhost", 8123, ClientFactory())
            kbQueue.put(command)

    def login(self):
        pwd = self.root.ids.loginPass.text
        username = self.root.ids.loginUsr.text
        command = {'command': 'login', 'go_around': False, 'args': (username, pwd)}
        reactor.connectTCP("localhost", 8123, ClientFactory())
        kbQueue.put(command)
        self.root.current = 'chatRoom'

    def upload_image(self):
        path = fileopenbox(msg='Choose an image', multiple=False)
        if path is not None: # test
            self.pfp_byte_arr = create_thumbnail(path)
            self.placeholder.texture = CoreImage(self.pfp_byte_arr, ext='png').texture
            self.root.current = 'signup'


if __name__ == '__main__':
    ChatApp().run()
