import os

res_file = open("./src/res.py", "wt")

for fname in os.listdir("./res"):
    if fname.endswith(".svg"):
        res_file.write("svg_" + fname[:-4] + " = \"")

        with open("./res/" + fname) as svg:
            for c in svg.read():
                code = hex(ord(c))[2:]
                if len(code) > 4:
                    res_file.write("\\U" + code.zfill(8))
                else:
                    res_file.write("\\u" + code.zfill(4))
        res_file.write("\"\n")
