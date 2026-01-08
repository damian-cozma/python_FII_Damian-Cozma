# SongStorage

## Project Description

SongStorage is a CLI (Command Line Interface) application for managing a local audio file library.  
The application provides organized storage of audio files inside a dedicated folder, along with persistent metadata stored in an SQLite database.

The main features of the application are:

- adding and deleting songs  
- selective metadata editing  
- searching using multiple criteria combined with logical AND  
- creating playlists (savelists)  
- audio playback using a third-party library  

---

## Required Installations

### Requirements

- Python 3.10 or newer  
- pip  

### Python Dependencies

- `pygame` (used for audio playback)

Install dependencies using:

```bash
pip install pygame
```

## How to Run the Application

The application is executed exclusively as a Python module, from the project root directory:

```bash
python -m cli.main <command> [options]
```
