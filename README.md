This script parses the folder name and uses cinegoer module to search imdb for possible titles and appends the foldername with it.
it is verbose and asks user for details.

For example : \
TEST folder has a Folder named \
`Lawrence Of Arabia (1962) [BluRay] [1080p] [YTS.AM]` \
and finally rename it to \
`Lawrence Of Arabia (1962) [BluRay] [1080p] [YTS.AM] [imdbid-tt0056172]`

it will strip out details in brackets () []

run script as : \
`python mov_renamer.py "H:\Media\TEST"`

#### New commands added

`python .\mov_renamer.py list-metadata "D:\JELLYFIN_RENAME"`
`python .\mov_renamer.py wipe-metadata-soft "D:\JELLYFIN_RENAME" txt,jpg`
`python .\mov_renamer.py wipe-metadata-hard "D:\JELLYFIN_RENAME" txt,jpg`

Search with name 'Lawrence Of Arabia' ? (y/n): y \
Folder Name - :Lawrence Of Arabia (1962) [BluRay] [1080p] [YTS.AM]:, Searching with :Lawrence Of Arabia: \
Search Results found 20 \
Checking 1 - :Lawrence of Arabia: \
opening - https://www.imdb.com/title/tt0056172/ \
Is this the correct one ? ( rename to :Lawrence Of Arabia (1962) [BluRay] [1080p] [YTS.AM] [imdbid-tt0056172]: (y/n): y
