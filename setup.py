from Cython.Build import cythonize
from setuptools import setup, Extension

setup(
    name="cw-fruit-fight-2022-gui-client",
    version="0.1a0",
    author="Andrew Golovashevich",
    maintainer="Andrew Golovashevich",
    url="http://github.com/landgrafhomyak/cw-fruit-fight-2022-gui-client",
    license="CC BY-NC-SA 4.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Games/Entertainment",
        "Typing :: Typed"
    ],
    install_requires=["PySide2 == 5.15.2.1", "telethon == 1.31.1", "qasync == 0.23.0"],
    packages=[
        "cw_fruit_fight_2022_gui_client",
    ],
    package_dir={
        "cw_fruit_fight_2022_gui_client": "./cw_fruit_fight_2022_gui_client",
    },
    ext_package="cw_fruit_fight_2022_gui_client",
    package_data={
        "cw_fruit_fight_2022_gui_client": [
            "./apple.svg",
            "./banana.svg",
            "./cherry.svg",
            "./lemon.svg",
            "./orange.svg",
            "./pineapple.svg",
            "./watermelon.svg",
            "./py.typed",
            "./client.pyi"
            "./game.pyi",
            "./gui.pyi",

            "./pumpkin.svg",
            "./blood.svg",
            "./bone.svg",
            "./tooth.svg",
            "./skull.svg",
            "./brain.svg",
            "./heart.svg",
        ]
    },
    ext_modules=cythonize(
        [
            Extension(
                name="gui",
                sources=[
                    "./cw_fruit_fight_2022_gui_client/gui.pyx",
                ]
            ),
            Extension(
                name="client",
                sources=[
                    "./cw_fruit_fight_2022_gui_client/client.pyx",
                ]
            ),
            Extension(
                name="game",
                sources=[
                    "./cw_fruit_fight_2022_gui_client/game.pyx",
                    "./cw_fruit_fight_2022_gui_client/_game.c",
                ]
            )
        ],
        compiler_directives={'language_level': "3"}
    )
)
