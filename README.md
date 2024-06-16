# YouTube to Spotify Playlist Converter

## Overview
This web application provides a seamless interface for users to convert YouTube playlists into Spotify playlists. By simply entering the ID of a YouTube playlist, users can generate a corresponding Spotify playlist with ease.

## Features

### Login
- Secure user authentication to access personal Spotify details.

### Home
- A dashboard that displays user-specific options and features after login.

### Show Playlists
- View a list of existing Spotify playlists associated with the user's account.

### Add Playlist
- Interface to search for YouTube playlists using a playlist ID.
- Displays detailed information about YouTube videos in the playlist.
- Shows Spotify search results corresponding to the YouTube videos to ensure accurate track matching.

## How to Use

### Prerequisites
- Ensure you have accounts on both YouTube and Spotify.
- Obtain necessary API keys from YouTube Data API and Spotify Web API.

### Installation
1. Clone the repository: `git clone https://github.com/AsafMesi/youtube2spotify`
2. Navigate to the project directory and install dependencies: cd youtube-to-spotify, npm install, pip install dotenv

### Running the Application
1. Start the backend: `python3 server.py`
2. Start the frontend: `npm start`
3. Open your web browser and go to `http://localhost:5000` to access the application.

### Adding a YouTube Playlist
1. From the Home page, navigate to the 'Add Playlist' section.
2. Enter the ID of the YouTube playlist you wish to convert.
3. Review the video details and corresponding Spotify tracks that appear.
4. Confirm to create a Spotify playlist, which will then be saved to your Spotify account.

## Configuration
- Configure your API keys and user authentication details in your own `google.env` and `spotify.env` files (ensure those files are secure and not exposed publicly).

## Security
- All user data is handled confidentially. Authentication is managed through secure OAuth protocols for both YouTube and Spotify APIs.

## Contributing
Contributions to this project are welcome! Please fork the repository and submit pull requests with your proposed changes.

## Diagram
![image](https://github.com/AsafMesi/youtube2spotify/assets/92261832/6489af64-1404-47dc-a24e-46be53604e15)

## Acknowledgements
- Thanks to YouTube Data API and Spotify Web API for the services used in this project.



