import lab3.assertions as assertions
from random import random
import tkinter as tk
from collections import Iterable


def read_data() -> tuple:
    with open("data.txt", "r") as file:
        canvas_size = tuple(map(float, file.readline().split()))
        assertions.size(canvas_size, 2)
        assertions.all_positive(canvas_size)
        rectangles = []
        row_number = 1
        for row in file:
            rectangle_points = tuple(map(float, row.split()))
            assertions.size(rectangle_points, 4)
            assertions.all_positive(rectangle_points)
            x1, y1, x2, y2 = rectangle_points
            width, height = canvas_size
            if x1 >= width or x2 >= width or y1 >= height or y2 >= height:
                raise ValueError("Line %d: Rectangle doesn't fit canvas" % row_number)
            rectangles.append(rectangle_points)
            row_number += 1
        return canvas_size, rectangles


def get_random_float(left: float = 0.0, right: float = 1.0) -> float:
    return random() * (right - left) + left


def generate_rectangle(left_top_node: tuple = None) -> tuple:
    points = None
    while True:
        if points is not None:
            left_top_node = yield tuple(points)
        border_box = [(0, 0), canvas_size]
        if left_top_node is not None:
            border_box[0] = left_top_node
        else:
            if len(rectangles_list) >= 3:
                if rectangles_box:
                    border_box = rectangles_box
        points = []
        for _ in range(2 if left_top_node is None else 1):
            for i in range(2):
                points.append(get_random_float(border_box[0][i], border_box[1][i]))
        if left_top_node is not None:
            points = list(left_top_node) + points
        for i in range(2):
            if points[i+2] < points[i]:
                points[i], points[i+2] = points[i+2], points[i]


def update_rectangles_box(rectangles: list) -> tuple:
    global rectangles_box
    if len(rectangles):
        if rectangles_box:
            x_min, y_min = rectangles_box[0]
            x_max, y_max = rectangles_box[1]
        else:
            x_min, y_min = canvas_size
            x_max, y_max = 0, 0
        for rect in rectangles:
            for i in (0, 2):
                if rect[i] < x_min:
                    x_min = rect[i]
                if rect[i] > x_max:
                    x_max = rect[i]
                if rect[i+1] < y_min:
                    y_min = rect[i+1]
                if rect[i+1] > y_max:
                    y_max = rect[i+1]
        rectangles_box = (x_min, y_min), (x_max, y_max)


def fill_rect(rect: Iterable, color: str = 'black') -> None:
    canvas.create_rectangle(rect, width=1, fill=color)


def draw_rect(rect: Iterable, special: bool = False) -> None:
    if special:
        canvas.create_rectangle(rect, width=2, outline="blue")
    else:
        canvas.create_rectangle(rect, width=1, outline=FILL_COLORS[color_index])


def draw_border_box() -> None:
    global canvas, border_index, rectangles_box
    if border_index:
        canvas.delete(border_index)
    if rectangles_box:
        border_index = canvas.create_rectangle(rectangles_box[0], rectangles_box[1], width=2, dash=(10, 10),
                                               tags="border", outline="red")
    else:
        border_index = 0


def create_new_rect(left_top: tuple = None, special: bool = False) -> None:
    # global rectangle_generator
    if left_top is not None:
        rect = rectangle_generator.send(left_top)
    else:
        rect = next(rectangle_generator)
    rectangles_list.append(rect)
    draw_rect(rect, special)
    update_rectangles_box([rect])
    draw_border_box()


def fill_hlines(area, color: str = 'black') -> None:
    global canvas
    for y in range(int(area[1] + 1), int(area[3]), 8):
        canvas.create_line([area[0], y, area[2], y], fill=color, width=4)


def fill_vlines(area, color: str = 'black') -> None:
    global canvas
    for x in range(int(area[0] + 1), int(area[2]), 8):
        canvas.create_line([x, area[1], x, area[3]], fill=color, width=4)


def get_intersection(x: int, y: int) -> tuple:
    area = [0, 0, canvas_size[0], canvas_size[1]]
    n_intersects = 0
    for rect in rectangles_list:
        if rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]:
            n_intersects += 1
            for i in range(2):
                if area[i] < rect[i]:
                    area[i] = rect[i]
                if area[i+2] > rect[i+2]:
                    area[i+2] = rect[i+2]
    return area if n_intersects > 0 else None


def fill(x: int, y: int, color: str = 'black', mode: str = 'solid') -> None:
    area = get_intersection(x, y)
    if area is not None:
        if mode == 'solid':
            fill_rect(area, color=color)
        elif mode == 'hline':
            fill_hlines(area, color=color)
        elif mode == 'vline':
            fill_vlines(area, color=color)
        else:
            print("%s fill mode is invalid")


def clear() -> None:
    global canvas, rectangles_list, rectangles_box, border_index
    canvas.delete("all")
    rectangles_list = []
    rectangles_box = None
    border_index = 0


def on_left_mouse_click(event) -> None:
    create_new_rect()


def on_left_mouse_double_click(event) -> None:
    create_new_rect((event.x, event.y), True)


def on_right_mouse_click(event) -> None:
    fill(event.x, event.y, mode=FILL_MODES[fill_mode_index], color=FILL_COLORS[color_index])


def on_key_backspace(event) -> None:
    clear()


def on_change_fill_mode(event) -> None:
    global FILL_MODES, fill_mode_index, fill_mode_button
    fill_mode_index += 1
    if fill_mode_index >= len(FILL_MODES):
        fill_mode_index = 0
    fill_mode_button["text"] = FILL_MODES[fill_mode_index]


def on_change_color(event) -> None:
    global FILL_COLORS, color_index, color_button
    color_index += 1
    if color_index >= len(FILL_COLORS):
        color_index = 0
    color_button["bg"] = FILL_COLORS[color_index]



canvas_size, rectangles_list = read_data()
rectangles_box = None
update_rectangles_box(rectangles_list)
border_index = 0
rectangle_generator = generate_rectangle()
next(rectangle_generator)

FILL_MODES = ["solid", "hline", "vline"]
fill_mode_index = 0

FILL_COLORS = ["black", "blue", "red", "green", "gray", "cyan", "magenta", "brown"]
color_index = 0

root = tk.Tk()
canvas = tk.Canvas(root, height=canvas_size[1], width=canvas_size[0], bg="white")
canvas.tag_raise("border")
for rectangle in rectangles_list:
    draw_rect(rectangle)
draw_border_box()
canvas.pack(side=tk.LEFT)
canvas.bind("<Button-2>", on_left_mouse_double_click)
canvas.bind("<Button-1>", on_left_mouse_click)
canvas.bind("<Button-3>", on_right_mouse_click)
root.bind("<Key-BackSpace>", on_key_backspace)

fill_mode_button = tk.Button(text=FILL_MODES[0])
fill_mode_button.bind("<Button-1>", on_change_fill_mode)
fill_mode_button.pack(side=tk.LEFT)

color_button = tk.Button(bg=FILL_COLORS[color_index])
color_button.bind("<Button-1>", on_change_color)
color_button.pack(side=tk.LEFT)
root.mainloop()