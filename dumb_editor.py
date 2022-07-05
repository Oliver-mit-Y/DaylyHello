import shutil
from einträge import *
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

x = 700
y = 500
dumblocation = "./dmps/dumpfile.json"

eintragliste = Eintraege(dumblocation)
root = Tk()
root.title('Eintrags Editor')
mainframe = Frame(root)
selection_frame = Frame(mainframe)
type_selector_frame = Frame(mainframe)
back = str('Notes')
backtyp = 0
ed_ent = {'typ': Eintraege.daylytea, 'n': 0}
karteien = []


def meister_proper(wid):
    wid_cont = wid.winfo_children()
    for wc in wid_cont:
        wc.destroy()


def str_cleanup(s):
    while s[-1:] == "\n":
        s = s[:-1]
    return s

# Clear the dp frame before putting new stuff into it + set pressed button color
def create_dp_for_dp(n, btn_list, db):
    meister_proper(selection_frame)
    pressed_kartei(n, btn_list)
    dp = Frame(selection_frame, width=0,
                    height=0,
                    background=db
                    )
    dp.grid_propagate(True)
    return dp


def create_entry(typ, m, btn_list, height):
    eintragliste.new_entry(typ)
    eintragliste.savedump()
    show_frame_x(m, btn_list, height, typ)


def show_frame_x(m=None, btn_list=None, height=None, typ=None, dp=None):
    if not dp:
        dp = create_dp_for_dp([m, typ], btn_list, 'lightgrey')

        if typ is not None:
            for n, d in enumerate(eintragliste.dump[typ]):
                part = [d['id'], Button(dp, text=d['title'])]
                part[1].configure(command=lambda p=part[0]:
                                  show_frame_x(dp=editor_frame(eintragliste.dmp_by_id(p))))
                part[1].grid(row=n, column=0, sticky=W)
            plus_btn = Button(dp, text="+", command=lambda: create_entry(typ, m, btn_list, height))
            plus_btn.grid(row=0, column=1, padx=10)
        if typ is None:
            print("kys little piece of shit")

    dp.grid(column=0, row=0, padx=(5, 0), pady=(5, 5))


def file_btn_fnc(ent_wdg):
    pth = askopenfilename(title='selcet image', filetypes=(('any', '.*'),), initialdir='./')
    ent_wdg.delete(0, END)
    ent_wdg.insert(0, string=pth)


def bck_btn_fnc():
    show_frame_x(back, karteien,
                 selection_frame.winfo_height(), typ=backtyp)


# frame to edit one specific Entry
def editor_frame(d):
    dp = Frame(selection_frame, width=selection_frame.winfo_width()-10, height=root.winfo_height(),
                    background='lightgrey')
    dp.grid_propagate(False)
    optionlist = [{'name': 'Standard', 'frame': Frame(), 'children': []},
                  {'name': 'API', 'frame': Frame(), 'children': []},
                  {'name': 'Images', 'frame': Frame(), 'children': []},
                  {'name': 'controll', 'frame': Frame(), 'children': []},
                  d['id']]
    for en, opt in enumerate(optionlist):
        if en != 4:
            optframe = Frame(dp)
            optframe.configure(background='grey', relief='flat', borderwidth=1)
            optframe.grid(column=0, row=en, pady=1, ipadx=5, padx=5)
            optionlist[en]['frame'] = optframe
    title_lbl = Label(optionlist[0]['frame'])
    title_lbl.configure(text='Titel', background='darkgrey')
    title_lbl.grid(column=0, row=0, ipadx=4, pady=5, sticky=NW, padx=5)
    title_ent = Entry(optionlist[0]['frame'])
    title_ent.configure(background='darkgrey')
    title_ent.insert(0, d['title'])
    title_ent.grid(column=0, row=1, sticky=NW, pady=5, padx=5)
    optionlist[0]['children'].append(title_ent)

    txt_lbl = Label(optionlist[0]['frame'])
    txt_lbl.configure(text='text eingeben', background='darkgrey')
    txt_lbl.grid(column=1, row=0, sticky=NW, pady=5, padx=5)
    txt_txt = Text(optionlist[0]['frame'])
    txt_txt.configure(height=5, width=51, background='darkgrey', wrap=WORD)
    txt_txt.insert('1.0', d['txt'])
    txt_txt.grid(column=1, row=1, sticky=NW, pady=(5, 5), padx=5)
    optionlist[0]['children'].append(txt_txt)

    optionlist[0]['frame'].update()
    height_zero = optionlist[0]['frame'].winfo_height()
    optionlist[0]['frame'].grid_propagate(False)
    optionlist[0]['frame'].configure(width=mainframe.winfo_width() - 130, height=height_zero)

    api_vl = IntVar()
    api_vl.set(d['api'])
    api_chck = Checkbutton(optionlist[1]['frame'], variable=api_vl)
    api_chck.configure(text='API', background='darkgrey')
    api_chck.grid(column=0, row=0, sticky=NW, pady=5, padx=2)
    optionlist[1]['children'].append(api_vl)

    api_cnf_lbl = Label(optionlist[1]['frame'])
    api_cnf_lbl.configure(text='Module File', background='darkgrey')
    api_cnf_lbl.grid(column=0, row=1, sticky=NW, pady=5, padx=2)
    api_path_frm = Frame(optionlist[1]['frame'])
    api_path_frm.configure(background='darkgrey')
    api_path_frm.grid(row=1, column=1, pady=5, padx=2, sticky=NW)
    api_path_ent = Entry(api_path_frm)
    api_path_ent.configure(background='darkgrey')
    api_path_ent.insert(0, d["api_conf"])
    api_path_ent.grid(row=0, column=0, sticky=NS)
    api_path_btn = Button(api_path_frm)
    api_path_btn.configure(text='F', width=1, background='darkgrey', command=lambda: file_btn_fnc(api_path_ent))
    api_path_btn.grid(row=0, column=1, sticky=NW)
    optionlist[1]['children'].append(api_path_ent)

    api_lnk_lbl = Label(optionlist[1]['frame'])
    api_lnk_lbl.configure(text='API Link', background='darkgrey')
    api_lnk_lbl.grid(column=0, row=2, sticky=NW, pady=5, padx=2)
    api_lnk_ent = Entry(optionlist[1]['frame'])
    api_lnk_ent.configure(width=60, background='darkgrey')
    api_lnk_ent.insert(0, d['api_lnk'])
    api_lnk_ent.grid(column=1, row=2, sticky=NW, pady=5, padx=2)
    optionlist[1]['children'].append(api_lnk_ent)

    optionlist[1]['frame'].update()
    height_one = optionlist[1]['frame'].winfo_height()
    optionlist[1]['frame'].grid_propagate(False)
    optionlist[1]['frame'].configure(width=mainframe.winfo_width()-130, height=height_one)

    ii, im, ib = d['img']
    img_vl = IntVar()
    img_vl.set(ii)
    img_big_vl = IntVar()
    img_big_vl.set(ib)
    img_yes_no = Checkbutton(optionlist[2]['frame'], variable=img_vl)
    img_yes_no.configure(text='Image', background='darkgrey')
    img_yes_no.grid(row=0, column=0, pady=5, padx=2, sticky=NW)
    optionlist[2]['children'].append(img_vl)
    img_big_yes_no = Checkbutton(optionlist[2]['frame'], variable=img_big_vl)
    img_big_yes_no.configure(text='Big', background='darkgrey')
    img_big_yes_no.grid(row=0, column=1, pady=5, padx=2, sticky=NW)
    optionlist[2]['children'].append(img_big_vl)

    img_path_lbl = Label(optionlist[2]['frame'])
    img_path_lbl.configure(text='Path to Imgae', background='darkgrey')
    img_path_lbl.grid(row=1, column=0, pady=5, padx=2, sticky=NW)
    img_path_frm = Frame(optionlist[2]['frame'])
    img_path_frm.configure(background='darkgrey')
    img_path_frm.grid(row=1, column=1, pady=5, padx=2, sticky=NW)
    img_path_ent = Entry(img_path_frm)
    img_path_ent.configure(background='darkgrey')
    img_path_ent.insert(0, im)
    img_path_ent.grid(row=0, column=0, sticky=NS)
    img_path_btn = Button(img_path_frm)
    img_path_btn.configure(text='F', width=1, background='darkgrey', command=lambda: file_btn_fnc(img_path_ent))
    img_path_btn.grid(row=0, column=1, sticky=NW)
    optionlist[2]['children'].append(img_path_ent)

    qr_vl = IntVar()
    qr_vl.set(d['qr'])
    qr_yes_no = Checkbutton(optionlist[2]['frame'], variable=qr_vl)
    qr_yes_no.configure(text='QR', background='darkgrey')
    qr_yes_no.grid(row=2, column=0, pady=5, padx=2, sticky=NW)
    optionlist[2]['children'].append(qr_vl)

    qr_data_ent = Text(optionlist[2]['frame'])
    qr_data_ent.configure(background='darkgrey', width=50, height=4)
    qr_data_ent.insert('1.0', d['qr_data'])
    qr_data_ent.grid(row=2, column=1, pady=5, padx=2, sticky=NW)
    optionlist[2]['children'].append(qr_data_ent)

    optionlist[2]['frame'].update()
    height_two = optionlist[2]['frame'].winfo_height()
    optionlist[2]['frame'].grid_propagate(False)
    optionlist[2]['frame'].configure(width=mainframe.winfo_width() - 130, height=height_two)

    optionlist[3]['frame'].configure(background='black')

    back_button = Button(optionlist[3]['frame'])
    back_button.configure(background='darkgrey', text='Back', font=('calibri', 12), command=lambda: bck_btn_fnc())

    del_button = Button(optionlist[3]['frame'])
    del_button.configure(background='darkgrey', text='delete', font=('calibri', 12), command=lambda: del_btn_fnc(d))
    
    apply_button = Button(optionlist[3]['frame'])
    apply_button.configure(background='darkgrey', text='Apply', font=('calibri', 12),
                           command=lambda: apply_btn_fnc(optionlist))
    
    ok_button = Button(optionlist[3]['frame'])
    ok_button.configure(background='darkgrey', text='Okay', font=('calibri', 12), command=lambda: okay_btn_fnc(optionlist))
    
    button_list = [back_button, del_button, apply_button, ok_button]

    hgt = 14
    pdy = 5
    pdx = 2
    opt_wdth = mainframe.winfo_width()-(143+pdx*2*len(button_list))

    for n, b in enumerate(button_list):
        b.grid(row=0, column=n, padx=pdx, pady=pdy, ipady=hgt)

    optionlist[3]['frame'].update()

    for n, b in enumerate(button_list):
        b_use = b.winfo_width() / opt_wdth
        b_wnt = 1/len(button_list) - b_use
        b_range = b_wnt*opt_wdth / 2
        b.grid(ipadx=b_range)

    height_three = optionlist[3]['frame'].winfo_height()
    optionlist[3]['frame'].grid_propagate(False)
    optionlist[3]['frame'].configure(width=mainframe.winfo_width()-130, height=height_three)

    return dp


def pressed_kartei(m, btn_list):
    global back
    global backtyp
    for btn in btn_list:
        if btn['name'] == m[0]:
            btn['goto'].configure(background='lightgray')
        else:
            btn['goto'].configure(background='grey')
        root.update()
    back = m[0]
    backtyp = m[1]


def apply_btn_fnc(optlist):
    title = str_cleanup(optlist[0]['children'][0].get())
    text = str_cleanup(optlist[0]['children'][1].get('1.0', END))
    api_state = optlist[1]['children'][0].get()
    api_conf = str_cleanup(optlist[1]['children'][1].get())
    api_lnk = optlist[1]['children'][2].get()

    img_state = optlist[2]['children'][0].get()
    img_big = optlist[2]['children'][1].get()
    img_pre_pth = str_cleanup(optlist[2]['children'][2].get())
    
    svid = optlist[4].replace('#', '')
    if img_state:
        try:
            filend = img_pre_pth.split('.')
            filend = filend[-1]
            img_pth = f'dmps/{svid}.{filend}'
            if img_pre_pth != img_pth:
                shutil.copyfile(img_pre_pth, img_pth)

        except Exception:
            messagebox.showerror('Image ERROR', 'Bild konnte entweder nicht gefunden werden oder Zugriff wurde verweigert')
            img_pth = f'./dmps/{svid}.png'
    else:
        img_pth = f'./dmps/{svid}.png'
    qr_state = optlist[2]['children'][3].get()
    qr_data = str_cleanup(optlist[2]['children'][4].get('1.0', END))
    tmp = {"title": title, "txt": text, "api": api_state, "api_conf": api_conf, "api_lnk": api_lnk,
           "img": (img_state, img_pth, img_big), "qr": qr_state, "qr_data": qr_data, "id": optlist[4]}
    for i, t in enumerate(eintragliste.dump):
        for n, d in enumerate(t):
            if d['id'] == optlist[4]:
                eintragliste.dump[i][n] = tmp
                eintragliste.savedump()
                eintragliste.reloaddump()
                break


def okay_btn_fnc(optlist):
    apply_btn_fnc(optlist)
    bck_btn_fnc()


def del_btn_fnc(d):
    if not messagebox.askyesno(f'Are you sure you want to delete entry \'{d["title"]}\'?'):
        return
    for m, tt in enumerate(eintragliste.dump):
        for n, e in enumerate(tt):
            if e['id'] == d['id']:
                eintragliste.dump[m].pop(n)
                eintragliste.savedump()
                eintragliste.reloaddump()
    bck_btn_fnc()


if __name__ == '__main__':
    root.geometry(f"{x}x{y}+100+100")
    root.resizable(False, False)
    root.configure(background='black')
    root.update()

    mainframe.configure(width=root.winfo_width(), height=root.winfo_height(), background="grey")
    mainframe.grid(column=0, row=0, sticky=E)
    mainframe.grid_propagate(False)
    root.update()

    selection_frame.configure(width=mainframe.winfo_width()-125, height=mainframe.winfo_height(),
                              background='lightgray')
    selection_frame.grid(column=1, row=0, sticky=E)
    selection_frame.grid_propagate(False)
    root.update()

    type_selector_frame.configure(width=125, height=mainframe.winfo_height(), background='lightgray')
    type_selector_frame.grid(column=0, row=0)
    type_selector_frame.grid_propagate(True)
    root.update()

    karteien = [
        {'name': 'DaylyTea',
         'typ': eintragliste.daylytea,
         'goto': Button(type_selector_frame,
                        command=lambda: show_frame_x(karteien[0]['name'], karteien,
                                                     selection_frame.winfo_height(), karteien[0]['typ']))},
        {'name': 'Notes',
         'typ': eintragliste.notes,
         'goto': Button(type_selector_frame,
                        command=lambda: show_frame_x(karteien[1]['name'], karteien,
                                                     selection_frame.winfo_height(), karteien[1]['typ']))},
        {'name': 'Upcoming',
         'typ': eintragliste.upcoming,
         'goto': Button(type_selector_frame,
                        command=lambda: show_frame_x(karteien[2]['name'], karteien,
                                                     selection_frame.winfo_height(), karteien[2]['typ']))},
        {'name': 'Weather',
         'typ': eintragliste.weather,
         'goto': Button(type_selector_frame,
                        command=lambda: show_frame_x(karteien[3]['name'], karteien,
                                                     selection_frame.winfo_height(), karteien[3]['typ']))},
        {'name': 'Space',
         'typ': eintragliste.space,
         'goto': Button(type_selector_frame,
                        command=lambda: show_frame_x(karteien[4]['name'], karteien,
                                                     selection_frame.winfo_height(), karteien[4]['typ']))},
        {'name': 'Crypto',
         'typ': eintragliste.crypto,
         'goto': Button(type_selector_frame,
                        command=lambda: show_frame_x(karteien[5]['name'], karteien,
                                                     selection_frame.winfo_height(), karteien[5]['typ']))},
        {'name': 'Mails',
         'typ': eintragliste.mails,
         'goto': Button(type_selector_frame,
                        command=lambda: show_frame_x(karteien[6]['name'], karteien,
                                                     selection_frame.winfo_height(), karteien[6]['typ']))}
    ]

    for c, k in enumerate(karteien):
        k['goto'].configure(text=k['name'], background='grey', borderwidth=1, relief='flat')
        k['goto'].grid(column=0, row=c, pady=1)
    root.update()
    irange = ((root.winfo_height() - type_selector_frame.winfo_height()) / (len(karteien)*2))
    for c, k in enumerate(karteien):
        k['goto'].grid(ipady=irange, ipadx=(125-k['goto'].winfo_width())/2)

    mainloop()
