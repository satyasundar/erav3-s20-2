from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class MyApp(App):
    def __init__(self):
        super().__init__()
        self.click_count = 0

    def build(self):
        # Create a vertical layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create a label
        self.label = Label(text="Click the button!", font_size=20)

        # Create a button
        button = Button(text="Click Me", size_hint=(1, 0.5))
        button.bind(on_press=self.on_button_press)  # Bind button press to a function

        # Add widgets to layout
        layout.add_widget(self.label)
        layout.add_widget(button)

        return layout

    def on_button_press(self, instance):
        # Update label text when button is pressed
        self.click_count += 1
        self.label.text = f"Button clicked {self.click_count} times!"

if __name__ == '__main__':
    MyApp().run()