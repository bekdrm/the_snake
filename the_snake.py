from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс всех объектов в игре."""

    def __init__(self) -> None:
        """Метод __init__ в котором объекту присваиваются атрибуты."""
        self.position = None
        self.body_color = None

    def draw(self):
        """Метод draw который отрисовывает объекты на игровом поле."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    x_positions = [x for x in range(0, SCREEN_WIDTH, 20)]
    y_positions = [y for y in range(0, SCREEN_HEIGHT, 20)]

    def __init__(self):
        """
        Инициализирует яблоко с определенным цветом
        и случайной позицией.
        """
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """
        Генерирует случайные координаты для яблока.
        Возвращает координаты (x, y) новой позиции яблока.
        """
        self.position = (choice(self.x_positions), choice(self.y_positions))
        return self.position

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        """
        Инициализирует змейку с начальной позицией,
        цветом, направлением, и длинной.
        """
        super().__init__()
        self.positions = [
            ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
            ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        ]
        self.lenght = 1
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

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
        else:
            self.lenght += 1

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Возвращает атрибуты змейки к исходным значениям."""
        self.lenght = 1
        self.direction = RIGHT
        self.positions = [
            ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
            ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        ]
        self.next_direction = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_s and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_a and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_d and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры, управляющая игровым циклом."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.lenght += 1
            snake.positions.append(snake.positions[-1])
            apple.randomize_position()

        if len(snake.positions) > 2 and \
                snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
