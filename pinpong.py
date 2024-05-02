import pygame as PG
import sys # данная библиотека понадобится для корректного выхода из игры
from random import randint
PG.init() # запускаем встроенный функционал PyGame для корректной работы библиотеки

SCREEN_WIDTH = 960 # ширина игрового окна
SCREEN_HEIGHT = 540 # высота игрового окна
SCREEN = PG.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) ) # создаем игровое окно
FPS = 60 # частота обновления экрана (frames per second - количество кадров в секунду)
CLOCK = PG.time.Clock() # создаем счетчик времени между кадрами, для поддержки заданного значения FPS

PG.mixer.init() # запускаем встроенный функционал PyGame для для работы с музыкой и звуками

sound_hit = PG.mixer.Sound('hit.mp3') # создаем звук выстрела и сохраняем в переменную
sound_gol = PG.mixer.Sound('gol.mp3')
PG.mixer.music.load('music_bg.mp3') # создаем фоновую музыку для игры
PG.mixer.music.set_volume(0.7) # задаем громкость для фоновой музыки
PG.mixer.music.play() # запускаем фоновую музыку

bg_image = PG.image.load('bg.jpg') # загружаем фоновое изображение
bg = PG.transform.scale( bg_image, (960, 540) ) # задаем размер для фонового изображения

p1_image = PG.transform.scale( PG.image.load('p_1.png'),(40, 240)) # загружаем изображение игрока
p2_image = PG.transform.scale( PG.image.load('p_2.png'),(40, 240))
ball_image = PG.transform.scale( PG.image.load('ball.png'),(40, 40))


# класс для создания надписей
class Label(): # text - текст надписи, x и y - координаты, align - направление, font_size - размер, color- цвет
    def __init__(self, text, x, y, align = 'left', font_size = 36, color = (255, 255, 255)):
        self.font = PG.font.Font(None, font_size) # создаем шрифт (None - любой системный, font_size - размер)
        self.align = align # сохраняем направления для перерасчета координат отрисовки
        self.color = color
        self.x = x # сохраняем начальную координату x для перерасчета координат отрисовки
        self.y = y # сохраняем начальную координату y для перерасчета координат отрисовки
        self.render(text) # обновляем текст
    
    def render(self, text): # метод обновления текста
        self.text = self.font.render(text, True, self.color) # переводим текст в набор пикселей (True - сглаживать пиксели)
        self.rect = self.text.get_rect() # определяем прямоугольник по размеру текста
        self.rect.centery = self.y # задаем прямоугольнику для отрисовки текста координаты x и y
        if self.align == 'left': self.rect.left = self.x
        elif self.align == 'right': self.rect.right = self.x
        else : self.rect.centerx = self.x

# создаем надпись 'GAME OVER'
label_game_over = Label('GAME OVER', SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.5, 'center', 72, (255, 0, 0))

# класс игрока (наследуемся от PG.sprite.Sprite, для удобной проверки столкновений)
class Player_left(PG.sprite.Sprite):
    def __init__(self):
        PG.sprite.Sprite.__init__(self) # вызываем конструктор родительского класса (обязательно)
        self.image = p1_image
        self.rect = self.image.get_rect() # определяем прямоугольник по размеру изображения
        self.rect.x = 0
        self.rect.centery = SCREEN_HEIGHT * 0.5
        self.speed = 5 # скорость игрока
        self.score = 0 # очки игрока
        self.score_label = Label(f'{self.score}', 15, 15, 'left')

    def update(self): # метод обновления игрока
        # ДВИЖЕНИЕ
        KEY = PG.key.get_pressed() # получаем список всех клавиш, которые были нажаты между обновлениями экрана
        
        if KEY[PG.K_w]: # если среди них была СТРЕЛКА ВВЕРХ
            self.rect.y -= self.speed # - двигаем игрока вверх
            if self.rect.centery < 0 : self.rect.centery = 0 # не даем выйти за пределы экрана
        elif KEY[PG.K_s]: # если среди них была СТРЕЛКА ВНИЗ
            self.rect.y += self.speed # - двигаем игрока вниз
            if self.rect.centery > SCREEN_HEIGHT : self.rect.centery = SCREEN_HEIGHT # не даем выйти за пределы экрана

       
        SCREEN.blit(self.image, self.rect)
        
class Player_right(PG.sprite.Sprite):
    def __init__(self):
        PG.sprite.Sprite.__init__(self) # вызываем конструктор родительского класса (обязательно)
        self.image = p2_image
        self.rect = self.image.get_rect() # определяем прямоугольник по размеру изображения
        self.rect.right = SCREEN_WIDTH
        self.rect.centery = SCREEN_HEIGHT * 0.5
        self.speed = 5 # скорость игрока
        self.score = 0 # очки игрока
        self.score_label = Label(f'{self.score}', SCREEN_WIDTH -15, 15, 'right')

    def update(self): # метод обновления игрока
        # ДВИЖЕНИЕ
        KEY = PG.key.get_pressed() # получаем список всех клавиш, которые были нажаты между обновлениями экрана
        
        if KEY[PG.K_UP]: # если среди них была СТРЕЛКА ВВЕРХ
            self.rect.y -= self.speed # - двигаем игрока вверх
            if self.rect.centery < 0 : self.rect.centery = 0 # не даем выйти за пределы экрана
        elif KEY[PG.K_DOWN]: # если среди них была СТРЕЛКА ВНИЗ
            self.rect.y += self.speed # - двигаем игрока вниз
            if self.rect.centery > SCREEN_HEIGHT : self.rect.centery = SCREEN_HEIGHT # не даем выйти за пределы экрана

       
        SCREEN.blit(self.image, self.rect)

# класс пули (наследуемся от PG.sprite.Sprite, для удобной проверки столкновений)
class Ball(PG.sprite.Sprite):
    def __init__(self):
        PG.sprite.Sprite.__init__(self) # вызываем конструктор родительского класса (обязательно)
        self.image = ball_image # задаем спрайту изображение нужного размера
        self.rect = self.image.get_rect() # определяем прямоугольник по размеру изображения
        self.rect.centerx = SCREEN_WIDTH * 0.5 # задаем прямоугольнику координаты
        self.rect.centery = SCREEN_HEIGHT * 0.5
        self.speed = 10 # скорость пули
        self.speed_x = self.speed if randint(0,1)==0 else -self.speed
        self.speed_y = self.speed if randint(0,1)==0 else -self.speed
    def update(self): # метод обновления
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top <0:
            sound_hit.play() 
            self.rect.top = 0
            self.speed_y *= -1
        if self.rect.bottom >SCREEN_HEIGHT:
            sound_hit.play()
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y *= -1  
        if PG.Rect.colliderect(self.rect, p1.rect):
            sound_hit.play()
            self.rect.left = p1.rect.right
            self.speed_x *= -1
        if PG.Rect.colliderect(self.rect, p2.rect):
            sound_hit.play()
            self.rect.right = p2.rect.left
            self.speed_x *= -1 
        if self.rect.left <0:
            sound_gol.play()
            p2.score += 1
            p2.score_label.render(f'{p2.score}')
            self.rect.centerx = SCREEN_WIDTH * 0.5 # задаем прямоугольнику координаты
            self.rect.centery = SCREEN_HEIGHT * 0.5
            self.speed = 10 # скорость пули
            self.speed_x = self.speed if randint(0,1)==0 else -self.speed
            self.speed_y = self.speed if randint(0,1)==0 else -self.speed
        if self.rect.right >SCREEN_WIDTH:
            sound_gol.play()
            p1.score += 1
            p1.score_label.render(f'{p1.score}')
            self.rect.centerx = SCREEN_WIDTH * 0.5 # задаем прямоугольнику координаты
            self.rect.centery = SCREEN_HEIGHT * 0.5
            self.speed = 10 # скорость пули
            self.speed_x = self.speed if randint(0,1)==0 else -self.speed
            self.speed_y = self.speed if randint(0,1)==0 else -self.speed
        SCREEN.blit(self.image, self.rect) # рисуем пулю в координатах прямоугольника

p1 = Player_left() # создаем игрока
p2 = Player_right()
ball = Ball()

game_loop_is = True # переменная, отвечающая за работу главного цикла игры (работает пока True)

# ГЛАВНыЙ ЦИКЛ ИГРЫ (крутится, пока game_loop_is = True)
while game_loop_is:
    CLOCK.tick(FPS) # ждем, до наступления следующего кадра
    
    

    # проверяем все события, которые произошли между кадрами
    for event in PG.event.get():
        # если окно было закрыто или игрок нажал на клавишу ESCAPE
        if event.type == PG.QUIT or (event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE):
            game_loop_is = False # останавливаем главный игровой цикл

    SCREEN.blit(bg, (0, 0)) # рисуем фон в верхнем левом углу экрана
    p1.update()
    p2.update()
    ball.update()
    SCREEN.blit(p1.score_label.text,p1.score_label.rect)
    SCREEN.blit(p2.score_label.text,p2.score_label.rect)
    PG.display.flip() # обновляем экран игры

# ПОСЛЕ ОСТАНОВКИ ГЛАВНОГО ИГРОВОГО ЦИКЛА
PG.quit() # выходим из Pygame
sys.exit() # закрываем приложение