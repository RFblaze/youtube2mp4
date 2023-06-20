from pytube import YouTube
from pytube import Playlist
from tkinter import Tk
from tkinter.filedialog import askdirectory
from colorama import init, Fore
import os
import requests
import eyed3
from eyed3.id3.frames import ImageFrame


from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3

# We need this pointer relationship to hide the empty window that appears
root = Tk()
# To not show the empty window that appears when running the code
root.withdraw()
# To make sure the dialog box to select folder appears over every window
root.attributes("-topmost", True)

# I'm pretty sure the bottom init function is to make colorama work
init()


def on_complete(stream, filepath):
    """This function is just used to display the bottom message when the download
    is completed. The parameters come from the pytube module"""
    if file_choice == "a":
        audio_filepath = filepath.replace("mp4", "mp3")

        print(
            Fore.GREEN
            + f" Audio has been successfully downloaded \033[39min {os.path.realpath(audio_filepath)}"
        )
    if file_choice == "v":
        
        # Just for appearance
        if "/" in filepath:
            filepath = filepath.replace("\\", "/")

        print(
            Fore.GREEN
            + f" Video has been successfully downloaded \033[39min {os.path.realpath(filepath)}"
        )


def on_progress(stream, chunk, bytes_remaining):
    """This function is just used to display the download progress when the download.
    The parameters come from the pytube module"""
    print(f" Progress: {round(100 - (bytes_remaining / stream.filesize * 100),2 )}%")
    print()

# My link: https://www.youtube.com/watch?v=x64N7PNd28c
link = None
while True:
    print()
    link = input(" Youtube link (type in q to quit):").strip()
    print()
    # This is to quit the program
    if link.strip().lower() == "q":
        break
    # Detecting playlist or not
    if "playlist" not in link:
        # Parameters of the video_object are to display the messages of the functions on the top
        try:
            video_object = YouTube(link, on_complete_callback=on_complete, on_progress_callback=on_progress)
        # The exception only happens when the link input is not a link
        except:
            # \033[39m is the 'anticode' that shows where to stop the color
            print(
                Fore.RED
                + " An error occured, make sure you properly copied your YouTube link \033[39m"
            )
            continue

        print(Fore.LIGHTBLUE_EX + " Information about the video: \033[39m")
        print()
        # This try and except is incase the link input is not a youtube link
        try:
            print(Fore.CYAN + f" Video Title: \033[39m  {video_object.title}")
        except:
            print(
                Fore.RED
                + " An error occured, make sure you copied a YouTube link \033[39m"
            )
            continue
        print(Fore.CYAN + f" Channel: \033[39m      {video_object.author}")
        print(
            Fore.CYAN
            + f" Video Length: \033[39m {round(video_object.length / 60,2)} minutes"
        )
        print(Fore.CYAN + f" Date: \033[39m         {video_object.publish_date}")
        print()

        print(" Choose if you would like to save a video or audio only")
        print(" V - Video and Audio (mp4)")
        print(" A - Audio only      (mp3)")
        print()
        file_choice = input(" ").strip().lower()
        print()

        if file_choice == "q":
            break

        while file_choice != "a" and file_choice != "v":
            print(" Invalid input, try again")
            print()
            print(" Choose if you would like to save a video or audio only")
            print()
            print(" V - Video and Audio (mp4)")
            print(" A - Audio only      (mp3)")
            file_choice = input(" ").strip().lower()
            print()

        path_choice = input(
            " Choose where to save your file (press enter to continue or q to quit)"
        )
        if path_choice.strip().lower() == "q":
            break
        print()
        # Asks user where to save the video or audio they want
        SAVE_PATH = askdirectory(
            title="Select Folder"
        )  # shows dialog box and return the path

        while file_choice != "a" or file_choice != "v":
            if file_choice == "v":
                # Some links don't work with get_highest resolution, so we have to handle that
                try:
                    video_object.streams.get_highest_resolution().download(SAVE_PATH)

                except:
                    video_object.streams.get_lowest_resolution().download(SAVE_PATH)

                break
            elif file_choice == "a":
                # The code structure below came from https://www.codespeedy.com/download-youtube-video-as-mp3-using-python/
                # It makes it so that the output is an mp3 instead of an mp4
                out_file = video_object.streams.get_audio_only().download(SAVE_PATH)
                base, ext = os.path.splitext(out_file)
                new_file = base + ".mp3"
                try:
                    os.rename(out_file, new_file)
                except FileExistsError:
                    pass

                response = requests.get(video_object.thumbnail_url)
                response.raise_for_status()
                
                # audiofile = eyed3.load(os.path.realpath(new_file))
                # if (audiofile.tag == None):
                #     audiofile.initTag()

                # audiofile.tag.images.set(ImageFrame.FRONT_COVER, response.content, 'rb', 'image/jpeg' )
                # audiofile.tag.save()

                # mp3_obj = MP3(os.path.realpath(new_file), ID3=ID3)

                # mp3_obj = ID3()

                # mp3_obj.add(APIC(
                #     encoding=3,  # UTF-8
                #     mime='image/jpeg',
                #     type=3,  # Front cover
                #     desc='Cover',
                #     data= response.content
                # ))

                # mp3_obj.save(new_file)

                break
    if "playlist" in link:
        try:
            playlist_object = Playlist(link)
        except:
            # The exception only happens when the link input is not a link
            # print(Fore.RED + ' An error occured, make sure you properly copied your YouTube link. \033[39m')
            continue
        print(Fore.LIGHTBLUE_EX + " Information about the playlist: \033[39m")
        print()
        # This try and except is incase the link input is not a youtube link
        try:
            print(Fore.CYAN + f" Playlist Title: \033[39m   {playlist_object.title}")
        except:
            print(
                Fore.RED
                + " An error occured, make sure you copied a YouTube link OR that your playlist is not private \033[39m"
            )
            continue
        print(Fore.CYAN + f" Channel: \033[39m          {playlist_object.owner}")
        print(Fore.CYAN + f" Number of Videos: \033[39m {playlist_object.length}")
        print()

        print(
            " Choose if you would like to save every video in your playlist as video or audio files"
        )
        print(" V - Video and Audio (mp4)")
        print(" A - Audio only      (mp3)")
        print()
        file_choice = input(" ").strip().lower()
        print()

        while file_choice != "a" and file_choice != "v":
            print(" Invalid input, try again")
            print()
            print(" Choose if you would like to save a video or audio only")
            print()
            print(" V - Video and Audio (mp4)")
            print(" A - Audio only      (mp3)")
            file_choice = input(" ").strip().lower()
            print()

        path_choice = input(
            " Choose where to save your files (press enter to continue or q to quit)"
        )
        if path_choice.strip().lower() == "q":
            break
        print()
        # Asks user where to save the video or audio they want
        SAVE_PATH = askdirectory(
            title="Select Folder"
        )  # shows dialog box and return the path
        while file_choice != "a" or file_choice != "v":
            if file_choice == "v":
                # Some links don't work with get_highest resolution, so we have to handle that
                try:
                    for video in playlist_object.videos:
                        video.streams.get_highest_resolution().download(SAVE_PATH)
                        print(
                            Fore.CYAN
                            + f"{video.title}\033[39m has been successfully downloaded"
                        )
                        print()
                except:
                    for video in playlist_object.videos:
                        video.streams.get_lowest_resolution().download(SAVE_PATH)
                        print(
                            Fore.CYAN
                            + f"{video.title}\033[39m has been successfully downloaded"
                        )
                        print()
                break
            elif file_choice == "a":
                # The code structure below came from https://www.codespeedy.com/download-youtube-video-as-mp3-using-python/
                # It makes it so that the output is an mp3 instead of an mp4
                for audio in playlist_object.videos:
                    out_file = audio.streams.get_audio_only().download(SAVE_PATH)
                    base, ext = os.path.splitext(out_file)
                    new_file = base + ".mp3"
                    os.rename(out_file, new_file)
                    print(
                        Fore.CYAN
                        + f"{audio.title}\033[39m has been successfully downloaded"
                    )
                    print()
                break
# This is how to save subtitles
# >>> yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')
# >>> caption = yt.captions.get_by_language_code('en')
# >>> print(caption.generate_srt_captions())
# 1
# 00:00:10,200 --> 00:00:11,140
# K-pop!
#
# 2
# 00:00:13,400 --> 00:00:16,200
# That is so awkward to watch.
# ...
