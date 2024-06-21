# Plex Managarr
A WebUI application for managing image collections for Plex Media Server libraries. Right now it is in early 
stages and acts as a companion tool for [Kometa](https://kometa.wiki).

## How does it work?
The app is currently in very early proof of concept stage. You can run `main.py` and provide a 
[ThePosterDB](https://theposterdb.com) or [Mediux](https://mediux.pro) URL to generate a `metadata.yml` file for a 
TV show or movie collection (and accompanying `collections.yml` file for movie collections). These files are used 
by [Kometa](https://kometa.wiki) when processing and importing images and metadata into Plex.

Long term, the plan for this project is to build out a WebUI that can manage metadata and images for your Plex 
Media Server library in realtime via a webserver that takes update commands from the frontend and processes 
those updates through Kometa.
