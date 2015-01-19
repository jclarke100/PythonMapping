"""
Script to import all GPX tracks from a folder into a line feature class
in a file geodatabase. New line feature for each GPX file.

Generate linear density map of those lines to show where most tracks go.

Parameters:
    1 - Path to source folder of GPX files
    2 - Target feature class to which data is appended
    3 - Option to truncate target feature class before data load

TODO:
Could do with some error handling, create FGDB if it doesn't exist etc
Also doesn't carry any attributes through from GPX, date/time would be good
"""

import sys, arcpy, os

def main():

    print "Script started"

    gpxFolder = sys.argv[1]
    target = sys.argv[2]
    doTruncate = sys.argv[3]
    ##gpxFolder = r"c:\stuff\python\gpx"
    ##target = r"c:\stuff\python\GPS.gdb\Tracks_1"
    ##doTruncate = False

    if not os.path.isdir(gpxFolder):
        print "No source folder found: " + gpxFolder
        sys.exit(1)

    if not arcpy.Exists(target):
        print "No target found: " + target
        sys.exit(1)

    if doTruncate:
        try:
            print "Truncating %s..." % target
            arcpy.TruncateTable_management(target)
        except:
            print "Target not found or can't truncate"
            sys.exit()

    for f in os.listdir(gpxFolder):
        print "Processing file %s" % f

        print "\tconvert to points in_mem"
        arcpy.GPXtoFeatures_conversion(gpxFolder + "\\" + f, "in_memory\\track")

        print "\tconvert in_memory points to lines"
        arcpy.PointsToLine_management("in_memory\\track", "in_memory\\track_line")

        print "\tadd the new in_mem line to target feature class"
        arcpy.AddMessage(f)
        print("\t" + f)
        arcpy.Append_management("in_memory\\track_line", target, "NO_TEST")

        # Line density stuff todo - needs Spatial Analyst
        # lineDensity = LineDensity(target, "", 10, 20)

if __name__ == '__main__':
    main()
