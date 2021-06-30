import os
import ast
import sys
import shutil
import tkinter as tk
import tkinter.filedialog
from PIL import Image
from flask import Flask, request, render_template, send_from_directory, jsonify, Response


class SetupWindow:
    def __init__(self):
        self.done = False
        self.jpeg_loc = None
        self.tiff_loc = None
        self.import_loc = None
        self.motioncorr_loc = None
        self.ctf_loc = None
        self.save_loc = None

        self.root = tk.Tk()
        self.root.title('GemIO - Setup')

        self.jpeg_folder = tk.StringVar()
        self.tiff_folder = tk.StringVar()
        self.import_file = tk.StringVar()
        self.motioncorr_file = tk.StringVar()
        self.ctf_file = tk.StringVar()
        self.save_folder = tk.StringVar()

        OPTIONAL_ROW = 0
        JPEG_ROW = 1
        TIFF_ROW = 2
        IMPORT_ROW = 3
        MOTIONCORR_ROW = 4
        CTF_ROW = 5
        SAVE_ROW = 6
        SUBMIT_ROW = 7

        self.optional_label = tk.Label(self.root, text='* optional')
        self.jpeg_label = tk.Label(self.root, text='Directory of jpeg files: ')
        self.jpeg_entry = tk.Entry(self.root, width=20, textvariable=self.jpeg_folder)
        self.jpeg_button = tk.Button(self.root, text='Browse', command=lambda: self.browse_folder('jpeg'))
        self.tiff_label = tk.Label(self.root, text='Directory of tiff files: ')
        self.tiff_entry = tk.Entry(self.root, width=20, textvariable=self.tiff_folder)
        self.tiff_button = tk.Button(self.root, text='Browse', command=lambda: self.browse_folder('tiff'))
        self.import_label = tk.Label(self.root, text='* Import star file: ')
        self.import_entry = tk.Entry(self.root, width=20, textvariable=self.import_file)
        self.import_button = tk.Button(self.root, text='Browse', command=lambda: self.browse_file('import'))
        self.motioncorr_label = tk.Label(self.root, text='* MotionCorr star file: ')
        self.motioncorr_entry = tk.Entry(self.root, width=20, textvariable=self.motioncorr_file)
        self.motioncorr_button = tk.Button(self.root, text='Browse', command=lambda: self.browse_file('motioncorr'))
        self.ctf_label = tk.Label(self.root, text='* CtfFind star file: ')
        self.ctf_entry = tk.Entry(self.root, width=20, textvariable=self.ctf_file)
        self.ctf_button = tk.Button(self.root, text='Browse', command=lambda: self.browse_file('ctf'))
        self.save_label = tk.Label(self.root, text='* Directory to save new files: ')
        self.save_entry = tk.Entry(self.root, width=20, textvariable=self.save_folder)
        self.save_button = tk.Button(self.root, text='Browse', command=lambda: self.browse_folder('save'))
        self.submit_button = tk.Button(self.root, text='Submit', command=self.go_next)

        self.optional_label.grid(row=OPTIONAL_ROW, column=1)
        self.jpeg_label.grid(row=JPEG_ROW, column=0, sticky=tk.E)
        self.jpeg_entry.grid(row=JPEG_ROW, column=1)
        self.jpeg_button.grid(row=JPEG_ROW, column=2)
        self.tiff_label.grid(row=TIFF_ROW, column=0, sticky=tk.E)
        self.tiff_entry.grid(row=TIFF_ROW, column=1)
        self.tiff_button.grid(row=TIFF_ROW, column=2)
        self.import_label.grid(row=IMPORT_ROW, column=0, sticky=tk.E)
        self.import_entry.grid(row=IMPORT_ROW, column=1)
        self.import_button.grid(row=IMPORT_ROW, column=2)
        self.motioncorr_label.grid(row=MOTIONCORR_ROW, column=0, sticky=tk.E)
        self.motioncorr_entry.grid(row=MOTIONCORR_ROW, column=1)
        self.motioncorr_button.grid(row=MOTIONCORR_ROW, column=2)
        self.ctf_label.grid(row=CTF_ROW, column=0, sticky=tk.E)
        self.ctf_entry.grid(row=CTF_ROW, column=1)
        self.ctf_button.grid(row=CTF_ROW, column=2)
        self.save_label.grid(row=SAVE_ROW, column=0, sticky=tk.E)
        self.save_entry.grid(row=SAVE_ROW, column=1)
        self.save_button.grid(row=SAVE_ROW, column=2)
        self.submit_button.grid(row=SUBMIT_ROW, column=0, columnspan=3)

        self.root.mainloop()

    def browse_folder(self, event):
        folder_name = tk.filedialog.askdirectory()
        if folder_name:
            if event == 'jpeg':
                self.jpeg_folder.set(folder_name)
            elif event == 'tiff':
                self.tiff_folder.set(folder_name)
            elif event == 'save':
                self.save_folder.set(folder_name)

    def browse_file(self, event):
        file_name = tk.filedialog.askopenfilename()
        if file_name:
            if event == 'import':
                self.import_file.set(file_name)
            elif event == 'motioncorr':
                self.motioncorr_file.set(file_name)
            elif event == 'ctf':
                self.ctf_file.set(file_name)

    def go_next(self):
        jpeg_exists = os.path.exists(self.jpeg_folder.get())
        tiff_exists = os.path.exists(self.tiff_folder.get())
        if self.import_file.get():
            import_exists = os.path.exists(self.import_file.get())
        else:
            import_exists = True
        if self.motioncorr_file.get():
            motioncorr_exists = os.path.exists(self.motioncorr_file.get())
        else:
            motioncorr_exists = True
        if self.ctf_file.get():
            ctf_exists = os.path.exists(self.ctf_file.get())
        else:
            ctf_exists = True
        if self.save_folder.get():
            save_exists = os.path.exists(self.save_folder.get())
        else:
            save_exists = True

        if not jpeg_exists:
            self.error_display('jpeg')
        elif not tiff_exists:
            self.error_display('tiff')
        elif not import_exists:
            self.error_display('import')
        elif not motioncorr_exists:
            self.error_display('motioncorr')
        elif not ctf_exists:
            self.error_display('ctf')
        elif not save_exists:
            self.error_display('save')
        else:
            self.top = tk.Toplevel(self.root)
            top_text = tk.Label(self.top, text='Please press OK and click on the URL in the terminal or navigate to '
                                               'http://127.0.0.1:5000/\n'
                                               'Ctrl+C on the terminal when done.')
            top_button = tk.Button(self.top, text='OK', command=self.close_next)
            top_text.pack()
            top_button.pack()
            self.top.grab_set()

    def error_display(self, error):
        self.top = tk.Toplevel(self.root)
        if error == 'jpeg' or error == 'tiff' or error == 'save':
            top_text = tk.Label(self.top, text=f'{error.upper()} directory not found!')
        else:
            top_text = tk.Label(self.top, text=f'{error.upper()} file not found!')
        top_button = tk.Button(self.top, text='OK', command=self.close_error)
        top_text.pack()
        top_button.pack()
        self.top.grab_set()

    def close_next(self):
        self.done = True
        self.jpeg_loc = self.jpeg_folder.get()
        self.tiff_loc = self.tiff_folder.get()
        if self.import_file.get():
            self.import_loc = self.import_file.get()
        if self.motioncorr_file.get():
            self.motioncorr_loc = self.motioncorr_file.get()
        if self.ctf_file.get():
            self.ctf_loc = self.ctf_file.get()
        if self.save_folder.get():
            self.save_loc = self.save_folder.get()
        self.root.destroy()

    def close_error(self):
        self.top.destroy()


if __name__ == '__main__':
    #setup = SetupWindow()
    #if setup.done:
    if True:
        """jpeg_loc = setup.jpeg_loc
        tiff_loc = setup.tiff_loc
        import_loc = setup.import_loc
        motioncorr_loc = setup.motioncorr_loc
        ctf_loc = setup.ctf_loc
        save_loc = setup.save_loc"""

        jpeg_loc = 'C:\\Users\\honki\\PycharmProjects\\Circle_Picker\\app\\data\\screenshots'
        save_loc = 'C:\\Users\\honki\\Documents'

        app = Flask(__name__)
        cli = sys.modules['flask.cli']
        cli.show_server_banner = lambda *x: None

        @app.route('/', methods=['GET', 'POST'])
        def gallery_page():
            if request.method == 'POST':
                data = {}
                import_new = []
                motioncorr_new = []
                ctf_new = []

                selected_jpegs = set(ast.literal_eval(list(request.form.to_dict().keys())[0]))
                """jpeg_trash = os.path.join(jpeg_loc, 'Trash')
                if not os.path.exists(jpeg_trash):
                    os.mkdir(jpeg_trash)
                tiff_trash = os.path.join(tiff_loc, 'Trash')
                if not os.path.exists(tiff_trash):
                    os.mkdir(tiff_trash)
                tiff_dirname = os.path.split(tiff_loc)[-1]
                if import_loc:
                    import_dir = os.path.split(import_loc)[0]
                    with open(import_loc) as f:
                        import_star = f.readlines()
                    for line in import_star:
                        img_root = line.split(' ')[0].split('.tif')[0].split('/')[-1]
                        if f'{img_root}.jpeg' not in selected_jpegs:
                            import_new.append(line)
                    if save_loc:
                        save_import = save_loc
                    else:
                        save_import = import_dir
                        old_import = import_loc.replace('.star', '_old.star')
                        if os.path.exists(old_import):
                            os.remove(old_import)
                        os.rename(import_loc, old_import)
                    with open(os.path.join(save_import, 'movies.star'), 'w+') as f:
                        for line in import_new:
                            f.write(line)

                if motioncorr_loc:
                    motioncorr_dir = os.path.split(motioncorr_loc)[0]
                    motioncorr_trash = os.path.join(motioncorr_dir, tiff_dirname, 'Trash')
                    if not os.path.exists(motioncorr_trash):
                        os.mkdir(motioncorr_trash)
                    with open(motioncorr_loc) as f:
                        motioncorr_star = f.readlines()
                    for line in motioncorr_star:
                        img_root = line.split(' ')[0].split('.mrc')[0].split('_noDW')[0].split('/')[-1]
                        if f'{img_root}.jpeg' not in selected_jpegs:
                            motioncorr_new.append(line)
                    if save_loc:
                        save_motioncorr = save_loc
                    else:
                        save_motioncorr = motioncorr_dir
                        old_motioncorr = motioncorr_loc.replace('.star', '_old.star')
                        if os.path.exists(old_motioncorr):
                            os.remove(old_motioncorr)
                        os.rename(motioncorr_loc, old_motioncorr)
                    with open(os.path.join(save_motioncorr, 'corrected_micrographs.star'), 'w+') as f:
                        for line in motioncorr_new:
                            f.write(line)
                if ctf_loc:
                    ctf_dir = os.path.split(ctf_loc)[0]
                    ctf_trash = os.path.join(ctf_dir, tiff_dirname, 'Trash')
                    if not os.path.exists(ctf_trash):
                        os.mkdir(ctf_trash)
                    with open(ctf_loc) as f:
                        ctf_star = f.readlines()
                    for line in ctf_star:
                        img_root = line.split(' ')[0].split('.mrc')[0].split('_noDW')[0].split('/')[-1]
                        if f'{img_root}.jpeg' not in selected_jpegs:
                            ctf_new.append(line)
                    if save_loc:
                        save_ctf = save_loc
                    else:
                        save_ctf = ctf_dir
                        old_ctf = ctf_loc.replace('.star', '_old.star')
                        if os.path.exists(old_ctf):
                            os.remove(old_ctf)
                        os.rename(ctf_loc, old_ctf)
                    with open(os.path.join(save_ctf, 'micrographs_ctf.star'), 'w+') as f:
                        for line in ctf_new:
                            f.write(line)

                for jpeg in selected_jpegs:
                    jpeg_full = os.path.join(jpeg_loc, jpeg)
                    if os.path.exists(jpeg_full):
                        shutil.move(jpeg_full, jpeg_trash)
                    tiff_full = os.path.join(tiff_loc, jpeg.replace('.jpeg', '.tif'))
                    if os.path.exists(tiff_full):
                        shutil.move(tiff_full, tiff_trash)
                    if motioncorr_loc:
                        motioncorr_extensions = ['0-Patch-FitCoeff.log', '0-Patch-Frame.log', '0-Patch-Full.log',
                                                 '0-Patch-Patch.log', '.com', '.err', '.mrc', '_noDW.mrc', '.out',
                                                 '_shifts.eps', '.star']
                        for extension in motioncorr_extensions:
                            motioncorr_full = os.path.join(motioncorr_dir, tiff_dirname,
                                                           jpeg.replace('.jpeg', extension))
                            if os.path.exists(motioncorr_full):
                                shutil.move(motioncorr_full, motioncorr_trash)
                    if ctf_loc:
                        ctf_extensions = ['_avrot.txt', '.ctf', '_ctffind4.com', '_ctffind4.log', '.mrc', '.txt']
                        for extension in ctf_extensions:
                            ctf_full = os.path.join(ctf_dir, tiff_dirname, jpeg.replace('.jpeg', f'_noDW{extension}'))
                            if os.path.exists(ctf_full):
                                shutil.move(ctf_full, ctf_trash)
                            else:
                                ctf_full = os.path.join(ctf_dir, tiff_dirname, jpeg.replace('.jpeg', extension))
                                if os.path.exists(ctf_full):
                                    shutil.move(ctf_full, ctf_trash)"""

                if save_loc:
                    save_selected = os.path.join(save_loc, 'selected.txt')
                else:
                    save_selected = os.path.join(os.getcwd(), 'selected.txt')
                with open(save_selected, 'w+') as f:
                    for jpeg in sorted(selected_jpegs):
                        f.write(f'{jpeg}\n')

                data['selected'] = len(selected_jpegs)
                data['location'] = save_selected

                return jsonify(data)
            else:
                jpegs = sorted({file for file in os.listdir(jpeg_loc) if file.endswith('.png')})
                if jpegs:
                    image = Image.open(os.path.join(jpeg_loc, jpegs[0]))
                    full_width, full_height = image.size
                    width = 400
                    height = full_height // (full_width//width)
                else:
                    width = 400
                    height = 400
                return render_template('main.html', directory=jpeg_loc, jpegs=jpegs, width=width, height=height)

        @app.route('/jpeg/<path:filename>')
        def jpeg_directory(filename):
            return send_from_directory(jpeg_loc, filename)

        app.run()
