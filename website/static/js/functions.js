let volume = false;
var trailer = document.getElementById("trailer");

function toggleVolume(e) {
    if (volume == false) {
        volume = true;
        e.src = "../static/icons/volume.png";
        trailer.muted = false;
    }
    else {
        volume = false;
        e.src = "../static/icons/mute.png";
        trailer.muted = true;
    }
}