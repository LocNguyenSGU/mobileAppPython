import os
from datetime import datetime

from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window

# Set window size
Window.size = (350, 600)

class MenuScreen(Screen):
    pass

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None
        self.capture_folder = "captured_images"  # Thư mục lưu ảnh

    def on_enter(self):
        """Start the camera when the screen is entered"""
        self.start_camera()

    def on_leave(self):
        """Stop the camera when switching to another screen"""
        if self.camera:
            self.camera.play = False  # Dừng camera khi rời khỏi màn hình
            self.remove_widget(self.camera)  # Xóa widget camera để giải phóng tài nguyên

    def start_camera(self):
        """Start the camera"""
        if not self.camera:
            # Create a Camera widget
            self.camera = Camera(play=True, allow_stretch=True, keep_ratio=False)
            self.camera.size_hint = (1, 1)  # Camera fills the whole screen
            self.camera.pos_hint = {'x': 0, 'y': 0}
            self.add_widget(self.camera)

            # Add buttons to the layout
            self.add_buttons()

    def add_buttons(self):
        """Add capture and cancel buttons to the layout"""
        # Capture button
        capture_button = Button(
            text="Capture",
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={"center_x": 0.5, "y": 0.05},
            on_press=self.capture
        )
        self.add_widget(capture_button)

        # Cancel button
        cancel_button = Button(
            text="Cancel",
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={"center_x": 0.5, "y": 0.15},
            on_press=self.switch_to_menu_screen
        )
        self.add_widget(cancel_button)

    def capture(self, instance):
        """Capture button pressed, save image to file"""
        print("Capture button pressed")

        # Ensure the capture folder exists
        if not os.path.exists(self.capture_folder):
            os.makedirs(self.capture_folder)

        # Generate a filename with the current date and time
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.capture_folder}/capture_{timestamp}.png"

        # Capture the image and save it to the file
        self.camera.export_to_png(filename)

        print(f"Image saved to {filename}")

    def switch_to_menu_screen(self, instance):
        """Switch to the menu screen"""
        self.manager.current = "MenuScreen"


class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_leave(self):
        """Clean up when leaving the screen"""
        pass


class AppMobile(MDApp):
    def build(self):
        self.theme_cls.material_style = "M2"
        self.theme_cls.primary_palette = "Green"
        screen = Builder.load_string(screen_helper)
        return screen

    def switch_to_second_screen(self):
        """Switch to the second screen"""
        self.root.current = "SecondScreen"
        self.root.get_screen("SecondScreen").start_camera()

    def switch_to_menu_screen(self):
        """Switch back to the menu screen"""
        self.root.current = "MenuScreen"

    def switch_to_third_screen(self):
        """Switch to the third screen"""
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

        BoxLayout:
            size_hint_y: None
            height: 220
            width: 350

            Image:
                source: './imageApp/img.png'
                allow_stretch: True
                keep_ratio: False
                size_hint: None, None
                size: self.parent.size

            AnchorLayout:
                anchor_x: 'left'
                anchor_y: 'top'
                size_hint: None, None
                width: self.parent.width
                height: self.parent.height

                BoxLayout:
                    orientation: 'vertical'
                    spacing: 10
                    size_hint_y: None
                    height: 120
                    halign: 'left'

                    MDLabel:
                        text: 'Hi, plant lover!'
                        halign: 'left'
                        theme_text_color: 'Custom'
                        size_hint_x: None
                        width: self.parent.width * 0.9
                        text_size: self.size
                        text_color: 0, 0, 0, 1
                        font_style: 'Caption'

                    MDLabel:
                        text: 'Good morning'
                        halign: 'left'
                        theme_text_color: 'Custom'
                        text_color: 0, 0, 0, 1
                        font_style: 'H5'
                        font_name: "Roboto-Bold"
                        size_hint_x: None
                        width: self.parent.width * 0.9
                        text_size: self.size
                        pos_hint: {"center_x": -0.5, "center_y": 1}

        MDLabel:
            text: 'Hello world'
            halign: 'center'

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
        Camera:
            id: camera_widget
            play: True
            allow_stretch: True
            keep_ratio: False
            size_hint: 1, 1
            pos_hint: {'x': 0, 'y': 0}

        Button:
            text: "Capture"
            size_hint: None, None
            size: 150, 50
            pos_hint: {"center_x": 0.5, "y": 0.05}
            on_press: root.capture(self)

        Button:
            text: "Cancel"
            size_hint: None, None
            size: 150, 50
            pos_hint: {"center_x": 0.5, "y": 0.15}
            on_press: root.switch_to_menu_screen(self)

<ThirdScreen>:
    BoxLayout:
        orientation: 'vertical'
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