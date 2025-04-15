from random import choice

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
X_POSITIONS = [x for x in range(0, SCREEN_WIDTH, 20)]
Y_POSITIONS = [y for y in range(0, SCREEN_HEIGHT, 20)]
CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (220, 220, 220)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 10
RECORD = 0

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption(f'Игра - Змейка. '
                       f'Ваш рекорд - {RECORD}. '
                       f'Нажмите ESC, чтобы выйти.')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс всех объектов в игре."""

    def __init__(self, position=None, body_color=None):
        """Метод __init__ в котором объекту присваиваются атрибуты."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод draw который отрисовывает объекты на игровом поле."""
        raise NotImplementedError(f'Метод draw() не реализован в классе'
                                  f'-наследнике {self.__class__.__name__}.')

    def draw_one_segment(self, position, color=None, border_color=None):
        """Отрисовывет на игровом поле сегмент 20х20."""
        if color is None:
            color = self.body_color
        # Сделал для зарисовки хвоста змейки,
        # чтобы можно было убрать след границ клетки,
        # поменяв цвет границы на цвет поля.
        if border_color is None:
            border_color = BORDER_COLOR
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        """
        Инициализирует яблоко с определенным цветом
        и случайной позицией.
        """
        super().__init__(body_color=APPLE_COLOR)
        self.position = self.randomize_position()

    def randomize_position(self, not_empty=None):
        """
        Генерирует случайные координаты для яблока.
        Возвращает координаты (x, y) новой позиции яблока.
        """
        while True:
            self.position = (choice(X_POSITIONS), choice(Y_POSITIONS))
            if not_empty is None or self.position not in not_empty:
                return self.position

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        self.draw_one_segment(self.position)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        """
        Инициализирует змейку с начальной позицией,
        цветом, направлением, и длинной.
        """
        super().__init__(body_color=SNAKE_COLOR)
        self.positions = [CENTER]
        self.lenght = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        if new_direction:
            self.direction = new_direction

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """
        Добавляет координаты новой головы змейки в начало списка
        и удаляет из него её последний сегмент.
        """
        x, y = self.get_head_position()
        x_direction, y_direction = self.direction
        self.positions.insert(0, (
            (x + x_direction * GRID_SIZE) % SCREEN_WIDTH,
            (y + y_direction * GRID_SIZE) % SCREEN_HEIGHT
        ))

        if len(self.positions) > self.lenght:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        # Голова змеи
        self.draw_one_segment(self.get_head_position())

        if self.last:
            self.draw_one_segment(self.last,
                                  BOARD_BACKGROUND_COLOR,
                                  BOARD_BACKGROUND_COLOR
                                  )

    def reset(self):
        """Возвращает атрибуты змейки к исходным значениям."""
        self.__init__()


def handle_keys(snake_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and snake_object.direction != DOWN:
                snake_object.update_direction(UP)
            elif event.key == pg.K_s and snake_object.direction != UP:
                snake_object.update_direction(DOWN)
            elif event.key == pg.K_a and snake_object.direction != RIGHT:
                snake_object.update_direction(LEFT)
            elif event.key == pg.K_d and snake_object.direction != LEFT:
                snake_object.update_direction(RIGHT)
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def main():
    """Основная функция игры, управляющая игровым циклом."""
    global RECORD
    pg.init()
    snake = Snake()
    apple = Apple()
    screen.fill(BOARD_BACKGROUND_COLOR)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.lenght += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            RECORD = max(RECORD, len(snake.positions))
            pg.display.set_caption(f'Игра - Змейка. '
                                   f'Ваш рекорд - {RECORD}. '
                                   f'Нажмите ESC, чтобы выйти.')
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw_one_segment(apple.position, APPLE_COLOR)
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
