from setuptools import setup, find_packages

setup(
    name="project_tehnocat",
    version="1.0.8",
    description="Personal assistant CLI tool. Manage your contacts and notes.",
    url="https://github.com/st3n/project-TehnoCat",
    author="TehnoCat Team",
    author_email="tehnocat@example.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["tehnocat = project_tehnocat.assistant_bot_main:main"]},
    install_requires=["prompt_toolkit", "jaro-winkler", "rich", "faker", "gnureadline"],
)
