# LyricGenerator

Every musical artist has a unique style that permeates through their music. The content of their songs often evolves over the course of their career but the original voice is always present. Our goal for this project is to dive into the heart of the artist and see if we are able to bring this voice out. The concrete task we are going to achieve is given a seed set of words, can we construct a new and original song in an artist’s style.

### How to run it

If you have precomputed a list of important words for this artist 
```
python Generator.py "Add first line here!" path_to_folder_with_lyrics path_to_precomputed_list
```

If you have NOT precomputed a list of important words for the artist, no worries we will do it for you but it may take a while as we use TextRank and it is quite slow
```
python Generator.py "Add first line here!" path_to_folder_with_lyrics NONE
```

Examples:
```
python Generator.py "Hey Jude don't make it bad" BeatlesLyrics/ textRankListBeatles.txt

python Generator.py "Hey Hey momma said the way you move" BobMarleyLyrics/ NONE
```

The lyrics files themselves should be formatted as such:
```
name_of_song

line 1
line 2
line 3
...
...
...
last line
```

### Credits

Based on [Text Rank](https://gist.github.com/voidfiles/1646117)
From this [paper](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf)
External dependencies: nltk, numpy, networkx
