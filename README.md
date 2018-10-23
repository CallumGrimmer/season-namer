# season-namer

This is a python3 script that takes a folder path and the season link on imdb and renames video files in the folder. The resulting syntax will be:

    n_[episode_name] 
   
For example the Simpsons season 5, episode 1 will go from:

    s05e01 --> 1_Homer's Barbershop Quartet
    
The episode numbering is so that the episodes won't go out of order if the folder is sorted alphabetically.   
 
## Usage

To use this tool, navigate to IMDB and find the season page you are looking for. It will likely look similar to https://www.imdb.com/title/tt0096697/episodes?season=5

Then copy the url and run the renamer tool like so:

    python3 renamer.py <path-to-folder> <imdb-link>
    
The folder path can be relative or absolute. 

Any feedback is welcome!
