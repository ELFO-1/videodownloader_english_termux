#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author :  ELFO
#
#videodownloader for termux

import os
import subprocess
import glob
import configparser
import sys
from pathlib import Path

download_path = os.path.join(os.path.expanduser('~'), 'storage/downloads/videodownloader')
os.makedirs(download_path, exist_ok=True)
os.chdir(download_path)

def load_config():
    """Loads the configuration or creates a new one"""
    config = configparser.ConfigParser()
    config_file = Path.home() / '.config' / 'ytdownloader' / 'config.ini'

    # Create directory if it does not exist
    config_file.parent.mkdir(parents=True, exist_ok=True)

    if config_file.exists():
        config.read(config_file)
    else:
        config['DEFAULT'] = {
            'cookies_file': '',
        }
        with open(config_file, 'w') as f:
            config.write(f)

    return config, config_file

def setup_cookies():
    """Configures the path to the cookies file"""
    config, config_file = load_config()

    current_cookies = config['DEFAULT'].get('cookies_file', '')
    print(f"\nCurrent cookies file: {current_cookies or 'Not configured'}")

    change = input("Do you want to change the path to the cookies file? (y/n): ")
    if change.lower() == 'y':
        new_path = input("Enter the full path to cookies.txt: ")
        if os.path.exists(new_path):
            config['DEFAULT']['cookies_file'] = new_path
            with open(config_file, 'w') as f:
                config.write(f)
            print("Cookies path updated successfully!")
        else:
            print("Error: The specified file does not exist!")

    return config['DEFAULT'].get('cookies_file', '')

def convert_to_wav(video_file):
    """Converts video to WAV format for audio CD"""
    try:
        output_file = os.path.splitext(video_file)[0] + '.wav'
        subprocess.run([
            'ffmpeg', '-i', video_file,
            '-vn',  # Keine Video-Streams
            '-acodec', 'pcm_s16le',  # CD-Quality Audio
            '-ar', '44100',  # Sample Rate für Audio-CD
            '-ac', '2',  # Stereo
            output_file
        ], check=True)
        print(f"Successfully converted to: {output_file}")
        return output_file
    except subprocess.CalledProcessError:
        print("Conversion error.")
        return None

def convert_to_mp3(video_file):
    """Converts video to MP3 format"""
    try:
        output_file = os.path.splitext(video_file)[0] + '.mp3'
        subprocess.run([
            'ffmpeg', '-i', video_file,
            '-vn',  # Keine Video-Streams
            '-acodec', 'libmp3lame',  # MP3 Codec
            '-ab', '320k',  # Bitrate
            '-ar', '44100',  # Sample Rate
            '-ac', '2',  # Stereo
            output_file
        ], check=True)
        print(f"Successfully converted to: {output_file}")
        return output_file
    except subprocess.CalledProcessError:
        print("Conversion error.")
        return None

def convert_audio(video_file, format_type):
    """Converts video to the selected audio format"""
    if format_type == "mp3":
        return convert_to_mp3(video_file)
    else:  # wav für Audio-CD
        return convert_to_wav(video_file)

def main():
    print("\n=== Videodownloader and converter by Elfo === "
    )

    # Cookies-Setup
    print("\n=== For YouTube with cookie support ===")
    cookies_file = setup_cookies()

    while True:
        url = input("\nEnter video URL (or 'q' to exit): ")

        if url.lower() == 'q':
            break

        # Prepare download command
        download_cmd = ["yt-dlp", "-f", "b"]

        # Add cookies if configured
        if cookies_file:
            download_cmd.extend(["--cookies", cookies_file])

        download_cmd.append(url)

        # Video herunterladen
        try:
            subprocess.run(download_cmd, check=True)
            print("Video downloaded successfully.")

            # Find the last downloaded video
            video_files = glob.glob("*.mp4") + glob.glob("*.webm") + glob.glob("*.mkv")
            if video_files:
                latest_video = max(video_files, key=os.path.getctime)
                print(f"Found video: {latest_video}")

                # Question about the desired format
                print("\nIn which format do you want to convert the video?")
                print("1: MP3")
                print("2: Audio-CD Format (WAV)")
                format_choice = input("Choose 1 oder 2: ")

                if format_choice in ['1', '2']:
                    format_type = "mp3" if format_choice == '1' else "wav"
                    audio_file = convert_audio(latest_video, format_type)
                    if audio_file:
                        print("\nConversion completed!")
                        print(f"The audio file was created: {audio_file}")
                        if format_type == "wav":
                            print("You can now burn this file with your preferred CD burning program.")
                else:
                    print("Invalid selection.")
            else:
                print("No video file found.")

        except subprocess.CalledProcessError:
            print("Error downloading video.")

        another = input("\nWould you like to download anotherunterlade (y/n): ")
        if another.lower() != 'y':
            break

if __name__ == "__main__":
    main()
