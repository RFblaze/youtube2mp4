# youtube2mp4

## Instructions for running

The are two ways to run this program

- Running the Python file
- Running the executable ".exe" file
  _Note: The executable file only works for Windows at the moment_

### - Running the Python file

The python file contains a library called pytube (check the documentation [here](https://pytube.io/en/latest/)) which takes care of fetching the video and audio streams of a Youtube video and must be installed on your local computer to run this program. You can simply install it by running

```sh
pip install pytube
```

#FIXME I also messed around with the pytube installation and must find what I changed about it to make it work.

### - Running the executable

The executable is the simplest way to use the program. It was created using auto-py-to-exe (check it [here](https://pypi.org/project/auto-py-to-exe/)) and packages all the dependencies within the executable file, meaning that it can be ran without installing anything. Simply downloading and running the executable should work

_Note: The executable might not always be up to date with the python file as I may forget to create an executable when a change to the python file has been made_

### Issues

1. On Windows, the program writes the output file path wrong for both audio and video options. It puts a back slash before the saved file instead of a forward slash. For example:

```sh
Video has been successfully downloaded in C:/path/to/file\my_vid.mp4
```
