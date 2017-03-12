var imageArray = ["Bach - Jesu, Joy of Man's Desiring.gif", 'Britney Spears - Toxic.gif', 'Chopin - Mazurka Op6 No1.gif', 'Coldplay - A Sky Full of Stars.gif', 'Coldplay - Paradise.gif', 'Crystallize.gif', 'Cutie Honey - Opening.gif', 'Evangelion - Fly Me To the Moon.gif', 'Game_of_Thrones.gif', 'Halo_One_Final_Effort_Complex.gif', 'Halo_One_Final_Effort.gif', 'Merry_Christmas_Mr_Lawrence.gif', 'Oblivion.gif', "Star Wars - Rey's Theme.gif", 'Sweetwater_Train_Theme.gif', 'Tetris - Theme A.gif', 'The_Shire.gif', 'Utena - Revolution.gif', 'Westworld_MainTitles_HalcyonMusic.gif'];
var imageDurationArray = [297500, 189700, 177800, 266700, 238000, 248500, 82600, 202300, 79100, 168000, 141400, 280000, 333200, 154700, 49700, 46900, 128800, 86100, 84700];

$(document).ready(function () {
    window.timeoutHandle = setTimeout(next, 5000);
    var currentIndex = 0;
    var nextIndex = 1;

    var previous = function () {
        $("#main-display-image").hide();
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
        $("#main-display-image").hide();
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
        $("#main-display-image").show();
        clearTimeout(timeoutHandle);
        window.timeoutHandle = setTimeout(next, imageDurationArray[currentIndex]);
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
    window.timeoutHandle = setTimeout(next, 5000);

});
