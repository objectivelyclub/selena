import os
import argparse
from PIL import Image, ImageSequence

argparser = argparse.ArgumentParser() 
argparser.add_argument('input_path', nargs='+', help="The path of the GIF files that should be displayed on the page.")
argparser.add_argument('js_file', help="The path to the javascript file to modify.")
args = argparser.parse_args()

def getGIFDuration(gifPath):
    """
    Returns the duration, in ms, of the given GIF.
    """
    name, extension = os.path.splitext(gifPath)
    if extension == '.gif':
        im = Image.open(path)
        durations = []

        for frame in ImageSequence.Iterator(im):
            try:
                durations.append(frame.info['duration'])
            except KeyError:
                # Ignore if there was no duration, we will not count that frame.
                pass

        total_duration = sum(durations)
        return total_duration

if __name__ == "__main__":
    paths = []
    durations = []
    for path in args.input_path:
        filename = os.path.basename(path)
        webpath = os.path.join("images", filename)
        paths.append(webpath)
        durations.append(getGIFDuration(path))

    lines = []
    lines.append("var imageArray = %s;\n" % (paths.__str__()))
    lines.append("var imageDurationArray = %s;\n" % (durations.__str__()))

    lines.append("""
$(document).ready(function () {
    var currentIndex = 0;

    var previous = function () {
        $("#main-display-image").hide();
        if (currentIndex == 0) {
            currentIndex = imageArray.length - 1;
        } else {
            currentIndex--;
        }
        $("#main-display-caption").text(imageArray[currentIndex]);
    };

    var next = function () {
        $("#main-display-image").hide();
        if (currentIndex == imageArray.length - 1) {
            currentIndex = 0;
        } else {
            currentIndex++;
        }
        $("#main-display-caption").text(imageArray[currentIndex]);
    };

    var play = function () {
        $("#main-display-image").attr("src", imageArray[currentIndex]);
        $("#main-display-image").show();
        setTimeout(next, imageDurationArray[currentIndex]);
    };

    $("#prev-button").bind("click", previous);
    $("#next-button").bind("click", next);
    $("#play-button").bind("click", play);

    var checkKey = function (e) {
        switch (e.which) {
            case 189: previous(); break; // dash
            case 187: next(); break; // equals
            case 48: play(); break; // 0
        }
    }

    $("body").on("keydown", checkKey); // make sure this works on firefox

});
""")
    with open(args.js_file, 'w+') as fout:
        for line in lines:
            fout.write(line)