import wx
from wx.core import DirDialog


class Language:

    data_en = {
        "title": "Photo Organizer",
        "browse": "Browse",
        "dir": "Choose a directory:",
        "dirlabel": "Directory of the photos",
        "n_photos": "Found {} files in selected folder.",
        "no_sel": "No directory selection.",
        "sort": "Sort",
        "progress": "Sorted: {}/{}",
        "progress_2": "Sorted: {}/{} - skipped {}"
    }
    data_fi = {
        "title": "Kuvien lajittelu",
        "browse": "Selaa",
        "dir": "Valitse kansio:",
        "dirlabel": "Kuvien sijainti",
        "n_photos": "{} tiedostoa valitussa kansiossa.",
        "no_sel": "Kansiota ei ole valittu.",
        "sort": "Jäjestä",
        "progress": "Tehty: {}/{}",
        "progress_2": "Tehty: {}/{} - ohitettu: {}"
    }

    def __init__(self, language_code):
        self.data = None

        if language_code == "fi":
            self.data = Language.data_fi
        elif language_code == "en":
            self.data = Language.data_en
        else:
            raise KeyError(f"'{language_code}' is not a used or valid language code.")

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError as e:
            print(f"Key '{e}' is not defined in Language class.")
            return "<" + key + ">"
        except TypeError as e:
            print("No language chosen.")
            raise e


class MainPanel(wx.Panel):
    def __init__(self, parent, ln: Language):
        super().__init__(parent)
        self.ln = ln
        self.on_dir_choice = None
        self.on_sort = None

        txt_dir_label = wx.StaticText(self, label=ln["dirlabel"])
        self.txt_n = wx.StaticText(self, label=ln["no_sel"])
        self.txt_progress = wx.StaticText(self, label="")
        btn_browse = wx.Button(self, label=ln["browse"])
        btn_sort = wx.Button(self, label=ln["sort"])
        self.txt_browse = wx.TextCtrl(self, value="", size=(260,-1))
        self.txt_browse.Disable()

        self.Bind(wx.EVT_BUTTON, self.open_dirdialog, btn_browse)
        self.Bind(wx.EVT_BUTTON, self.sort, btn_sort)

        sizer_file = wx.BoxSizer(wx.HORIZONTAL)
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer_file.Add(self.txt_browse, 0, wx.RIGHT, 5)
        sizer_file.Add(btn_browse, 0, wx.RIGHT, 5)
        sizer.Add(txt_dir_label, 0, wx.TOP|wx.LEFT|wx.EXPAND, 10)
        sizer.Add((5,5), 0)
        sizer.Add(sizer_file, 0, wx.LEFT|wx.EXPAND, 10)
        sizer.Add((5,5), 0)
        sizer.Add(self.txt_n, 0, wx.LEFT|wx.EXPAND, 10)
        sizer.Add((5,5), 0)
        sizer.Add(btn_sort, 0, wx.LEFT, 10)
        sizer.Add((5,5), 0)
        sizer.Add(self.txt_progress, 0, wx.LEFT, 10)

        self.SetSizer(sizer)

    def open_dirdialog(self, evt):
        with DirDialog(self, self.ln["dir"], style=wx.DD_DIR_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.txt_browse.SetValue(dlg.GetPath())
                n = len(self.on_dir_choice(dlg.GetPath()))
                self.txt_n.SetLabel(self.ln["n_photos"].format(n))

    def update_progress(self, n, max, skipped):
        if skipped <= 0:
            self.txt_progress.SetLabel(self.ln["progress"].format(n, max))
        else:
            self.txt_progress.SetLabel(self.ln["progress_2"].format(n, max, skipped))


    def sort(self, evt):
        self.on_sort(self.txt_browse.GetValue(), self.update_progress)

    def cb_sort(self, fn):
        """
        fn: None fn()
        """
        self.on_sort = fn

    def cb_on_dir_choice(self, fn):
        """
        fn: int fn(dir_path)
        """
        self.on_dir_choice = fn


if __name__ == "__main__":
    app = wx.App()

    ln = Language("fi")
    frame = wx.Frame(None, title="TestFrame", size=(600,400))
    panel = MainPanel(frame, ln)
    
    frame.Show(True)
    app.MainLoop()
