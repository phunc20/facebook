## Installation of python packages
- `pip install geopy`
- `pip install rtree`
  - You might fail to install. See below
  - [The machine must have `spatialindex` first](https://github.com/Toblerity/rtree/issues/88). After all, as described in the package's documentation, **"Rtree is a ctypes Python wrapper of `libspatialindex`"**
  - For users of Arch Linux: `pacman -S spatialindex`. (Other OSs/distros should be able to follow a similar step.) Once `spatialindex` installed, try again `pip install rtree`

