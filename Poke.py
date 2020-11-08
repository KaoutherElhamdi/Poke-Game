from uagame import Window
from pygame.time import Clock, get_ticks as get_ms
from pygame.event import get as get_events
from pygame.draw import circle as draw_circle
from pygame import QUIT, Color, MOUSEBUTTONUP, KEYDOWN, K_q, K_RETURN, init as init_timer, quit, get_init
from random import randint
from math import sqrt

class Dot:
    def __init__(self, radius, width, height, velocity, color):
        self._radius = radius
        self._velocity = velocity
        self._color = color
        self.random_location(width, height)
        
    def draw(self, surface):
        draw_circle(surface, Color(self._color), self._center, self._radius)
        
    def move(self, window):
        self._move_h(window.get_width())
        self._move_v(window.get_height())
        
    def _move_h(self, width):
        self._make_a_move(0, width)
                
    def _move_v(self, height):
        self._make_a_move(1, height)
        
    def _make_a_move(self, i, size):
        self._center[i] = self._center[i] + self._velocity[i]
        if (self._center[i] <= self._radius) or (self._center[i] + self._radius >= size):
            self._velocity[i] *= -1
            
    def random_location(self, width, height):
        w = randint(self._radius, width-self._radius)
        h = randint(self._radius, height-self._radius)
        self._center = [w, h]
        
    def intersection(self, other):
        distance = sqrt(sum([(self._center[i]-other._center[i])**2 for i in range(2)]))
        return distance <= self._radius + other._radius
            
class Game:
    def __init__(self):
        if get_init:
            init_timer()
            
        self._clock = Clock()
        
        self._width = 500
        self._height = 400
        
        self.window = create_window(self._width, self._height)
        self._surface = self.window.get_surface()
        
        #Initialize self._big_dot and self._small_dot
        self._big_dot = Dot(40, self._width, self._height, [2, 1], 'blue')
        self._small_dot = Dot(25, self._width, self._height, [1, 2], 'red')
        
        if self.points_intersection():
            self.randomize_dots()
        
        self._score = 0
        self._close = False
        self._to_remove = get_ms()//1000
        
        init_timer()        
        
    def update_game(self):
        self.window.clear()
        
        self._score = get_ms()//1000 - self._to_remove
        self.window.draw_string("Score: {}".format(self._score),0,0)
        
        self._small_dot.draw(self._surface)
        self._big_dot.draw(self._surface)
        
        self.window.update()
        
        self._big_dot.move(self.window)
        self._small_dot.move(self.window)
        
    def _handle_events(self):
        events = get_events()
        for event in events:
            if event.type == MOUSEBUTTONUP:
                self.randomize_dots()
            if event.type == QUIT:
                self._close = True
            if event.type == KEYDOWN:
                if event.key == K_q:
                    self._close = True
        
    def play(self):
        while not self._close:
            
            self._handle_events()
            
            self.update_game()
            
            self._clock.tick(90)
            
            if self.points_intersection():
                self.game_over()
            
        self.window.close()
    
    def randomize_dots(self):
        self._big_dot.random_location(self._width, self._height)
        while self.points_intersection():
            self._small_dot.random_location(self._width, self._height)
        
    def points_intersection(self):
        return self._big_dot.intersection(self._small_dot)
            
    def game_over(self):
        self.draw_game_over()
        pause = True
        while pause:
            for event in get_events():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                    self._close = True
                    pause = False
                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.__init__()
                    pause = False
        
    def draw_game_over(self):
        replay_msg = "PRESS ENTER  TO PLAY AGAIN"
        game_over_msg = "GAME OVER"
        
        self.window.set_font_size(40)
        self.window.draw_string(replay_msg, (self._width-self.window.get_string_width(replay_msg))//2,(self._height-self.window.get_font_height())//2)
        self.window.set_font_color(self._small_dot._color)
        self.window.set_bg_color(self._big_dot._color)
        self.window.set_font_size(70)
        self.window.draw_string(game_over_msg, 0, self._height-self.window.get_font_height())
        self.window.update()
        
def create_window(width, heigth):
    window = Window('Poke the Dots', width, heigth)
    window.set_bg_color('black')
    window.set_font_size(64)
    return window

def main():
      
    #Start the game
    game = Game()
    
    #Play
    game.play()

main()