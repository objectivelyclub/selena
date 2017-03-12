var imageArray = ["Bach - Jesu, Joy of Man's Desiring.gif", 'Britney Spears - Toxic.gif', 'Chopin - Mazurka Op6 No1.gif', 'Coldplay - A Sky Full of Stars.gif', 'Cutie Honey - Opening.gif', 'Evangelion - Fly Me To the Moon.gif', 'Paradise - Coldplay.gif', "Star Wars - Rey's Theme.gif", 'Tetris - Theme A.gif', 'Utena - Revolution.gif'];
var imageDurationArray = [297500, 189700, 177800, 266700, 82600, 202300, 238000, 154700, 46900, 86100];

$(document).ready(function () {
    var currentIndex = 0;
    var nextIndex = 1;

    var previous = function () {
        if (currentIndex == 0) {
            currentIndex = imageArray.length - 1;
        } else {
            currentIndex--;
        }
        nextIndex = (currentIndex + 1) % imageArray.length;
        $("#track-name").text(imageArray[currentIndex]);
        $("#next-track-name").text(imageArray[nextIndex]);
        play();
    };

    var next = function () {
        if (currentIndex == imageArray.length - 1) {
            currentIndex = 0;
        } else {
            currentIndex++;
        }
        nextIndex = (currentIndex + 1) % imageArray.length;
        $("#track-name").text(imageArray[currentIndex]);
        $("#next-track-name").text(imageArray[nextIndex]);
        play();
    };

    var play = function () {
        $("#main-display-image").attr("src", "images/" + imageArray[currentIndex]);
        setTimeout(next, imageDurationArray[currentIndex]);
    };

    $("#prev-button").bind("click", previous);
    $("#next-button").bind("click", next);

    var checkKey = function (e) {
        switch (e.which) {
            case 189: previous(); break; // dash
            case 187: next(); break; // equals
            case 48: play(); break; // 0
        }
    }

    $("body").on("keydown", checkKey); // make sure this works on firefox

    setTimeout(next, 5000);

});
