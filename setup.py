import setuptools

setuptools.setup(
    name="FocusFlow",
    version="0.1.0",
    author="Shaheer Ahmed",
    description="A minimalist Pomodoro timer and task manager designed for focused, distraction-free productivity.",
    py_modules=["main"],
    install_requires=[
        "customtkinter==5.2.2",
        "darkdetect==0.8.0",
        "packaging==26.0"
    ],
    python_requires=">=3.10"
)