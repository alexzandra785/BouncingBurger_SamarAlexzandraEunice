from tkinter import *
import random
from PIL import Image, ImageTk

# Setup
tk = Tk()
tk.title('Samar - Bouncing Ball')
tk.resizable(False, False)
WIDTH, HEIGHT = 800, 600
canvas = Canvas(tk, width=WIDTH, height=HEIGHT)
canvas.pack()

# 1. Load and display background using forward slashes to avoid unicode errors
bg = Image.open("C:/Users/Admin/Desktop/myproj/background.png")
bg = bg.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
bg_tk = ImageTk.PhotoImage(bg)
canvas.create_image(0, 0, image=bg_tk, anchor=NW)
canvas.bg = bg_tk  # keep reference

# 2. Load ball image
ball_img = Image.open("C:\\Users\\Admin\\Desktop\\myproj\\ball.png")
ball_img = ball_img.resize((90, 90), Image.ANTIALIAS)
ball_tk = ImageTk.PhotoImage(ball_img)
ball = canvas.create_image(10, 10, image=ball_tk, anchor=NW)
canvas.ball_ref = ball_tk  # keep reference

# Already resized version
orig_ball = Image.open("C:/Users/Admin/Desktop/myproj/ball.png") \
                 .resize((90, 90), Image.ANTIALIAS) \
                 .convert("RGBA")
ball_tk = ImageTk.PhotoImage(orig_ball)
ball = canvas.create_image(10, 10, image=ball_tk, anchor=NW)
canvas.ball_ref = ball_tk


# Label
label = canvas.create_text(10, 10, text="SAMAR", fill="black", font=("Arial", 12, "bold"))

# Movement settings
xspeed = yspeed = 3
running = True

def random_color():
    return random.choice(['red', 'orange', 'yellow', 'green', 'blue', 'violet'])

from PIL import Image, ImageColor

tint_cache = {}

def tint_image(image, tint_color, alpha=120):
    overlay = Image.new("RGBA", image.size, tint_color + (alpha,))
    return Image.alpha_composite(image, overlay)

def get_tinted(color_name):
    if color_name not in tint_cache:
        rgb = ImageColor.getrgb(color_name)  # converts "red" → (255, 0, 0)
        tinted = tint_image(orig_ball, rgb)
        tint_cache[color_name] = ImageTk.PhotoImage(tinted)
    return tint_cache[color_name]


def moveBall():
    global xspeed, yspeed
    if running:
        canvas.move(ball, xspeed, yspeed)
        left, top, right, bottom = canvas.bbox(ball)
        cx, cy = (left+right)/2, (top+bottom)/2
        canvas.coords(label, cx, cy)

        hit = False
        if left <= 0 or right >= WIDTH:
            xspeed = -xspeed; hit = True
        if top <= 0 or bottom >= HEIGHT:
            yspeed = -yspeed; hit = True

        if hit:
            color = random_color()
            canvas.itemconfig(label, fill=color)
            new_tk = get_tinted(color)
            canvas.itemconfig(ball, image=new_tk)
            canvas.ball_ref = new_tk

    canvas.after(10, moveBall)


def toggle_pause(event=None):
    global running
    running = not running

# Bind space to pause/resume
tk.bind('<space>', toggle_pause)

# Start animation
canvas.after(10, moveBall)
tk.mainloop()


