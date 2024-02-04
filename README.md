# GPX-Importer
A python GPX importer with multi file support for blender.

![Large set of *.GPX rendered at once](_examples/preview.jpg)

> [!note]
> 2. This importer has currently only been tested with *.GPX files exported from Apple Health


## Usage
Blender 4.0.X is reccomended 
1. Open Blender and move into the Scripting viewport
2. Install the gpx_blender.zip file as addon
3. Make sure the Addon is enabled
4. Import your files just as other formats via "File > Import > GPS Exchange Format (.gpx)"
4. Each GPX file will be imported in it's own collection

There are two options available on import, plotting elevation data can be messy so it is not enabled by default.
- [x] Create Edges
- [ ] Plot Elevation

> [!note]
> This importer just plots latitude and longitude in Degrees as X and Y coordinates as Blender Units


