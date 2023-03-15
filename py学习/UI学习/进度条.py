# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-03-15 15:44:53
LastEditTime : 2023-03-15 15:45:06
FilePath     : /CODE/py学习/UI学习/进度条.py
Github       : https://github.com/sandorn/home
==============================================================
'''


def progress_bar():
    from progress.bar import Bar
    import time

    bar = Bar('Processing', max=20)
    for _ in range(100):
        time.sleep(0.01)
        bar.next()

    bar.finish()


def tqdm():
    import time
    from tqdm import tqdm
    for _ in tqdm(list(range(100))):
        time.sleep(0.01)


def alive_progress():
    from alive_progress import alive_bar
    import time
    mylist = list(range(100))
    with alive_bar(len(mylist)) as bar:
        for _ in mylist:
            bar()
            time.sleep(0.01)


def guipro():
    import PySimpleGUI as sg
    import time
    mylist = list(range(1000))
    for i, item in enumerate(mylist):
        sg.one_line_progress_meter('This is my progress meter!', i + 1, len(mylist), ' -key-')
        time.sleep(0.01)


def guipross():
    '''有错误'''
    import PySimpleGUI as sg
    import time
    mylist = list(range(20))
    progressbar = [[sg.ProgressBar(len(mylist), orientation='horizontal', size=(51, 10), key='progressbar')]]
    outputwin = [[sg.Output(size=(78, 20))]]
    layout = [[sg.Frame('Progress', layout=progressbar)], [sg.Frame('Output', layout=outputwin)], [sg.Submit('Start'), sg.Cancel()]]
    window = sg.Window('Custom Progress Meter', layout)
    progress_bar = window[progressbar]
    while True:
        event, values = window.read(timeout=10)
        if event == 'Cancel' or event is None:
            break
        elif event == 'Start':
            for i, item in enumerate(mylist):
                print(item)
                time.sleep(1)
                progress_bar.UpdateBar(i + 1)
    window.close()


def window():
    import PySimpleGUI as sg  # Part 1 - The import
    # Define the window's contents
    layout = [
        [sg.Text("What's your name?")],  # Part 2 - The Layout
        [sg.Input()],
        [sg.Button('Ok')]
    ]
    # Create the window
    window = sg.Window('Window Title', layout)  # Part 3 - Window Defintion
    # Display and interact with the Window
    event, values = window.read()  # Part 4 - Event loop or Window.read call
    # Do something with the information gathered
    print('Hello', values[0], "! Thanks for trying PySimpleGUI")
    # Finish up by removing from the screen
    window.close()


if __name__ == "__main__":
    # progress_bar()
    # tqdm()
    # alive_progress()
    # guipro()
    # guipross()
    # window()
