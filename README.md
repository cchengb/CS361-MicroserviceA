# README for Music Generation Microservice
# Overview
This repository hosts the Music Generation Microservice, a Flask-based application designed to generate music dynamically based on user-defined parameters such as the number of notes, musical scale, and instrument. This document offers detailed instructions and necessary documentation to ensure easy integration and usage.

# Getting Started
Prerequisites
1. Python 3.x
2. Flask
3. Requests
4. music21 library
5. soundfonts(GeneralUserGS.sf2) download link: https://www.dropbox.com/s/4x27l49kxcwamp5/GeneralUser_GS_1.471.zip?dl=1
   create the folder soundfonts under the root directory, then put the download GeneralUserGS.sf2 under soundfont folder.
7. An environment capable of playing MP3 files (e.g., VLC, browser, or media player)
    
# Installation
1.	Clone this repository to your local machine or (you could download the music.py, index.html, test_music_server.py, and the soundfonts from the above link).
2.	Install the required Python dependencies, if you use the pycharm run it under
source .venv/bin/activate  
pip install flask music21 requests 

3.	Start the Flask server by running Music.py within your project directory:
python Music.py 

# Usage Instructions
Using the test_music_service.py Script

The test_music_service.py script is designed for you to interact with the Music Generation Microservice by sending HTTP GET requests to generate music and then downloading the produced MP3 file if available. Below is a breakdown of how to use this script:
1.	Configuration:
   
    a. Ensure your Flask server is running at http://127.0.0.1:5000.

    b. The test_music_service.py script should be in the same project directory.

2.	Execution:
   
	a. Run the script from your command line:
python test_music_service.py

    b. The script will make a request to the microservice, handle the response, download the music file, and automatically play it in the background.

# Programmatically Requesting Data from the Microservice
Here is how the script makes requests to the microservice, you could find the code under the test_music_service.py, just need to run python test_musci_service.py:

<img width="452" alt="image" src="https://github.com/cchengb/CS361-Microsoftservice-A/assets/145725044/7f3ad6e2-daae-42e4-b6c4-d07ca70bf99e">

# Handling the Response and Downloading Files
Upon receiving a successful response, the script processes the JSON data, retrieves the URL of the generated music file, and downloads it into the downloads folder, it also will play automatically in the background, you can find the dowloaded mp3 under the folder downloads:

<img width="496" alt="image" src="https://github.com/cchengb/CS361-Microsoftservice-A/assets/145725044/003f3759-a2d1-4791-9150-1e674a08f638">

<img width="288" alt="image" src="https://github.com/cchengb/CS361-Microsoftservice-A/assets/145725044/ce4a5244-7623-4aaf-8556-df41c3983c85">


# UML Sequence Diagram Elements more details as below:
 <img width="468" alt="image" src="https://github.com/cchengb/CS361-Microsoftservice-A/assets/145725044/914b7702-7d58-4270-b4f6-9cfac3aafdc8">

Participants:
1.	Client (Test Music Service): Executes the GET request.
2.	HTTP Request: Acts as the communication channel.
3.	Server (Flask Music Generation Service): Processes the request and responds.
   
Sequence of Events:
1.	Client prepares the HTTP GET request:
The client prepares an HTTP GET request with parameters (num_notes, scale, instrument).
2.	HTTP GET Request:
The HTTP request is sent to the server. This is the main "pipe" through which data flows.
3.	Server receives the request:
The server's /generate endpoint processes the incoming GET request.
4.	Server processes the request:
	The server validates the parameters, generates the music, converts it, and prepares the MP3 file.
5.	Server sends the response:
	The server responds with a JSON object containing the URL of the generated MP3 file.
6.	Client receives the response:
	The client parses the JSON response and extracts the URL of the MP3 file.
7.	Client requests the MP3 file:
	The client sends a new HTTP GET request to download the MP3 file using the received URL.
8.	Server sends the MP3 file:
	The server responds to the file download request by sending the MP3 file.
9.	Client optionally plays the MP3 file:
	The client may play the MP3 file using appropriate software or a web player.
