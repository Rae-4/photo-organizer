# Sort photo files to folders by date.
# Folders are created and named in format YYYY-MM-DD

from os import getcwd, mkdir, walk
from os.path import join
from datetime import datetime
from shutil import move


from PIL import Image


def main():
    _, _, filenames = next(walk(getcwd()), (None, None, []))
    source = None
    cwd = getcwd()
    target = None

    print("Found {} files in {}".format(len(filenames), cwd))
    print("Sorting files to folders...")

    for filename in filenames:
        source = join(cwd, filename)
        date = None
        with Image.open(source) as im:
            date = datetime.strptime(
                im.getexif().get(0x0132),
                "%Y:%m:%d %H:%M:%S"
            ).date()

        target = join(cwd, str(date))

        try:
            mkdir(target)
        except FileExistsError:
            pass

        if source:
            move(source, join(target, filename))


if __name__ == "__main__":
    main()