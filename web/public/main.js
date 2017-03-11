var imageArray = ["images/Bach - Jesu, Joy of Man's Desiring.gif", 'images/Britney Spears - Toxic.gif', 'images/Chopin - Mazurka Op6 No1.gif', 'images/Coldplay - A Sky Full of Stars.gif', 'images/Cutie Honey - Opening.gif', 'images/Evangelion - Fly Me To the Moon.gif', 'images/Paradise - Coldplay.gif', "images/Star Wars - Rey's Theme.gif", 'images/Tetris - Theme A.gif', 'images/Utena - Revolution.gif'];
var imageDurationArray = [297500, 189700, 177800, 266700, 82600, 202300, 238000, 154700, 46900, 86100];

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
