# Spotify Playlist Analyzer

The **Spotify Playlist Analyzer** is a web application that allows users to analyze and gain insights into their Spotify playlists. With this tool, you can explore the artists and track popularity within your playlists, sort and filter your playlists based on various criteria, and discover new trends in your music library.

## Features

- **Login with Spotify:** Log in to your Spotify account to access your playlists and analyze them.
- **View Playlists:** See a list of all your Spotify playlists and click on them for detailed analysis.
- **Analyze Playlists:** Analyze the artists and track popularity in your playlists.
- **Sort and Filter:** Sort your playlists by artist count or track popularity, and filter them by various criteria.
- **Discover Trends:** Gain insights into your music preferences and discover new trends within your playlists.

## How to Use

1. **Login with Spotify or URL:** Click on the "Login with Spotify" button to log in to your Spotify account. If you don't wish to log in with Spotify, you can click "Analyze with Spotify URL" and paste a URL link into the search bar.
2. **Select a Playlist:** After logging in, you will see a list of your playlists. Click on a playlist to analyze it.
3. **Analyze the Playlist:** Once you've selected a playlist, you can view details such as artist count and track popularity. You can also sort the data based on your preferences.
4. **Explore Insights:** Explore the insights about your music library and make informed decisions about your playlists.

## Technologies Used

- Flask: A Python web framework for building the backend of the application.
- Spotify API: Used to access user playlists and retrieve playlist details.
- Spotipy: A Python library for interacting with the Spotify Web API.

## Setup Instructions
To set up this project locally, follow these steps:

1. Clone the repository to your local machine.
2. Install the required Python packages using pip install -r requirements.txt.
3. Create a Spotify Developer account and obtain your client ID and client secret.
4. Create a .env file in the project directory and add the following variables:
`SPOTIPY_CLIENT_ID=your_client_id`
`SPOTIPY_CLIENT_SECRET=your_client_secret`
`SPOTIPY_REDIRECT_URI=http://localhost:5000/redirect`

Replace `your_client_id` and `your_client_secret` with your actual Spotify developer credentials.
5. Run the Flask application using `python3 app.py` or `flask run`.
6. Access the application in your web browser at `http://localhost:5000`.

## License
This project is licensed under the **MIT License**.