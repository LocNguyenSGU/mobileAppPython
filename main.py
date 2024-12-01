import os
from datetime import datetime
from PIL import Image as PILImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.widget import Widget
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
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{self.capture_folder}/capture_{timestamp}.png"

        # Capture the image and save it to the file
        self.camera.export_to_png(filename)
        print(f"Image saved to {filename}")

        # Open the captured image and rotate it
        img = PILImage.open(filename)
        img = img.rotate(270, expand=True)  # Rotate 270 degrees

        # Save the rotated image back to the same file
        img.save(filename)
        print(f"Image rotated and saved to {filename}")


    def switch_to_menu_screen(self, instance):
        """Switch to the menu screen"""
        self.manager.current = "MenuScreen"

class ThirdScreen(Screen):
    def on_enter(self):
        """Load history of captured images when entering the screen"""
        self.load_history()

    def load_history(self):
        """Display history of images grouped by date"""
        folder = "captured_images"
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Clear previous history
        grid = self.ids.history_grid
        grid.clear_widgets()

        # Group images by date
        images_by_date = {}
        for filename in os.listdir(folder):
            if filename.endswith(".png"):
                timestamp = filename.split("_")[1].replace(".png", "")
                date = datetime.strptime(timestamp, "%Y%m%d%H%M%S").strftime("%Y-%m-%d")
                if date not in images_by_date:
                    images_by_date[date] = []
                images_by_date[date].append(os.path.join(folder, filename))

            # Display images grouped by date
        for date, images in sorted(images_by_date.items(), reverse=True):
            # Add a label for the date
            date_label = Label(
                text=f"[b]{date}[/b]",
                markup=True,
                size_hint_y=None,
                height=30,
                halign="left",
                valign="middle",
                color = (0, 0, 0, 1)
            )
            date_label.bind(size=date_label.setter('text_size'))
            grid.add_widget(date_label)

            # Add images in rows of 3
            for i in range(0, len(images), 3):
                row = BoxLayout(orientation="horizontal", size_hint_y=None, height=150, spacing=5)
                for img_path in images[i:i + 3]:
                    btn = Button(
                        size_hint=(1, 1),
                        background_normal=img_path,
                        background_down=img_path,
                        on_press=lambda instance, path=img_path: self.show_details(path),
                    )
                    row.add_widget(btn)
                # Fill remaining spaces with empty widgets if the row has fewer than 3 items
                while len(row.children) < 3:
                    row.add_widget(Widget(size_hint=(1, 1)))
                grid.add_widget(row)

    def show_details(self, file_path):
        """Display details of the selected image"""
        timestamp = os.path.basename(file_path).split("_")[1].replace(".png", "")
        date_time = datetime.strptime(timestamp, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")

        detail_screen = DetailScreen(file_path, date_time)
        self.manager.add_widget(detail_screen)
        self.manager.current = detail_screen.name

class DetailScreen(Screen):
    def __init__(self, file_path, date_time, **kwargs):
        super().__init__(**kwargs)
        self.name = "DetailScreen"
        self.file_path = file_path
        self.date_time = date_time

    def on_enter(self):
        """Build detail view when entering the screen"""
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        layout = BoxLayout(orientation="vertical")

        # Add the image
        img = Image(source=self.file_path, allow_stretch=True, keep_ratio=True)
        layout.add_widget(img)

        # Add details
        details = f"Date & Time: {self.date_time}"
        label = Label(
            text=details,
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=50,
            font_size=16,
            color=(0, 0, 0, 1)
        )
        layout.add_widget(label)

        # Add a back button
        back_button = Button(text="Back", size_hint=(1, None), height=50, on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, instance):
        """Go back to ThirdScreen"""
        self.manager.current = "ThirdScreen"
        self.manager.remove_widget(self)



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

    def switch_to_detail_screen(self, file_path, date_time):
        """Switch to the detail screen with the selected image"""
        detail_screen = DetailScreen(file_path, date_time)
        self.root.add_widget(detail_screen)
        self.root.current = detail_screen.name


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
        ScrollView:
            do_scroll_x: False
            do_scroll_y: True
            
            GridLayout:
                id: history_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: [5, 5] 
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