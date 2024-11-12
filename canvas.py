from typing import List
from abc import ABC, abstractmethod

import pygame as pg
pg.init()


class CanvasObject(ABC):
    @abstractmethod
    def update(self, delta: float):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def handle_events(self, events: List[pg.event.Event]):
        pass


class CanvasSettings(CanvasObject):
    MAX_PEN_RADIUS      = 100
    MAX_COLOR_VALUE     = 255
    SETTINGS_WIDTH      = 150
    BACKGROUND_COLOR    = (0, 0, 0)
    FONT_MARKER         = pg.font.Font(None, 20)
    FONT_PANEL          = pg.font.Font(None, 40)
    FONT_COLOR_SELECTED = (0, 255, 255)
    FONT_COLOR          = (255, 255, 255)

    settings = {
        "pen_radius":   10,
        "red_color":    0,
        "green_color":  0,
        "blue_color":   0
    }

    def __init__(self, root: pg.Surface):
        self.root      = root
        self.is_active = False
        self.selected_parameter = 0
        self.right_pressed = False
        self.left_pressed = False

        self.closed_marker = pg.Surface((10, 15))
        self.closed_marker.fill(CanvasSettings.BACKGROUND_COLOR)
        pg.draw.rect(self.closed_marker, CanvasSettings.FONT_COLOR, (0, 0, self.closed_marker.get_width(), self.closed_marker.get_height()), 1)
        self.closed_marker.blit(CanvasSettings.FONT_MARKER.render("S", False, CanvasSettings.FONT_COLOR), (0, 0))

        self.settings_panel = pg.Surface((200, self.root.get_height()))        

    
    def update(self, delta: float):
        if self.right_pressed:
            patameter_name = list(CanvasSettings.settings.keys())[self.selected_parameter]
            match patameter_name:
                case "pen_radius":
                    if self.settings[patameter_name] < CanvasSettings.MAX_PEN_RADIUS:
                        self.settings[patameter_name] += 1
                case "red_color":
                    if self.settings[patameter_name] < CanvasSettings.MAX_COLOR_VALUE:
                        self.settings[patameter_name] += 1
                case "green_color":
                    if self.settings[patameter_name] < CanvasSettings.MAX_COLOR_VALUE:
                        self.settings[patameter_name] += 1
                case "blue_color":
                    if self.settings[patameter_name] < CanvasSettings.MAX_COLOR_VALUE:
                        self.settings[patameter_name] += 1
        
        elif self.left_pressed:
            patameter_name = list(CanvasSettings.settings.keys())[self.selected_parameter]
            match patameter_name:
                case "pen_radius":
                    if self.settings[patameter_name] > 1:
                        self.settings[patameter_name] -= 1
                case "red_color":
                    if self.settings[patameter_name] > 0:
                        self.settings[patameter_name] -= 1
                case "green_color":
                    if self.settings[patameter_name] > 0:
                        self.settings[patameter_name] -= 1
                case "blue_color":
                    if self.settings[patameter_name] > 0:
                        self.settings[patameter_name] -= 1

    def draw(self):
        if not self.is_active:
            self.root.blit(self.closed_marker, (0, 0))
        else:
            self.settings_panel.fill(CanvasSettings.BACKGROUND_COLOR)
            
            panel_width = self.settings_panel.get_width()
            panel_height = self.settings_panel.get_height()
            pg.draw.rect(self.settings_panel, (CanvasSettings.settings["red_color"], CanvasSettings.settings["green_color"], CanvasSettings.settings["blue_color"]), (0, panel_height - 100, panel_width, 100))
            pg.draw.rect(self.settings_panel, CanvasSettings.FONT_COLOR, (0, 0, panel_width, panel_height), 1)
            
            start_pos = 50
            for i, name in enumerate(list(CanvasSettings.settings)):
                if i == self.selected_parameter:
                    self.settings_panel.blit(
                        CanvasSettings.FONT_PANEL.render(f"{name[0]}: {CanvasSettings.settings[name]}", False, CanvasSettings.FONT_COLOR_SELECTED),
                        (10, start_pos + i * 100)
                    )
                else:
                    self.settings_panel.blit(
                        CanvasSettings.FONT_PANEL.render(f"{name[0]}: {CanvasSettings.settings[name]}", False, CanvasSettings.FONT_COLOR),
                        (10, start_pos + i * 100)
                    )
            self.root.blit(self.settings_panel, (0, 0))


    def handle_events(self, events: List[pg.event.Event]):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    self.is_active = not self.is_active
                
                if not self.is_active:
                    break

                if event.key == pg.K_UP:
                    if self.selected_parameter == 0:
                        self.selected_parameter = len(list(CanvasSettings.settings.keys())) - 1
                    else:
                        self.selected_parameter -= 1
                elif event.key == pg.K_DOWN:
                    if self.selected_parameter == len(list(CanvasSettings.settings.keys())) - 1:
                        self.selected_parameter = 0
                    else:
                        self.selected_parameter += 1
                
                elif event.key == pg.K_RIGHT:
                    self.right_pressed = True
                elif event.key == pg.K_LEFT:
                    self.left_pressed = True

            elif event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT:
                    self.right_pressed = False
                elif event.key == pg.K_LEFT:
                    self.left_pressed = False


class Canvas(CanvasObject):
    MIN_SCALE = 0.5
    MAX_SCALE = 2

    def __init__(
            self,
            root: pg.Surface,
            x: int,
            y: int,
            width: int,
            heigth: int,
            ):
        self.root        = root
        self.canvas      = pg.Surface((width, heigth))
        self.canvas.fill((255, 255, 255))
        self.width       = width
        self.height      = heigth
        self.x           = x
        self.y           = y

        self.mouse_left_pressed = False
        self.mouse_right_pressed = False
        self.mouse_middle_pressed = False
        self.last_mouse_pos = pg.mouse.get_pos()
        self.scale = 1


    def update(self, delta: float):
        mouse_position = pg.mouse.get_pos()
        relative_mouse_position = (
            max(mouse_position[0], self.x) - min(mouse_position[0], self.x),
            max(mouse_position[1], self.y) - min(mouse_position[1], self.y)
        )
        is_inside = relative_mouse_position[0] >= 0 and relative_mouse_position[0] <= self.canvas.get_width() and relative_mouse_position[1] >= 0 and relative_mouse_position[1] <= self.canvas.get_height()


        if self.mouse_left_pressed:
            if is_inside:    
                pg.draw.circle(
                    self.canvas,
                    (    
                        CanvasSettings.settings["red_color"],
                        CanvasSettings.settings["green_color"],
                        CanvasSettings.settings["blue_color"]
                    ),
                    relative_mouse_position,
                    CanvasSettings.settings["pen_radius"]
                )
        
        elif self.mouse_right_pressed:
            self.x += mouse_position[0] - self.last_mouse_pos[0]
            self.y += mouse_position[1] - self.last_mouse_pos[1]
            self.last_mouse_pos = mouse_position
        
        #elif self.mouse_middle_pressed:
        #    if mouse_delta[1] > 0 and self.scale > Canvas.MIN_SCALE:
        #        self.scale -= 0.01
        #    elif mouse_delta[1] < 0 and self.scale < Canvas.MAX_SCALE:
        #        self.scale += 0.01

    def draw(self):
        #scaled_canvas = pg.transform.scale(self.canvas, (self.canvas.get_width() * self.scale, self.canvas.get_height() * self.scale))
        self.root.blit(self.canvas, (self.x, self.y))

    def handle_events(self, events: List[pg.event.Event]):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_left_pressed = True
                elif event.button == 3:
                    self.mouse_right_pressed = True
                    self.last_mouse_pos = event.pos
                elif event.button == 2:
                    self.mouse_middle_pressed = True
                #elif event.button == 4:
                #    if self.scale < Canvas.MAX_SCALE:
                #        self.scale += 0.1
                #elif event.button == 5:
                #    if self.scale > Canvas.MIN_SCALE:
                #        self.scale -= 0.1
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_left_pressed = False
                elif event.button == 3:
                    self.mouse_right_pressed = False
                elif event.button == 2:
                    self.mouse_middle_pressed = False


class App(CanvasObject):
    def __init__(
            self,
            root: pg.Surface,
            clock: pg.time.Clock,
            bg_color: List[int],
            fps: int,
            canvas_size: List[int]
            ):
        self.root     = root
        self.bg_color = bg_color
        self.clock    = clock
        self.fps      = fps

        self.objects: List[CanvasObject] = [
            Canvas(
                root,
                0,
                0,
                canvas_size[0],
                canvas_size[1]
            ), CanvasSettings(root)
        ]
    
    def update(self):
        delta = self.clock.tick(self.fps) / 1000
        for obj in self.objects:
            obj.update(delta)

    def draw(self):
        self.root.fill(self.bg_color)
        for obj in self.objects:
            obj.draw()
        pg.display.flip()

    def handle_events(self):
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                self.quit()

        for obj in self.objects:
            obj.handle_events(events)

    def run(self):
        try:    
            while True:
                self.handle_events()
                self.update()
                self.draw()
        except KeyboardInterrupt:
            self.quit()

        except Exception as ex:
            print(ex)
            self.quit()
    
    def quit(self):
        pg.quit()
        quit()

if __name__ == "__main__":
    root = pg.display.set_mode((600, 600))
    pg.display.set_caption("Canvas (S - settings)")
    
    app = App(
        root,
        pg.time.Clock(),
        (0, 0, 0),
        30,
        (1000, 1000)
    )
    app.run()


        
