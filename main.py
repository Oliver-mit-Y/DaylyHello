import sys
import subprocess
import multiprocessing
from time import strftime, sleep
from tkinter import font, messagebox
from tkinter import *
import PIL.Image as Im
from PIL import ImageTk
import qrcode
import os
from einträge import *

# set up some parameters
if not os.path.exists('./dmps'):
        os.mkdir('./dmps')
        os.mkdir('./dmps/icons')

dumplocation = "./dmps/dumpfile.json"
x = 700
y = 860
dpbackground = 'lightgrey'
rootbackground = 'grey'
clockbackground = 'grey'
buttonbackground = 'darkgrey'
pressed_btn_color = '#cccccc'
pressed = 0
# create the most important objects
root = Tk()
mainframe = Frame(root)
dp_frame = Frame(mainframe)
kartei_frame = Frame(mainframe)
option_frame = Frame(mainframe)
clockframe = Frame(option_frame)
eintragsliste = Eintraege(dump_location=dumplocation)
clocktime = Label(clockframe)
weekd = Label(clockframe)
karteien = []
pictures = []
qr_codes = []

if sys.platform == 'win32':
    pypy = 'python'
else:
    pypy = 'python3'

# Funktion die ich aus dem Internet geklaut habe, um rgb Farben in TKinter zu nutzen
def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

# Funktion um alle items as einem Frame oder Canvas oder so was zu reinigen
def meister_proper(wid):
    wid_cont = wid.winfo_children()
    for wc in wid_cont:
        wc.destroy()


# Clear the dp frame before putting new stuff into it + set pressed button color
def create_dp_for_dp(n, db):
    meister_proper(dp_frame)
    pressed_kartei(n)
    dp = Canvas(dp_frame, width=root.winfo_width()-25,
                    height=dp_frame_height,
                    background=db,
                    highlightthickness=0)
    dp.grid_propagate(False)
    return dp


def open_editor():
    subprocess.Popen([pypy, 'dumb_editor.py'])


def module_load():
    for ts in eintragsliste.dump:
        for m in ts['entrys']:
            if m['api']:
                module = m['api_conf'].split('/')
                module = f'{module[-2]}/{module[-1]}'
                p = subprocess.Popen([pypy, f'./modules/{module}', m['id'], m['api_lnk']])
                p.wait()
    

def picture_load():
    global pictures
    pictures = []
    img = Im.open('./resources/image_load_error.png').convert('RGBA')
    ix, iy = img.size
    wish_size = 100
    img = img.resize((wish_size, int(iy*(wish_size/ix))), Im.ANTIALIAS)
    imgbg = Im.new('RGBA', img.size, dpbackground.upper())
    imgbg.paste(img, mask=img)
    imgbg = ImageTk.PhotoImage(imgbg)
    pictures.append({'id': 'no_id', 'img': imgbg, 'big': 0})

    for tt in eintragsliste.dump:
        for ee in tt['entrys']:
            if ee['img'][0]:
                if not ee['img'][2]:
                    img = Im.open(ee['img'][1]).convert('RGBA')
                    ix, iy = img.size
                    wish_size = 100
                    img = img.resize((wish_size, int(iy*(wish_size/ix))), Im.ANTIALIAS)
                    imgbg = Im.new('RGBA', img.size, dpbackground.upper())
                    imgbg.paste(img, mask=img)
                    imgbg = ImageTk.PhotoImage(imgbg)
                else:
                    img = Im.open(ee['img'][1]).convert('RGBA')
                    ix, iy = img.size
                    wish_size = 200
                    img = img.resize((int(ix*(wish_size/iy)), wish_size), Im.ANTIALIAS)
                    imgbg = Im.new('RGBA', img.size, dpbackground.upper())
                    imgbg.paste(img, mask=img)
                    imgbg = ImageTk.PhotoImage(imgbg)
                pictures.append({'id': ee['id'], 'img': imgbg, 'big': ee['img'][2]})


def qr_load():
    global qr_codes
    qr_codes = []
    for tt in eintragsliste.dump:
        for ee in tt['entrys']:
            if ee['qr']:
                wish_size = 85
                qr = qrcode.QRCode(border=0)
                qr.add_data(ee["qr_data"])
                qr.make()
                qr = qr.make_image()
                qx, qy = qr.size
                qr = qr.resize((wish_size, int(qy*(wish_size/qx))))
                qr = ImageTk.PhotoImage(qr)
                qr_codes.append({'id': ee['id'], 'qr': qr})


# alle "show_frame_x"-Funktionen sind fuer die einzelnen Karteien zum umschalten des Contents
def show_frame_x(n, typ):
    eintragsliste.reloaddump()
    parent_dp = create_dp_for_dp(n, 'lightgrey')
    dp = Frame(parent_dp, background=rootbackground)
    scroll = Scrollbar(dp_frame, orient=VERTICAL, command=parent_dp.yview, width=13)

    content = eintragsliste.dump[typ]['entrys']

    for en, tb in enumerate(content):
        tf = Frame(dp, background=dpbackground)
        ydist = 2
        backslash_n = 0
        for ch in tb['txt']:
            if ch == "\n":
                backslash_n += 1
        tb_width = 70
        tb_height = (len(tb['txt'])-backslash_n)/tb_width+backslash_n+1.5
        
        if tb_height >= 20:
            tb_height = 20
        
        iye, ipa, ibig = tb['img']

        textbox_frame = Frame(tf)
        headline_textbox = Text(textbox_frame, background=dpbackground, relief="flat")
        textbox = Text(textbox_frame, background=dpbackground, relief="flat")

        normal_bold = font.Font(family='Calibri', weight='bold', size=12)
        normal_normal = font.Font(family='Calibri', size=12)

        headline_textbox.tag_configure('headline', font=normal_bold)
        textbox.tag_configure('normal', font=normal_normal)

        headline_textbox.insert(1.0, tb['title'])
        textbox.insert(1.0, tb['txt'])

        headline_textbox.tag_add('headline', '1.0', '1.end')
        textbox.tag_add('normal', '1.0', END)

        headline_textbox.configure(state=DISABLED, height=1.5, width=tb_width, wrap='word')
        textbox.configure(state=DISABLED, height=tb_height, width=tb_width, wrap='word')

        textbox_frame.grid_rowconfigure(0, weight=1)
        textbox_frame.grid_rowconfigure(1, weight=1)
        textbox_frame.grid_columnconfigure(1, weight=1)

        headline_textbox.grid(row=0, column=0, sticky=EW)
        textbox.grid(row=1, column=0, sticky=EW)

        textbox_frame.grid(row=0, column=0, sticky=NW)
        if iye or tb['qr']:
            img_frm = Frame(tf, background=dpbackground)
            
            if iye:
                img_part = 0
                for n, p in enumerate(pictures):
                    if p['id'] == tb['id']:
                        img_part = n
                        break
                if not ibig:
                    try:
                        imgbg = pictures[img_part]['img']
                        il = Label(img_frm, image=imgbg)
                        il.configure(bd=0)
                        il.photo = imgbg
                        il.grid(column=0, row=0, padx=0, sticky=E, pady=0)
                    except Exception:
                        print('ImageError')
                else:
                    try:
                        imgbg = pictures[img_part]['img']
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
                qr_part = 0
                for n, p in enumerate(qr_codes):
                    if p['id'] == tb['id']:
                        qr_part = n
                        break
                qr = qr_codes[qr_part]['qr']
                ql = Label(img_frm, image=qr)
                ql.qr = qr
                ql.grid(column=0, row=rowow, padx=0, sticky=NE)

            img_frm.grid_propagate(True)
            img_frm.grid_columnconfigure(0, weight=1)
            img_frm.grid_rowconfigure(0, weight=1)
            img_frm.grid_rowconfigure(1, weight=1)
            img_frm.grid(column=1, row=0, sticky=NSEW, ipady=ydist)
        root.update()
        tf.grid_rowconfigure(0, weight=1)
        tf.grid_rowconfigure(1, weight=1)
        tf.grid_columnconfigure(0, weight=1)
        tf.grid_columnconfigure(1, weight=1)

        tf.grid(column=0, row=en, pady=(0, 1), sticky=NSEW)

    dp_frame.grid_columnconfigure(0, weight=1)
    dp_frame.grid_columnconfigure(1, weight=1)
    dp_frame.grid_rowconfigure(0, weight=1)

    dp.grid_columnconfigure(0, weight=1)

    parent_dp.create_window(0, 0, anchor=NW, window=dp)
    parent_dp.update_idletasks()

    parent_dp.configure(scrollregion=parent_dp.bbox('all'), yscrollcommand=scroll.set)

    parent_dp.grid(column=0, row=0, padx=(5, 0), pady=(5, 5))
    scroll.grid(row=0, column=1, sticky=NS)    


# funktion für den close button
def close(roo):
    roo.quit()


# update von allen items (unnütz weil man einfach root.update() machen kann)
def updateall(it):
    for i in it:
        i.update()


def pressed_kartei(n):
    global pressed
    for btn in karteien:
        if btn['typ'] == n:
            btn['goto'].configure(background=pressed_btn_color, image=btn['p_image'])
            pressed = btn['typ']
        else:
            btn['goto'].configure(background=buttonbackground, image=btn['image'])
        
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


def reload():
    module_load()
    picture_load()
    qr_load()

    na = ""
    for k in karteien:
        if k['typ'] == pressed:
            na = k['typ']

    show_frame_x(na, pressed)


def kartei_length_check(kartlist=None):
    msg_title = 'Neustart erforderlich'
    if kartlist:
        length = len(kartei_frame.winfo_children())
        eintragsliste.reloaddump()
        if len(eintragsliste.dump) != length:
            messagebox.showinfo(message='Änderung an Karteilänge wurde Festgestellt\nProgramm wird neugestartet um Änderungen zu übernehmen', title=msg_title)
            sys.stdout.flush()
            os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
        for nn, c in enumerate(eintragsliste.dump):
            if c['name'] != kartlist[nn]['name']:
                messagebox.showinfo(message='Änderung an Karteinamen wurde Festgestellt\nProgramm wird neugestartet um Änderungen zu übernehmen', title=msg_title)
                sys.stdout.flush()
                os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
        clocktime.after(1000, lambda: kartei_length_check(kartlist=kartlist))
    else:
        length = len(kartei_frame.winfo_children())
        eintragsliste.reloaddump()
        if len(eintragsliste.dump) != length:
            messagebox.showinfo(message='Änderung an Karteilänge wurde Festgestellt\nProgramm wird neugestartet um Änderungen zu übernehmen', title=msg_title)
            sys.stdout.flush()
            os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
        clocktime.after(1000, lambda: kartei_length_check())


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
    picture_load()
    qr_load()
    
    ladelabel.place_forget()
    root.configure(background=rootbackground)


    # mainframe grid configure
    mainframe.grid_columnconfigure(0, weight=1)
    mainframe.grid_rowconfigure(0, weight=1)
    mainframe.grid_rowconfigure(1, weight=1)
    mainframe.grid_rowconfigure(2, weight=1)

    # Grid important Frames
    kartei_frame.grid(column=0, row=0, sticky=EW)
    dp_frame.grid(column=0, row=1, sticky=NSEW, pady=0, ipady=0)
    option_frame.grid(column=0, row=2, sticky=EW, pady=0)
    mainframe.grid(column=0, row=0, sticky=NSEW)
    # set options for frames
    mainframe.configure(background=rootbackground)
    kartei_frame.configure(background=rootbackground)
    dp_frame.configure(background=dpbackground)
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
    clocktime.grid(column=1, row=0, padx=(100, 0), ipady=0, sticky=NSEW)

    add_btn.grid(column=0, row=0, ipady=15, pady=(1, 0), sticky=EW)
    close_btn.grid(column=2, row=0, ipady=15, pady=(1, 0), sticky=EW)

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
    
    dp_frame.grid_propagate(False)
    for n, cards in enumerate(eintragsliste.dump):
        card = {'name': cards['name'], 
                'goto': Button(kartei_frame,
                               command=lambda c=n, nn=n: show_frame_x(c, nn)),
                'typ': n,
                'icn': cards['icon'],
                'image':None,
                'p_image':None}
        karteien.append(card)


    # Configuriere Buttons für Karteien
    for c, k in enumerate(karteien):
        if k['icn'][0]:
            try:
                img = Im.open(k['icn'][1]).convert('RGBA')
                ix, iy = img.size
                wish_size = 30
                img = img.resize((int(ix*(wish_size/iy)), wish_size), Im.ANTIALIAS)
                imgbg = Im.new('RGBA', img.size, buttonbackground.upper())
                imgbg.paste(img, mask=img)
                imgbg = ImageTk.PhotoImage(imgbg)

                k['goto'].configure(image=imgbg, compound=LEFT)
                k['goto'].image = imgbg
                k['image'] = imgbg

                img = Im.open(k['icn'][1]).convert('RGBA')
                ix, iy = img.size
                wish_size = 30
                img = img.resize((int(ix*(wish_size/iy)), wish_size), Im.ANTIALIAS)
                pressed_img = Im.new('RGBA', img.size, pressed_btn_color.upper())
                pressed_img.paste(img, mask=img)
                pressed_img = ImageTk.PhotoImage(pressed_img)
                k['goto'].i_pressed = pressed_img
                k['p_image'] = pressed_img

            except Exception:
                print('ImageError')
                img = Im.open('./resources/image_load_error.png').convert('RGBA')
                ix, iy = img.size
                wish_size = 30
                img = img.resize((int(ix*(wish_size/iy)), wish_size), Im.ANTIALIAS)
                imgbg = Im.new('RGBA', img.size, buttonbackground.upper())
                imgbg.paste(img, mask=img)
                imgbg = ImageTk.PhotoImage(imgbg)
                k['goto'].configure(image=imgbg, compound=LEFT)
                k['goto'].image = imgbg

        k['goto'].configure(text=k['name'], background=buttonbackground, borderwidth=1, relief='flat')
        kartei_frame.grid_columnconfigure(c, weight=1)
        k['goto'].grid(column=c, row=0, ipady=15, padx=1, sticky=NSEW)

    # add reload button
    reload_btn = Button(option_frame, text='r', width=1, height=1, command=lambda:reload(), background=buttonbackground)
    reload_btn.grid(row=0, column=1, sticky=SE)
    root.update()
    dp_frame_height = (root.winfo_height() - kartei_frame.winfo_height() - option_frame.winfo_height())
    dp_frame.configure(height=dp_frame_height, width=x)

    show_frame_x(karteien[0]['typ'], 0)
    
    kartei_length_check(karteien)

    root.mainloop()
