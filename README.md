# About
This tool automates the creation of audio samples and a html tracklist in which one can listen to those samples.

It was initially built for a music wordpress webshop.

An album can have one or multiple CDs.
For each CD it will generate audio samples and a text file with the html code to show a tracklist.
After uploading the samples as simple media objects to a wordpress website, the html code can be inserted in the product's page.
The html code will have a table with the track names and a shortcode for each sample audio file.

# How to install
In order to be able to create the audio samples, the project uses the FFmpeg framework (https://ffmpeg.org/).<br>
You must have ffmpeg and ffprobe in the same directory as Main.py.

# How to configure
All you need to do is set the options.json file, explained below:

```
{
    "cds_path": "path\\to\\mp3-album-files", 
    "sample_duration": 30,
    "fade_out_duration": 3,
    "upload_url": "https://website.com/wp-content/uploads/",
    "plugin_shortcode": "[your-favorite-audio-player-plugin fileurl='%s']"
}
```
## cds_path
The path to your mp3 files must be organized like in the example below:

    mp3-album-files
    ├── ...
    ├── album1
    │   ├── CD1
    │   │   ├── track1.mp3
    │   │   ├── track2.mp3
    │   │   └── track3.mp3
    │   └── CD2
    │       ├── track1.mp3
    │       ├── track2.mp3
    │       └── track3.mp3
    └── album2
        ├── track1.mp3 
        ├── track2.mp3
        └── track3.mp3

## sample_duration
The total duration of the sample in seconds.

## fade_out_duration
The fade out duration in seconds, at the end of the audio sample. 
This effect will start the given seconds before the end of the sample.

## upload_url
The uploaded file url beginning.<br>
This tool will append the year and month part to this url as well.<br>
Generated url example:<br>
`https://website.com/wp-content/uploads/2024/11/AlbumName-Sample-Track1.mp3
`

## plugin_shortcode
This shortcode must include a '%s' which will fit the uploaded file url.<br>


# How it works
The generated audio samples will be created in a folder next to the album or cd's folder with the suffix '_samples'.<br>
The generated html tracklist code will be created next to the album or cd's folder with the suffix '_samples_tracklist'.

## Command-line
Set your options.json file.<br>
Then run:<br>
`python Main.py
`

## Graphical User Interface
Set your options.json file.<br>
Then run:<br>
`python Main.py -g
`
Select the root directory of your mp3 files and then start.

# To-do list
* set options via GUI
* fully customize tracklist html generation



