from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, PushMatrix, PopMatrix, Rotate, Color, Ellipse
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.vector import Vector
from PIL import Image as PILImage
import numpy as np


class Car(Widget):
    angle = NumericProperty(0)  # Rotation angle
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    sensor1_x = NumericProperty(0)
    sensor1_y = NumericProperty(0)
    sensor1 = ReferenceListProperty(sensor1_x, sensor1_y)

    sensor2_x = NumericProperty(0)
    sensor2_y = NumericProperty(0)
    sensor2 = ReferenceListProperty(sensor2_x, sensor2_y)

    sensor3_x = NumericProperty(0)
    sensor3_y = NumericProperty(0)
    sensor3 = ReferenceListProperty(sensor3_x, sensor3_y)

    def __init__(self, sand, **kwargs):
        super().__init__(**kwargs)
        self.sand = sand
        with self.canvas:
            PushMatrix()
            self.rot = Rotate(angle=self.angle, origin=self.center)
            self.car_rect = Rectangle(source='images/car.png', pos=self.pos, size=(20, 10))
            PopMatrix()

            Color(0.48, 0.97, 0.74, 0.5)
            self.sensor1_ellipse = Ellipse(pos=self.sensor1, size=(10, 10))  # Front
            self.sensor2_ellipse = Ellipse(pos=self.sensor2, size=(10, 10))  # Right
            self.sensor3_ellipse = Ellipse(pos=self.sensor3, size=(10, 10))  # Left

    def move(self, rotation):
        self.angle += rotation
        self.rot.angle = self.angle
        self.velocity = Vector(2, 0).rotate(self.angle)  # Move in direction of angle
        new_pos = Vector(*self.velocity) + self.pos

        #print(f"Car center: {self.center}, Sensor1: {self.sensor1}")

        # Boundary checks (5-pixel margin)
        if new_pos[0] < 5:
            new_pos[0] = 5
        elif new_pos[0] > 1539:  # 1429 - 5
            new_pos[0] = 1539
        if new_pos[1] < 5:
            new_pos[1] = 5
        elif new_pos[1] > 849:  # 660 - 5
            new_pos[1] = 849

        self.pos = new_pos
        self.car_rect.pos = self.pos  # Update rectangle position
        self.rot.origin = self.center  # Update rotation origin

        # Update sensor positions (relative to car angle)
        car_center = Vector(self.center)
       # car_center = self.pos
        self.sensor1 = Vector(30, 0).rotate(self.angle) + car_center  # Front, 30 pixels ahead
        self.sensor2 = Vector(30, 0).rotate(self.angle + 30) + car_center  # Right, 30° offset
        self.sensor3 = Vector(30, 0).rotate(self.angle - 30) + car_center  # Left, -30° offset
        self.sensor1_ellipse.pos = self.sensor1
        self.sensor2_ellipse.pos = self.sensor2
        self.sensor3_ellipse.pos = self.sensor3

        # Check mask values at sensor positions
        self.signal1 = self.get_signal(int(self.sensor1[0]), int(self.sensor1[1]))
        self.signal2 = self.get_signal(int(self.sensor2[0]), int(self.sensor2[1]))
        self.signal3 = self.get_signal(int(self.sensor3[0]), int(self.sensor3[1]))

        # Adjust velocity based on obstacles
        if self.signal1 > 0 or self.signal2 > 0 or self.signal3 > 0:
            self.velocity = Vector(0.5, 0).rotate(self.angle)  # Slow down on obstacles
        else:
            self.velocity = Vector(2, 0).rotate(self.angle)  # Normal speed on roads
    
    def get_signal(self, x, y):
        # Check 20x20 area around sensor, clamp to bounds
        x_start = max(0, x - 10)
        x_end = min(1539, x + 10)
        y_start = max(0, y - 10)
        y_end = min(849, y + 10)
        area = self.sand[y_start:y_end, x_start:x_end]
        return np.mean(area) if area.size > 0 else 1.0  # 1.0 if out of bounds

class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (800, 500)  # Set window size to match image

        # Load mask
        img = PILImage.open("images/mask.png").convert('L')
        self.sand = np.asarray(img) / 255.0  # Normalize to 0-1

        with self.canvas:
            # Add background image
            self.bg = Rectangle(source='images/citymap.png', pos=self.pos, size=(1544, 854))
        self.car = Car(self.sand, pos=(700, 430))  # Center of the window
        self.rotation = 0
        self.add_widget(self.car)
        Clock.schedule_interval(self.update, 1.0 / 60.0)  # 60 FPS
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)
    
    def update(self, dt):
        self.car.move(self.rotation)
        # Print sensor signals for debugging
        print(f"Sensor1: {self.car.signal1:.2f}, Sensor2: {self.car.signal2:.2f}, Sensor3: {self.car.signal3:.2f}")
    
    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if key == 276:  # Left arrow
            self.rotation = 5
        elif key == 275:  # Right arrow
            self.rotation = -5
    
    def on_key_up(self, window, key, scancode):
        if key in (276, 275):
            self.rotation = 0

class SelfDrivingApp(App):
    def build(self):
        return Game()

if __name__ == '__main__':
    SelfDrivingApp().run()