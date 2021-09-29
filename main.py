# Sort photo files to folders by date.
# Folders are created and named in format YYYY-MM-DD

from os import mkdir, walk
from os.path import join
from datetime import datetime
from shutil import move

from PIL import Image, UnidentifiedImageError
import wx

from gui import Language, MainPanel


def main():
    app = wx.App()

    ln = Language("fi")
    frame = wx.Frame(None, title=ln["title"])
    panel = MainPanel(frame, ln)

    panel.cb_on_dir_choice(get_filenames)
    panel.cb_sort(sort)
    
    frame.Show(True)
    app.MainLoop()

def get_filenames(dir):
    _, _, filenames = next(walk(dir), (None, None, []))
    return filenames

def sort(dir, progress):
    _, _, filenames = next(walk(dir), (None, None, []))
    source = None
    target = None
    n_max = len(filenames)
    n = 0
    skipped = 0

    print("Found {} files in {}".format(len(filenames), dir))
    print("Sorting files to folders...")

    for filename in filenames:
        source = join(dir, filename)
        date = None
        try:
            with Image.open(source) as im:
                try:
                    date = datetime.strptime(
                        im.getexif().get(0x0132),
                        "%Y:%m:%d %H:%M:%S"
                    ).date()
                except (TypeError, ValueError):
                    skip(n, n_max, skipped, progress)
                    continue

        except UnidentifiedImageError as e:
            print("File skipped. {} is not an image.".format(e))
            skip(n, n_max, skipped, progress)
            continue

        target = join(dir, str(date))

        try:
            mkdir(target)
        except FileExistsError:
            pass

        if source:
            move(source, join(target, filename))

        n = n + 1
        progress(n, n_max, skipped)

def skip(n, n_max, skipped, progress):
    n = n + 1
    skipped = skipped + 1
    progress(n, n_max, skipped)


if __name__ == "__main__":
    main()