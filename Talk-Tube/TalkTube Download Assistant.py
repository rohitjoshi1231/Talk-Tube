# importing packages
import requests
import speech_recognition as sr
from pytube import YouTube
from pytube.cli import on_progress

# importing the api key, which returns api key.
from api.api_key import my_api_key

# url to access youtube data api
URL = 'https://www.googleapis.com/youtube/v3/search'
OPTIONS = {'audio': 'Audio', 'video': 'High Quality'}


def on_complete(stream, file_path):
    print(f"Download of '{stream.title}' completed!\n")


def get_user_input(prompt):
    """Obtaining user input using the Speech Recognition library."""
    try:
        with sr.Microphone() as source:
            print(prompt)
            audio = recognizer.listen(source)
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
        return text
    except sr.exceptions.RequestError:
        print("No Connection , turn on Data...")


def choose_option():
    """Selecting the options of the video."""
    print("Choose an option:")
    for key, value in OPTIONS.items():
        print(f"- {value} ({key})")

    selected_option = get_user_input("Say the option name...")
    return selected_option.lower()


def download_video(selected_option, video_link):
    """Downloads and retrieves the video or audio stream as appropriate."""
    try:
        yt = YouTube(video_link, on_progress_callback=on_progress,
                     on_complete_callback=on_complete)

        if selected_option in OPTIONS:
            download_stream = yt.streams.get_audio_only(
                'webm') if selected_option == 'audio' else yt.streams.get_highest_resolution()
            download_stream.download('./download')
            print(f"Download of '{yt.title}' completed.")
        else:
            print("Option not recognized.")
    except Exception as e:
        print("Error:", str(e))

        
def recognize():
    text = get_user_input("Tell the topic you're looking for...")
    params = {
        'key': my_api_key(),
        'q': text,
        'part': 'snippet',
        'maxResults': 1,
        'type': 'video'}

    response = requests.get(url=URL, params=params)
    data = response.json()

    try:
        # fetching the video id and its link from the api
        video_id = data['items'][0]['id']['videoId']
        video_link = f"https://www.youtube.com/watch?v={video_id}"
        selected_option = choose_option()
        download_video(selected_option, video_link)
    except KeyError:
        print("Error processing API response.")


if __name__ == '__main__':
    # initializing the speech recognizer
    recognizer = sr.Recognizer()
    try:
        if get_user_input("Tell, How You want to download Link/Voice...") == 'voice':
            recognize()
        else:
            print([v for k, v in OPTIONS.items()])
            op = input(">>>")
            link = input('link: ')
            download_video(op, link)
    except Exception as er:
        print("Error: ",er)