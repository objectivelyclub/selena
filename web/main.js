var imageArray = ["Bach - Jesu, Joy of Man's Desiring.gif", 'Britney Spears - Toxic.gif', 'Chopin - Mazurka Op6 No1.gif', 'Coldplay - A Sky Full of Stars.gif', 'Coldplay - Paradise.gif', 'Crystallize.gif', 'Cutie Honey - Opening.gif', 'Game_of_Thrones.gif', 'Halo_One_Final_Effort_Complex.gif', 'Halo_One_Final_Effort.gif', 'Oblivion.gif', "Star Wars - Rey's Theme.gif", 'Sweetwater_Train_Theme.gif', 'Tetris - Theme A.gif', 'The_Shire.gif', 'Utena - Hikarisasu Niwa - Sunlit Garden.gif', 'Westworld_MainTitles_HalcyonMusic.gif'];
var imageDurationArray = [186540, 150530, 159350, 194750, 203180, 232990, 60510, 72000, 148470, 105730, 267440, 106730, 34590, 54000, 116890, 71650, 69940];

$(document).ready(function () {
    window.timeoutHandle = setTimeout(next, 5000);
    var currentIndex = 0;
    var nextIndex = 1;

    var previous = function () {
        $("#main-display-image").hide();
        $("#track-name").text("Loading...");
        if (currentIndex == 0) {
            currentIndex = imageArray.length - 1;
        } else {
            currentIndex--;
        }
        nextIndex = (currentIndex + 1) % imageArray.length;
        play();
    };

    var next = function () {
        $("#main-display-image").hide();
        $("#track-name").text("Loading...");
        if (currentIndex == imageArray.length - 1) {
            currentIndex = 0;
        } else {
            currentIndex++;
        }
        nextIndex = (currentIndex + 1) % imageArray.length;
        play();
    };

    var play = function () {
        var loadingImage = new Image();
        loadingImage.onload = function() {
            $("#main-display-image").attr("src", this.src);
            $("#main-display-image").show();

            clearTimeout(timeoutHandle);
            window.timeoutHandle = setTimeout(next, imageDurationArray[currentIndex]);

            $("#track-name").text(imageArray[currentIndex]);
            $("#next-track-name").text(imageArray[nextIndex]);
        };
        loadingImage.src = "images/" + imageArray[currentIndex];
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