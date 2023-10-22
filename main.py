import window
import render

WIDTH   = 480
HEIGHT  = 640
GameWindow = None

def init():
    print('Init')
    global GameWindow
    GameWindow =  window.Window(WIDTH, HEIGHT, 'Tetris')
    GameWindow.set_on_draw_listener(lambda: render.render())
    pass

def loop():

    print("Begin loop")
    global GameWindow
    while not GameWindow.should_close():
        GameWindow.draw()
    pass

def main():
    try:
        init()
        loop()
    except OSError as err:
        print("OS error:", err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    else:
        return
    

if __name__ == '__main__':
    main()