This program is intended to copy FLAC music libraries into another directory using a defined structure.

Copies all files within a source directory recursively to another directory and (re)names directories and filenames according to a specified format taken from the files Metadata.
For each folder in source an albumart image is exported from a FLAC file if possible.

```
flacmover.py -i SRCDIR -o DESTDIR -f FORMATSTRING 
	-i SRCDIR   source root of files; defaults to current dir 
	-o DESTDIR  destination root of the renamed dirs and files 
	-f FORMATSTRING any format of directory file structure 
			with / as dir delimiter and %variable% for any variable 
			found in FLAC file tags as used by mutagen. 
			ex.: 
				%albumartist%/%albumartist%.%originalyear%.%album%/%discnumber%.%tracknumber%.%artist%.%title%
```
