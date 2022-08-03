from setuptools import setup, Extension

setup(
    name="cw-fruit-fight-2022-gui-client",
    version="0.0b0",
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
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Topic :: Games/Entertainment",
        "Typing :: Typed"
    ],
    install_requires=["PySide2 == 5.15.2.1", "telethon == 1.24.0"],
    packages=[
        "cw_fruit_fight_2022_gui_client",
        "cw_fruit_fight_2022_gui_client.gui",
    ],
    package_dir={
        "cw_fruit_fight_2022_gui_client": "./src/cw_fruit_fight_2022_gui_client",
        "cw_fruit_fight_2022_gui_client.gui": "./src/cw_fruit_fight_2022_gui_client/gui"
    },
    ext_package="cw_fruit_fight_2022_gui_client",
    package_data={
        "cw_fruit_fight_2022_gui_client.gui": ["./*.svg"]
    }
)
