from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from kivy.core.window import Window

# Đặt kích thước cửa sổ cố định
Window.size = (350, 600)


class MenuScreen(Screen):
    pass


class SecondScreen(Screen):
    pass


class AppMobile(MDApp):
    def build(self):
        self.theme_cls.material_style = "M2"
        self.theme_cls.primary_palette = "Green"
        screen = Builder.load_string(screen_helper)
        return screen

    def on_menu_press(self):
        print("Menu button pressed")

    def switch_to_second_screen(self):
        # Chuyển sang màn hình thứ hai
        self.root.current = "SecondScreen"

    def switch_to_menu_screen(self):
        # Quay lại màn hình đầu tiên
        self.root.current = "MenuScreen"


screen_helper = """
ScreenManager:
    MenuScreen:
        name: "MenuScreen"
    SecondScreen:
        name: "SecondScreen"

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
                left_action_items: [['home', lambda x: app.on_menu_press()]]
                right_action_items: [['account-settings', lambda x: app.switch_to_second_screen()]]
                mode: 'center'
                type: 'bottom'
                icon: 'camera'
                text_color: 1, 0, 0, 1
                on_action_button: app.switch_to_second_screen()


<SecondScreen>:
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: 'Second Screen'
            left_action_items: [['arrow-left', lambda x: app.switch_to_menu_screen()]]
"""

AppMobile().run()