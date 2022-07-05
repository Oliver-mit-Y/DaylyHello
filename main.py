import subprocess
from time import strftime
from tkinter import font
from turtle import bgcolor
from tkinter import *
import PIL.Image as Im
from PIL import ImageTk
import qrcode
from sys import platform
import os
from einträge import *
# set up some parameters
if not os.path.exists('./dmps'):
        os.mkdir('./dmps')
dumplocation = "./dmps/dumpfile.json"
x = 700
y = 850
dpbackground = 'lightgrey'
rootbackground = 'grey'
clockbackground = 'grey'
buttonbackground = 'darkgrey'
# create the most important objects
root = Tk()
mainframe = Frame(root)
dp_frame = Canvas(mainframe)
kartei_frame = Frame(mainframe)
option_frame = Frame(mainframe)
clockframe = Frame(option_frame)
eintragsliste = Eintraege(dump_location=dumplocation)
clocktime = Label(clockframe)
weekd = Label(clockframe)

if platform == 'win32':
    pypy = 'python'
else:
    pypy = 'python3'


# Funktion um alle items as einem Frame oder Canvas oder so was zu reinigen
def meister_proper(wid):
    wid_cont = wid.winfo_children()
    for wc in wid_cont:
        wc.destroy()


# Clear the dp frame before putting new stuff into it + set pressed button color
def create_dp_for_dp(n, btn_list, db):
    meister_proper(dp_frame)
    pressed_kartei(n, btn_list)
    dp = Frame(dp_frame, width=0,
                    height=0,
                    background=db
                    )
    dp.grid_propagate(True)
    return dp


def open_editor():
    subprocess.Popen([pypy, 'dumb_editor.py'])


def module_load():
    for ts in eintragsliste.dump:
        for m in ts:
            if m['api']:
                module = m['api_conf'].split('/')
                module = f'{module[-2]}/{module[-1]}'
                p = subprocess.Popen([pypy, f'./modules/{module}', m['id'], m['api_lnk']])
                p.wait()
    


# alle "show_frame_x"-Funktionen sind fuer die einzelnen Karteien zum umschalten des Contents
def show_frame_x(n, btn_list, typ):
    eintragsliste.reloaddump()
    dp = create_dp_for_dp(n, btn_list, rootbackground)
    content = eintragsliste.dump[typ]

    for en, tb in enumerate(content):
        ydist = 2
        tf = Frame(dp, background=dpbackground)
        tf.grid(column=0, row=en, pady=(0, 1), sticky=NE)
        tf.rowconfigure(0, weight=1)
        tf.rowconfigure(1, weight=1)
        txt = ent_to_str(tb)
        iye, ipa, ibig = tb['img']
        textbox = Text(tf, background=dpbackground, relief="flat")
        normal_bold = font.Font(family='Calibri', weight='bold', size=12)
        normal_normal = font.Font(family='Calibri', size=12)

        textbox.tag_configure('normal', font=normal_normal)
        textbox.tag_configure('headline', font=normal_bold)
        textbox.insert(1.0, txt)
        textbox.tag_add('headline', '1.0', '1.end')
        textbox.tag_add('normal', '2.0', END)
        textbox.configure(state=DISABLED, height=int(textbox.index('end').split('.')[0]), width=72)
        textbox.grid(column=0, row=0, sticky=NW)
        if iye or tb['qr']:
            img_frm = Frame(tf, background=dpbackground)
            img_frm.grid_columnconfigure(0, weight=1)
            img_frm.grid_rowconfigure(0, weight=1)
            img_frm.grid_rowconfigure(1, weight=1)
            img_frm.grid(column=1, row=0, sticky=E, ipady=ydist)
            if iye == 1:
                if ibig == 0:
                    try:
                        img = Im.open(ipa).convert('RGBA')
                        ix, iy = img.size
                        wish_size = 100
                        img = img.resize((wish_size, int(iy*(wish_size/ix))), Im.ANTIALIAS)
                        imgbg = Im.new('RGBA', img.size, dpbackground.upper())
                        imgbg.paste(img, mask=img)
                        imgbg = ImageTk.PhotoImage(imgbg)
                        il = Label(img_frm, image=imgbg)
                        il.configure(bd=0)
                        il.photo = imgbg
                        il.grid(column=0, row=0, padx=0, sticky=E, pady=0)
                    except Exception:
                        print('ImageError')
                else:
                    try:
                        img = Im.open(ipa).convert('RGBA')
                        ix, iy = img.size
                        wish_size = 200
                        img = img.resize((int(ix*(wish_size/iy)), wish_size), Im.ANTIALIAS)
                        imgbg = Im.new('RGBA', img.size, dpbackground.upper())
                        imgbg.paste(img, mask=img)
                        imgbg = ImageTk.PhotoImage(imgbg)
                        il = Label(tf, image=imgbg)
                        il.configure(bd=0)
                        il.photo = imgbg
                        il.grid(column=0, row=1, padx=0, sticky=W, pady=0)
                    except Exception:
                        print('ImageError')

            if tb['qr'] == 1:
                if iye == 1:
                    rowow = 1
                else:
                    rowow = 0
                wish_size = 85
                qr = qrcode.QRCode(border=0)
                qr.add_data(tb["qr_data"])
                qr.make()
                qr = qr.make_image()
                qx, qy = qr.size
                qr = qr.resize((wish_size, int(qy*(wish_size/qx))))
                qr = ImageTk.PhotoImage(qr)
                ql = Label(img_frm, image=qr)
                ql.qr = qr
                ql.grid(column=0, row=rowow, padx=0, sticky=E)
            img_frm.update()
            hfrm = img_frm.winfo_height()
            img_frm.grid_propagate(False)
            img_frm.configure(width=100, height=hfrm)

        tf.update()
        tfh = tf.winfo_height()
        tf.grid_propagate(False)
        tf.configure(width=684, height=tfh)

    dp.grid(column=0, row=0, padx=(5, 0), pady=(5, 5))


# funktion für den close button
def close(roo):
    roo.quit()


# update von allen items (unnütz weil man einfach root.update() machen kann)
def updateall(it):
    for i in it:
        i.update()


def pressed_kartei(n, btn_list):
    for btn in btn_list:
        if btn['name'] == n:
            btn['goto'].configure(background=dpbackground)
        else:
            btn['goto'].configure(background=buttonbackground)
        root.update()


def adding_test():
    eintragsliste.new_entry(eintragsliste.daylytea, title="new test entry", txt="omg i am way too great")
    eintragsliste.savedump()
    root.update()
    

def update_time():
    time = strftime('%d.%m.%Y\n%H:%M:%S')
    clocktime.configure(text=time)
    root.update()
    clocktime.after(1000, update_time)


def update_weekd():
    day = strftime('%a')
    weekd.configure(text=day)
    root.update()
    weekd.after(1000, update_weekd)


if __name__ == '__main__':

    # set the root up
    root.title('DaylyHello')
    root.geometry(f"{x}x{y}+20+20")
    root.configure(background=dpbackground)
    root.resizable(False, False)
    
    ladelabel = Label(root, text='bitte warten', background=dpbackground, bd=0, relief='flat', font=('Calibri 24'), width=100, height=1)
    ladelabel.place(relx=0.5, rely=0.5, anchor=CENTER)
    root.update()
    
    module_load()
    
    ladelabel.place_forget()
    root.configure(background=rootbackground)


    # mainframe grid configure
    mainframe.columnconfigure(0, weight=1)
    mainframe.columnconfigure(1, weight=1)

    # Grid important Frames
    kartei_frame.grid(column=0, row=0, sticky=N)
    dp_frame.grid(column=0, row=1, sticky=W)
    option_frame.grid(column=0, row=2, sticky=S, pady=0)
    mainframe.grid(column=0, row=0, sticky=NSEW)
    # set options for frames
    mainframe.configure(background=rootbackground)
    kartei_frame.configure(background=rootbackground)
    dp_frame.configure(background=dpbackground, highlightthickness=0)
    option_frame.configure(background=rootbackground)
    root.update()

    # option bar buttons
    add_btn = Button(option_frame, text='Add/Edit', width=0, command=lambda: open_editor(),
                     background=buttonbackground, borderwidth=0)
    close_btn = Button(option_frame, text='Close', width=0, command=lambda: close(root),
                       background=buttonbackground, borderwidth=0)

    clockframe.configure(background=clockbackground, width=0)

    clocktime.configure(text=strftime('%d.%m.%Y\n%H:%M:%S'), background=clockbackground, borderwidth=0,
                        font=('calibri', 12, 'bold'))
    weekd.configure(text=strftime('%a'), background=clockbackground, borderwidth=0,
                    font=('calibri', 29, 'bold'))

    clockframe.grid(column=1, row=0, ipady=0, pady=(1, 0), sticky=NSEW)
    weekd.grid(column=0, row=0, padx=20, sticky=W)
    clocktime.grid(column=2, row=0, padx=(100, 0), ipady=0, sticky=NSEW)

    add_btn.grid(column=0, row=0, ipady=15, pady=(1, 0), sticky=S)
    close_btn.grid(column=2, row=0, ipady=15, pady=(1, 0), sticky=S)

    update_time()
    update_weekd()

    root.update()

    add_btn_use = add_btn.winfo_width()/root.winfo_width()
    clockframe_use = clockframe.winfo_width()/root.winfo_width()
    close_btn_use = close_btn.winfo_width()/root.winfo_width()

    add_btn_wnt = 0.25-add_btn_use
    clockframe_wnt = 0.50-clockframe_use
    close_btn_wnt = 0.25-close_btn_use

    add_btn_range = add_btn_wnt*root.winfo_width()/2
    clockframe_range = clockframe_wnt*root.winfo_width()/2
    close_btn_range = close_btn_wnt*root.winfo_width()/2

    add_btn.grid(ipadx=add_btn_range)
    clockframe.grid(ipadx=clockframe_range)
    close_btn.grid(ipadx=close_btn_range)

    root.update()

    # Karteien
    dp_frame_height = (root.winfo_height() - (2 * option_frame.winfo_height()))
    dp_frame.configure(height=dp_frame_height, width=x)
    dp_frame.grid_propagate(False)
    karteien = [
        {'name': 'DaylyTea',
         'goto': Button(kartei_frame,
                        command=lambda: show_frame_x(karteien[0]['name'], karteien,
                                                     eintragsliste.daylytea))},
        {'name': 'Notes',
         'goto': Button(kartei_frame,
                        command=lambda: show_frame_x(karteien[1]['name'], karteien,
                                                     eintragsliste.notes))},
        {'name': 'Upcoming',
         'goto': Button(kartei_frame,
                        command=lambda: show_frame_x(karteien[2]['name'], karteien,
                                                     eintragsliste.upcoming))},
        {'name': 'Weather',
         'goto': Button(kartei_frame,
                        command=lambda: show_frame_x(karteien[3]['name'], karteien,
                                                     eintragsliste.weather))},
        {'name': 'Space',
         'goto': Button(kartei_frame,
                        command=lambda: show_frame_x(karteien[4]['name'], karteien,
                                                     eintragsliste.space))},
        {'name': 'Crypto',
         'goto': Button(kartei_frame,
                        command=lambda: show_frame_x(karteien[5]['name'], karteien,
                                                     eintragsliste.crypto))},
        {'name': 'Mails',
         'goto': Button(kartei_frame,
                        command=lambda: show_frame_x(karteien[6]['name'], karteien,
                                                     eintragsliste.mails))}
    ]

    # Configuriere Buttons für Karteien
    for c, k in enumerate(karteien):
        k['goto'].configure(text=k['name'], background=buttonbackground, borderwidth=1, relief='flat')
        k['goto'].grid(column=c, row=0, ipady=15, padx=1)
    root.update()

    for c, k in enumerate(karteien):
        k['goto'].grid(ipadx=(root.winfo_width() - kartei_frame.winfo_width()) / len(karteien * 2))


    show_frame_x(karteien[0]['name'], karteien, eintragsliste.daylytea)
    
    root.mainloop()
