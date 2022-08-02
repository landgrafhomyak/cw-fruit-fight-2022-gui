import os

import PyInstaller.__main__

res_file = open("./src/res.py", "wt")

for fname in os.listdir("./res"):
    if fname.endswith(".svg"):
        res_file.write("svg_" + fname[:-4] + " = ")

        with open("./res/" + fname) as svg:
            res_file.write(svg.read().__repr__())

        res_file.write("\n")

res_file.close()

PyInstaller.__main__.run([
    "--distpath", "dist",
    "--workpath", "build",
    "--specpath", "build",
    "--clean",
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--name", "cw-fruit-fight-2022-gui-client",
    "./src/main.py"
])
