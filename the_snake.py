from random import choice

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
X_POSITIONS = [x for x in range(0, SCREEN_WIDTH, GRID_SIZE)]
Y_POSITIONS = [y for y in range(0, SCREEN_HEIGHT, GRID_SIZE)]
CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
ALL_CELLS = set(
    (x, y)
    for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT))

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (220, 220, 220)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 10
record = 0

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption(f'Игра - Змейка. '
                       f'Ваш рекорд - {record}. '
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
                                  f'-наследнике {type(self).__name__}.')

    def draw_one_segment(self, position, color=None):
        """Отрисовывет на игровом поле сегмент 20х20."""
        color = color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self, body_color=APPLE_COLOR, occupied_cells=CENTER):
        """
        Инициализирует яблоко с определенным цветом
        и случайной позицией.
        """
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells=None):
        """
        Генерирует случайные координаты для яблока.
        Возвращает координаты (x, y) новой позиции яблока.
        """
        while True:
            self.position = (choice(X_POSITIONS), choice(Y_POSITIONS))
            if self.position not in occupied_cells:
                break

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        self.draw_one_segment(self.position)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self, body_color=SNAKE_COLOR):
        """
        Инициализирует змейку с начальной позицией,
        цветом, направлением, и длинной.
        """
        super().__init__(body_color=body_color)
        self.reset()

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
        self.last = self.positions[-1]
        if len(self.positions) > self.lenght:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        # Голова змеи
        self.draw_one_segment(self.get_head_position())

        if self.last:
            self.draw_one_segment(self.last, BOARD_BACKGROUND_COLOR)
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR,
                         pg.Rect(self.last, (GRID_SIZE, GRID_SIZE)), 1
                         )

    def reset(self):
        """Возвращает атрибуты змейки к исходным значениям."""
        self.positions = [CENTER]
        self.lenght = 1
        self.direction = RIGHT
        self.last = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pg.event.get():
        if (event.type == pg.QUIT
           or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)):
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and snake.direction != DOWN:
                snake.update_direction(UP)
            elif event.key == pg.K_s and snake.direction != UP:
                snake.update_direction(DOWN)
            elif event.key == pg.K_a and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            elif event.key == pg.K_d and snake.direction != LEFT:
                snake.update_direction(RIGHT)


def main():
    """Основная функция игры, управляющая игровым циклом."""
    global record
    pg.init()
    snake = Snake()
    apple = Apple(occupied_cells=snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.lenght += 1
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() in snake.positions[1:]:
            record = max(record, len(snake.positions))
            pg.display.set_caption(f'Игра - Змейка. '
                                   f'Ваш рекорд - {record}. '
                                   f'Нажмите ESC, чтобы выйти.')
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
