"""
                Tetris game
                Основная идея отрисовки, рисование в массиве, потом массив загрузить как текстуру
                и отобразить эту текстуру c помощью OpenGL

                Так же реализован один из примеров событийной модели общения между объектами
"""

import traceback
import window
import gl_render
import tetris
import game_manager as gm

WIDTH   = 240
HEIGHT  = 320
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
    events.on_ground    = lambda _: print("On ground sound")
    events.on_left      = lambda _: print("On left sound")
    events.on_right     = lambda _: print("On right sound")
    events.on_rotate    = lambda _: print("On rotate sounnd")
    events.on_delete    = lambda x: print(f"Delete {x} lines")
    events.on_game_over = lambda x: print(f"Game Over\nScore {x}")
    events.on_close     = lambda _: GameWindow.close()

    gm.game = tetris.Tetris((WIDTH, HEIGHT), events)
    GameWindow.set_event_listener(gm.window_events_listener)

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
        print(traceback.print_tb(err.__traceback__))
        print("OS error:", err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}\n{traceback.print_tb(err.__traceback__)}")
    finally:
        clear()
    

if __name__ == '__main__':
    main()