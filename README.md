# pixelcrush

> Crush those pixels! A "place" clone that uses proof of work.

This project is an online shared canvas where you can draw individual pixels.

It is inspired by various other projects:
- Reddit's [r/place](https://www.reddit.com/r/place/), which is no longer active. The intended rate-limiting of 6 seconds or something was quickly circumvented.
- A simplistic [clone by @rbxb](https://github.com/rbxb/place), which is [still active](https://pl.g7kk.com/ace)), and allows up to 8 pixels per second (or 0.125 seconds per pixel).
- And of course [pixelflut](https://github.com/defnull/pixelflut), which embraces flooding and botting. Thus, it usually only runs "locally" during a party or congress. [Seizure warning.](https://media.ccc.de/v/pixelflut-eh15).

This project approaches the topic of ratelimiting differently: Proof of work. If you want to set a
pixel, you have to provide a nonce that results in a better (here: higher) hash. Initially, all
pixels have a rather low diffculty, and finding a "better" nonce is easy. However, as time goes on
and the pixel is overwritten again and again, and thus the difficulty goes up and up, it becomes
harder to find a better nonce.

TODO: Play along with the [fancy web interface!](example.com)

TODO: The administrator can easily interfere and ease up or overwrite certain regions.

## Table of Contents

- [Usage](#usage)
- [TODOs](#todos)
- [NOTDOs](#notdos)
- [Contribute](#contribute)

## Usage

### Getting started

Usage: `./example/putpixel.py X Y R G B`

Simple, isn't it? This way, you can paint individual pixels. It's written in python, and not particularly convenient, clever or fast. However, it demonstrates how something like this can be used.

Here's how an example run looks like:

```
$ time ./putpixel.py 100 100 255 0 0
Trying to beat hash b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' for payload b'd\x00d\x00\xff\x00\x00' ...
Submitting (100, 100, 255, 0, 0) with hash b'\xa6\x84kb\x04\xdao\xe1\x17\xa8\xa9\xa1\xc3\x84\x1a\xc0x\\\x9c\x81\xeat\xeb\x18\xafz; \xa6\xdb\x11.' ...
Trying to beat hash b'\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' for payload b'd\x00d\x00\xff\x00\x00' ...
  100 unsuccessful attempts
Submitting (100, 100, 255, 0, 0) with hash b'\xff\x8cPt\\\xdb@\x05\x19\xfe\x00D\x1bpw\x18Ol\n\xad\xbf-\xdb\xfd\xd7Pc\x10\xb1\xc96O' ...

real	0m0,177s
user	0m0,152s
sys	0m0,021s
```

### Writing your own

The API is as simple as I could possibly make it:

Just POST some bytes to `/post`. Which bytes? Well, X, Y, R, G, B, nonce, and hash:
- X and Y are 2 bytes each, little-endian, and must be less than 1024 (the size of the image)
- R, G, B: Single bytes
- Nonce: Any 16 bytes that you like.
- Hash: The SHA-256 of the previous 23 bytes. (32 bytes)

The server will respond with any of:
- HTTP 400, wrong number of bytes
- HTTP 400, bad coordinates
- HTTP 400, bad hash
- HTTP 409, "conflict": The server provides the 32 bytes of the "better" hash, so you can immediately use it to find better candidates. Better luck next time.
- HTTP 200: Game on! :D

Come over to [TODO: PUBLISH MY SERVER] to try it out! :D

### Other API

Other endpoints are:
- `GET /place.png`: Returns a nice PNG of the current RGB data. Isn't it nice? :D
- `POST /row_hardness`: You provide two bytes (y-coordinate), and the server responds with 32K worth of hashes; one for each pixel in the row. Feel free to use this to optimize your hashing efforts! This way you don't have to make 1024*1024 calls to `/post`
- `POST /save`: Can be used by the administrator to save the current state (RGB data + hardness) to a new file.

Future endpoints:
- `POST /overwrite_pixel`: Can be used by the administrator to forcibly overwrite a single pixel. This is useful to erase nasty stuff.

## TODOs

* Some web interface to interact with it
* Maybe websockets to see updates in real-time?
* That administrator command

## NOTDOs

Here are some things this project will definitely not support:
* Anything "blockchain"y
* Any tracking

## Contribute

Feel free to dive in! [Open an issue](https://github.com/BenWiederhake/pixelcrush/issues/new) or submit PRs.
