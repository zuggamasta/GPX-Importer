# GPX-Importer
A python GPX importer with multi file support for blender.

![Large set of *.GPX rendered at once](_examples/preview.jpg)

> [!note]
> 1. This importer has currently only been tested with *.GPX files exported from Apple Health
> 2. This importer currently just plots latitude and longitude in Degrees as X and Y coordinates.



## Usage
Blender 4.0.X is recommended.
1. Download the [latest release](https://github.com/zuggamasta/GPX-Importer/releases/tag/v0.1.1-alpha) of this addon from github
2. Install the gpx_blender.zip file as addon
3. Make sure the Addon is enabled
4. Import your files just as other formats via "File > Import > GPS Exchange Format (.gpx)"
5. Each GPX file will be imported in it's own collection

> [!tip]
> There are two options available on import, plotting elevation data can be messy so it is not enabled by default.
> - [x] Create Edges
> - [ ] Plot Elevation

Make sure to check the objects location in space after import. Imported meshes might be far of screen.
