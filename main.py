import pygame
import random
import sqlite3

pygame.init()
width = 300
height = 600
window_size = (width, height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Тетрис")
rows = 20
columns = 10
cell_size = (width/columns, height/rows)
i_shape = [(0, 4), (1, 4), (2, 4), (3, 4)]
j_shape = [(0, 3), (1, 3), (2, 3), (2, 4)]
l_shape = [(0, 3), (1, 3), (2, 3), (2, 2)]
o_shape = [(0, 4), (0, 5), (1, 4), (1, 5)]
s_shape = [(1, 4), (2, 4), (0, 5), (1, 5)]
t_shape = [(0, 4), (1, 4), (2, 4), (1, 5)]
z_shape = [(0, 4), (1, 4), (1, 5), (2, 5)]


def draw_shape(shape, color):
    for pos in shape:
        x, y = pos
        x *= cell_size[0]
        y *= cell_size[1]
        pygame.draw.rect(screen, color, (x, y, cell_size[0], cell_size[1]))


def move_shape_x(shape, dx):
    for pos in range(len(shape[0])):
        shape[0][pos][0] += dx


def move_shape_y(shape, dy):
    for pos in range(len(shape[0])):
        shape[0][pos][1] += dy


def update_grid(shape):
    draw_shape(shape[0], 'black')


def tetromino_center(shape):
    new_shape = []
    max_x = max(list(map(lambda el: el[0], shape)))
    min_y = min(list(map(lambda el: el[1], shape)))
    for pos in shape:
        new_shape.append([pos[0] + columns // 2 - (max_x + 1) // 2, pos[1] - min_y])
    return new_shape


def get_piece_dimensions(fun, piece):
    x = piece[0][0]
    y = piece[0][1]
    for point in piece:
        x = fun(x, point[0])
        y = fun(y, point[1])
    return x, y


def rotate_piece(piece):
    min_x, min_y = get_piece_dimensions(min, piece)
    max_x, max_y = get_piece_dimensions(max, piece)
    dx = max_x - min_x
    dy = max_y - min_y
    new_piece = []
    new_max_x = min_x + dy
    new_max_y = min_y + dx
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if [x, y] in piece:
                x_new = new_max_x - dy // 2
                y_new = new_max_y - dx // 2
                if dy == 3:
                    if y <= max_y - 2:
                        x_new -= 1
                elif dx == 3:
                    if x <= max_x - 2:
                        y_new -= 1
                if y == max_y:
                    x_new = min_x
                elif y == min_y:
                    x_new = new_max_x
                if x == max_x:
                    y_new = new_max_y
                elif x == min_x:
                    y_new = min_y
                if x_new >= columns or x_new < 0:
                    return piece
                new_piece.append([x_new, y_new])
    return new_piece


template_tetrominoes = [i_shape, j_shape, l_shape, o_shape, s_shape, t_shape, z_shape]
colors_tetrominoes = [(180, 22, 26), (250, 255, 78), (120, 250, 90),
                      (120, 203, 255), (82, 74, 255), (225, 49, 255),
                      (255, 180, 243)]
tetrominoes = []
score = 0
game_over = False
running = True
new_tetromino = True
clock = pygame.time.Clock()
frame_rate = 60
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 20)
counter_sec = 0
pygame.time.set_timer(pygame.USEREVENT, 200)
text_surface = my_font.render(str(0), False, (213, 219, 45))
screen.blit(text_surface, (width / columns * (columns - 1), 0))

while running and not game_over:
    if new_tetromino:
        rand_t = random.randint(0, 6)
        color = colors_tetrominoes[rand_t]
        cent_t = tetromino_center(template_tetrominoes[rand_t])
        tetrominoes.append([cent_t, color])
        new_tetromino = False
    for row in range(rows):
        start_pos = (0, row * cell_size[1])
        end_pos = (width, row * cell_size[1])
        pygame.draw.line(screen, (100, 100, 100), start_pos, end_pos)
    for col in range(columns):
        start_pos = (col * cell_size[0], 0)
        end_pos = (col * cell_size[0], height)
        pygame.draw.line(screen, (100, 100, 100), start_pos, end_pos)
    for tetr in tetrominoes:
        draw_shape(tetr[0], tetr[1])
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            update_grid(tetrominoes[-1])
            move_shape_y(tetrominoes[-1], 1)
        elif event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                min_x = min(list(map(lambda coord: coord[0], tetrominoes[-1][0])))
                if min_x > 0:
                    update_grid(tetrominoes[-1])
                    move_shape_x(tetrominoes[-1], -1)
            elif event.key == pygame.K_RIGHT:
                max_x = max(list(map(lambda coord: coord[0], tetrominoes[-1][0])))
                if max_x < columns - 1:
                    update_grid(tetrominoes[-1])
                    move_shape_x(tetrominoes[-1], 1)
            elif event.key == pygame.K_UP:
                tetrominoes[-1] = (rotate_piece(tetrominoes[-1][0]), tetrominoes[-1][1])
                pygame.draw.rect(screen, (0, 0, 0), (0, cell_size[1], cell_size[0] * columns, cell_size[1] * rows), 0)
    for pos in tetrominoes[-1][0]:
        for tetromino in tetrominoes[0: -1]:
            for pos2 in tetromino[0]:
                if pos[1] == pos2[1] - 1 and pos[0] == pos2[0]:
                    new_tetromino = True
                    pass
    for tetromino in tetrominoes[0: -1]:
        for pos in tetrominoes[-1][0]:
            if pos in tetromino[0]:
                game_over = True
                pass
    clock.tick(frame_rate)
    if not new_tetromino:
        for pos in tetrominoes[-1][0]:
            x, y = pos
            if y >= rows - 1:
                new_tetromino = True
    else:
        for i in range(1, rows + 1):
            coord_data = list(map(lambda el: el[0], tetrominoes))
            count = 0
            for coord in coord_data:
                for c1 in coord:
                    if c1[1] == i:
                        count += 1
            if count == columns:
                score += 1
                for j in range(len(tetrominoes)):
                    k = 0
                    while k < len(tetrominoes[j][0]):
                        if tetrominoes[j][0][k][1] == i:
                            del tetrominoes[j][0][k]
                            k -= 1
                        elif tetrominoes[j][0][k][1] < i:
                            tetrominoes[1][0][k][1] += 1
                        k += 1
                pygame.draw.rect(screen, (0, 0, 0), (0, 0, cell_size[0] * columns, cell_size[1] * rows), 0)
                pygame.draw.rect(screen, (0, 0, 0), (width / columns * (columns - 1), 0, cell_size[0], cell_size[1]), 0)
                text_surface = my_font.render(str(score), False, (213, 219, 45))
                screen.blit(text_surface, (width / columns * (columns - 1), 0))
    if not game_over:
        pygame.display.update()
    else:
         print("GAME OVER")
         name123 = input("Введите")


connect = sqlite3.connect('Tetris123.db')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    name TEXT,
    score INTEGER
)""")

connect.commit()

cursor.execute("SELECT name FROM users")
cursor.execute('INSERT INTO users VALUES (?,?)',(name123, score))
connect.commit()
