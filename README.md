This embeds text inside images without changing the image too much.

It consumes jpg images and outputs png.

Uses 8 pixels per 3 chars.

Example:
```
$ python text_in_image.py -e ~/Desktop/No_secret.jpg -o ~/Desktop/Secret.png -t "I am secretly embedded"
$ python text_in_image.py -d ~/Desktop/Secret.png 
I am secretly embedded
```

```
$ python text_in_image.py -h
usage: text_in_image.py [-h] (--encrypt | --decrypt) [--text TEXT]
                        [--output_file OUTPUT_FILE]
                        image_path

Hides text inside image.

positional arguments:
  image_path            Image to hide text in

optional arguments:
  -h, --help            show this help message and exit
  --encrypt, -e
  --decrypt, -d
  --text TEXT, -t TEXT  Text to hide
  --output_file OUTPUT_FILE, -o OUTPUT_FILE
                        Name of output file
```