from setuptools import setup

setup(
    name="project_tehnocat",
    version="1.0.0",
    description="Personal assistant CLI tool. Manage your contacts and notes.",
    url="https://github.com/st3n/project-TehnoCat",
    author="TehnoCat Team",
    author_email="tehnocat@example.com",
    license="MIT",
    packages=["src"],
    include_package_data=True,
    entry_points={"console_scripts": ["tehnocat = src.assistant_bot_main:main"]},
    install_requires=["prompt_toolkit", "jaro-winkler", "rich", "faker", "gnureadline"],
)
