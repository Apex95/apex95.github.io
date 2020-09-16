---
layout: post
title:  "Build Tesseract 5 in Conda Environment"
date:   2020-09-16 00:45:05 +0300
tags: tesseract conda
image: /imgs/thumbnails/tesseract-5-conda.png
---

Here's a short guide to building **Tesseract 5** from source (master branch on GitHub). 

I'm writing this mainly because conda offers as packages only versions of Tesseract up to 4.1.1 -- at least at this moment. The other reason is that the cluster I'm compiling Tesseract on is running a CentOS 7 and permitting only inside-environment changes so I can't install packages with yum.

##### In this guide I'm using **gcc/g++** version **6.2.0**; it is recommended to use recent versions when compiling Tesseract 5. For example, the build fails with gcc/g++ 4.8.5.

## Building Steps

1. Create your **conda environment** and activate it:
```bash
conda create --name tess-build 
conda activate tess-build
```

2. Install the following dependencies. You'll need at least leptonica 1.74 for this to work - I'm using 1.78.0.
```bash
conda install -c conda-forge automake
conda install -c conda-forge libtool
conda install -c conda-forge pkgconfig
conda install -c conda-forge leptonica
```

3. Clone the latest Tesseract version from the master branch and navigate into the directory:
```bash
git clone https://github.com/tesseract-ocr/tesseract.git
cd tesseract
```

4. Run the following scripts to prepare the building process
```
./autogen.sh
./configure
```

5. Conda might not include the path to its libraries inside the `LD_LIBRARY_PATH` environment variable. I had to include it manually otherwise the build fails during linking:
```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/.conda/envs/tess-build/lib
```

6. Run the makefile:
```bash
make
```

7. Set the `TESSDATA_PREFIX` environment variable in order to inform Tesseract where to look for language packs; also download the **eng** (default) language pack into **tessdata**
```bash
export TESSDATA_PREFIX=$HOME/tesseract/tessdata
wget https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata -P tessdata/
```

8. See if it works:
```
(tess-build) [dan.sporici@hpsl-wn02 tesseract]$ ./tesseract -v
tesseract 5.0.0-alpha-781-gb19e3
leptonica-1.78.0
libgif 5.2.1 : libjpeg 9d : libpng 1.6.37 : libtiff 4.1.0 : zlib 1.2.11 : libwebp 1.0.2 : libopenjp2 2.3.1
Found AVX
Found SSE
Found OpenMP 201511
```
```
(tess-build) [dan.sporici@hpsl-wn02 tesseract]$ ./tesseract --list-langs
List of available languages (1):
eng
```


## Possible Leptonica Linking Issue

```
/usr/bin/ld: warning: libpng16.so.16, needed by /.conda/envs/tess-build/lib/liblept.so, not found (try using -rpath or -rpath-link)
/usr/bin/ld: warning: libjpeg.so.9, needed by /.conda/envs/tess-build/lib/liblept.so, not found (try using -rpath or -rpath-link)
/usr/bin/ld: warning: libgif.so.7, needed by /.conda/envs/tess-build/lib/liblept.so, not found (try using -rpath or -rpath-link)
/usr/bin/ld: warning: libwebp.so.7, needed by /.conda/envs/tess-build/lib/liblept.so, not found (try using -rpath or -rpath-link)
/.conda/envs/tess-build/lib/liblept.so: undefined reference to `png_create_read_struct@PNG16_0'
/.conda/envs/tess-build/lib/liblept.so: undefined reference to `DGifOpen'
/.conda/envs/tess-build/lib/liblept.so: undefined reference to `png_get_PLTE@PNG16_0'
/.conda/envs/tess-build/lib/liblept.so: undefined reference to `jpeg_std_error@LIBJPEG_9.0' 
/.conda/envs/tess-build/lib/liblept.so: undefined reference to `png_write_image@PNG16_0'
/.conda/envs/tess-build/lib/liblept.so: undefined reference to `EGifPutScreenDesc'
/.conda/envs/tess-build/lib/liblept.so: undefined reference to `EGifPutComment'
/.conda/envs/tess-build/lib/liblept.so: undefined reference to `WebPEncodeRGBA'
[...]
/.conda/envs/tess-build/lib/liblept.so: undefined reference to `png_init_io@PNG16_0'
collect2: error: ld returned 1 exit status
make[2]: *** [tesseract] Error 1
make[2]: Leaving directory `/tesseract'
make[1]: *** [all-recursive] Error 1
make[1]: Leaving directory `/tesseract'
make: *** [all] Error 2
```

This happens because the libraries in cause (**libpng16.so**, **libjpeg.so**, **libgif.so**, **libwebp.so**) are not found in the directories included in `LD_LIBRARY_PATH`.
If step 5 doesn't work (although it should), you might be able to get around this by modifying the **Makefile** and adding the libraries yourself after `-llept`:
```make
LEPTONICA_LIBS = -L/.conda/envs/tess-build/lib -llept -lz -lpng16 -ljpeg -lgif -lwebp
```

If you follow this approach, you need to copy the libraries to `tesseract/.libs` otherwise you'll get:
```
(tess-build) [dan.sporici@hpsl-wn02 tesseract]$ ./tesseract
/tesseract/.libs/lt-tesseract: error while loading shared libraries: liblept.so.5: cannot open shared object file: No such file or directory
/tesseract/.libs/lt-tesseract: error while loading shared libraries: libpng16.so.16: cannot open shared object file: No such file or directory
/tesseract/.libs/lt-tesseract: error while loading shared libraries: libjpeg.so.9: cannot open shared object file: No such file or directory
/tesseract/.libs/lt-tesseract: error while loading shared libraries: libgif.so.7: cannot open shared object file: No such file or directory 
```


That all; I hope this helps.
