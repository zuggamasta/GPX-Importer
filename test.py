from xml.dom.minidom import parse

filepath = "./_examples/gpx_apple_health.gpx"

xml = parse(filepath)
trkpts = xml.getElementsByTagName("trkpt")

try:
    print("running read_gpx... printing *.gpx metadata")
    global waypoints
    waypoints = []

    for trkpt in trkpts:       
        waypoint = (float(trkpt.attributes["lon"].value), float(trkpt.attributes["lat"].value), 0)
        waypoints.append(waypoint)
 
    print(waypoints)

except:
    print("import failed")