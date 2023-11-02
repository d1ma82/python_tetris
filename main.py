import traceback
import window
import gl_render
import tetris
import game_manager as gm

WIDTH   = 480
HEIGHT  = 640
GameWindow : window.GLFW
GL_render : gl_render.GL_Render

def init():

    print('Init')
    global GameWindow
    GameWindow =  window.GLFW((WIDTH, HEIGHT), 'Tetris')          # Note: run this before use Opengl
    global GL_render
    GL_render = gl_render.GL_Render((WIDTH, HEIGHT))
    GameWindow.set_render(GL_render)
    
    events = tetris.Events()
    events.on_ground = lambda _: print("On ground sound")
    events.on_left   = lambda _: print("On left sound")
    events.on_right  = lambda _: print("On right sound")
    events.on_rotate = lambda _: print("On rotate sounnd")
    events.on_delete = lambda _: print("On delete sound")
    events.on_close  = lambda _: GameWindow.close()

    gm.game = tetris.Tetris((WIDTH, HEIGHT), events)
    GameWindow.set_on_key_listener(gm.on_key)

    GL_render.attach_filterlist([gm.game])

def loop():

    print("Begin loop")
    global GameWindow
    while not GameWindow.should_close():
        GameWindow.draw()
    pass

def clear():
    pass

def main():
    try:
        init()
        loop()
        
    except OSError as err:
        print("OS error:", err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}\n{traceback.print_tb(err.__traceback__)}")
    finally:
        clear()
    

if __name__ == '__main__':
    main()