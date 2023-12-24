import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [width * [0] for _ in range(height)]

        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                value = self.board[i][j]

                color = [(255, 255, 255), (255, 0, 0), (0, 0, 255)][value]
                w = [1, 0, 0][value]

                pygame.draw.rect(screen, color, (
                    self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size), w)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos[0] - self.left, mouse_pos[1] - self.top
        if x in range(self.width * self.cell_size) and y in range(self.height * self.cell_size):
            return mouse_pos
        return None

    def on_click(self, cell):
        if cell:
            num_w, num_h = (cell[0] - self.left) // self.cell_size, (cell[1] - self.top) // self.cell_size
            if self.board[num_h][num_w] == 2:
                self.board[num_h][num_w] = 0
            else:
                self.board[num_h][num_w] += 1

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


if __name__ == '__main__':

    pygame.init()
    pygame.display.set_caption('Клеточки')
    width, height = 400, 500
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    fps = 1

    board = Board(5, 7)
    board.set_view(50, 50, 50)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()