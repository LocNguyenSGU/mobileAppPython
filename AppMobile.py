from kivy.graphics import Rotate
from kivy.multistroke import rotate_by
from kivy.uix import camera
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.camera import Camera
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

# Đặt kích thước cửa sổ cố định
# Window.size = (350, 600)
print(f"Window size: {Window.size}")

class MenuScreen(Screen):
    pass

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None

    def on_enter(self):
        """Khi màn hình SecondScreen xuất hiện, khởi động camera"""
        self.start_camera()

    def on_leave(self):
        """Tắt camera khi chuyển sang màn hình khác"""
        if self.camera:
            self.camera.play = False

    def start_camera(self):
        """Khởi động camera"""
        if not self.camera:
            # Tạo camera widget
            self.camera = Camera(play=True, allow_stretch=True, keep_ratio=False)
            self.camera.size_hint = (1, 1)  # Camera chiếm toàn màn hình
            self.camera.pos_hint = {'x': 0, 'y': 0}

            # Thêm camera vào màn hình
            self.add_widget(self.camera)


    def capture(self, instance):
        """Chụp ảnh (placeholder)"""
        print("Capture button pressed")


    def switch_to_menu_screen(self, instance):
        """Quay lại màn hình đầu tiên"""
        self.manager.current = "MenuScreen"


class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_leave(self):
        """Làm sạch khi chuyển sang màn hình khác"""
        pass


class AppMobile(MDApp):
    def build(self):
        self.theme_cls.material_style = "M2"
        self.theme_cls.primary_palette = "Green"
        screen = Builder.load_string(screen_helper)
        return screen


    def switch_to_second_screen(self):
        """Chuyển sang màn hình thứ hai"""
        self.root.current = "SecondScreen"
        self.root.get_screen("SecondScreen").start_camera()

    def switch_to_menu_screen(self):
        """Quay lại màn hình đầu tiên"""
        self.root.current = "MenuScreen"


    def switch_to_third_screen(self):
        self.root.current = "ThirdScreen"


screen_helper = """
ScreenManager:
    MenuScreen:
        name: "MenuScreen"
    SecondScreen:
        name: "SecondScreen"
    ThirdScreen: 
        name: "ThirdScreen"

<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'

        # BoxLayout chứa ảnh làm nền (có thể tắt ảnh để debug)
        BoxLayout:
            size_hint_y: None
            height: 220  # Tùy chỉnh chiều cao
            width: 350

            # Hình ảnh làm nền
            Image:
                source: './imageApp/img.png'
                allow_stretch: True  # Cho phép phóng to/thu nhỏ
                keep_ratio: False  # Không giữ tỷ lệ hình ảnh
                size_hint: None, None
                size: self.parent.size  # Đảm bảo ảnh bao phủ hết BoxLayout

            # AnchorLayout để căn chỉnh văn bản bên trên ảnh
            AnchorLayout:
                anchor_x: 'left'
                anchor_y: 'top'
                size_hint: None, None
                width: self.parent.width # Đảm bảo AnchorLayout có chiều rộng như BoxLayout
                height: self.parent.height

                BoxLayout:
                    orientation: 'vertical'
                    spacing: 10
                    size_hint_y: None
                    height: 120  # Đảm bảo chiều cao của BoxLayout đủ để chứa MDLabel
                    halign: 'left'

                    # MDLabel đầu tiên, căn trái
                    MDLabel:
                        text: 'Hi, plant lover!'
                        halign: 'left'
                        theme_text_color: 'Custom'
                        size_hint_x: None
                        width: self.parent.width * 0.9
                        text_size: self.size
                        text_color: 0, 0, 0, 1  # Màu chữ den
                        font_style: 'Caption'
                        pos_hint: {"center_x": -0.5, "center_y": 1}

                    # MDLabel thứ hai, căn trái
                    MDLabel:
                        text: 'Good morning'
                        halign: 'left'
                        theme_text_color: 'Custom'
                        text_color: 0, 0, 0, 1  # Màu chữ den
                        font_style: 'H5'
                        font_name: "Roboto-Bold"  # Font chữ dày
                        size_hint_x: None
                        width: self.parent.width * 0.9
                        text_size: self.size
                        pos_hint: {"center_x": -0.5, "center_y": 1}


        # MDLabel thứ ba nằm dưới
        MDLabel:
            text: 'Hello world'
            halign: 'center'

        # MDBottomAppBar để tạo thanh công cụ dưới
        MDBottomAppBar:
            MDTopAppBar:
                left_action_items: [['home', lambda x: app.switch_to_menu_screen()]]
                right_action_items: [['account-settings', lambda x: app.switch_to_third_screen()]]
                mode: 'center'
                type: 'bottom'
                icon: 'camera'
                text_color: 1, 0, 0, 1
                on_action_button: app.switch_to_second_screen()
                
<SecondScreen>:
    FloatLayout:
        # Camera chiếm toàn bộ màn hình
        Camera:
            id: camera_widget
            play: True
            allow_stretch: True  # Cho phép camera phóng to
            keep_ratio: False    # Không giữ tỷ lệ gốc
            size_hint: 1, 1
            pos_hint: {'x': 0, 'y': 0}

        # Nút chụp ảnh
        Button:
            text: "Capture"
            size_hint: None, None
            size: 150, 50
            pos_hint: {"center_x": 0.5, "y": 0.05}
            on_press: root.capture(self)

        # Nút hủy
        Button:
            text: "Cancel"
            size_hint: None, None
            size: 150, 50
            pos_hint: {"center_x": 0.5, "y": 0.15}
            on_press: root.switch_to_menu_screen(self)

<ThirdScreen>:
    BoxLayout:
        orientation: 'vertical'
        # MDBottomAppBar để tạo thanh công cụ dưới
        MDBottomAppBar:
            MDTopAppBar:
                left_action_items: [['home', lambda x: app.switch_to_menu_screen()]]
                right_action_items: [['account-settings', lambda x: app.switch_to_third_screen()]]
                mode: 'center'
                type: 'bottom'
                icon: 'camera'
                text_color: 1, 0, 0, 1
                on_action_button: app.switch_to_second_screen()

"""
AppMobile().run()