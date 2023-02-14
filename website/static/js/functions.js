let volume = false;
var trailer = document.getElementById("trailer");

function toggleVolume(e) {
    if (volume == false) {
        volume = true;
        e.src = "../static/volume-icons/volume.png";
        trailer.muted = false;
    }
    else {
        volume = false;
        e.src = "../static/volume-icons/mute.png";
        trailer.muted = true;
    }
}

document.addEventListener("click", e => {
    let handle
    if (e.target.matches(".handle")) {
        handle = e.target
    } else {
        handle = e.target.closest(".handle")
    }
    if (handle != null) {
        onHandleClick(handle)
    }
})

function onHandleClick(handle) {
    const slider = handle.closest(".slider-container").querySelector(".slider")
    const sliderIndex = parseInt(getComputedStyle(slider).getPropertyValue("--slider-index"))
    if (sliderIndex == 0) {
    } else {
        handle.style.setProperty("--display-handle", "display");
    }
    if (handle.classList.contains("left-handle")) {
        slider.style.setProperty("--slider-index", sliderIndex - 1)
    }
    if (handle.classList.contains("right-handle")) {
        slider.style.setProperty("--slider-index", sliderIndex + 1)
    }
}

window.addEventListener("resize", (e) => {
    // recalculate progress bar
})

document.querySelectorAll(".slider-progress-bar").forEach(calculateProgressBar)

function calculateProgressBar(progressBar) {
    progressBar.innerHTML = ""
    const slider = progressBar.closest(".slider-row").querySelector(".slider")
    const itemCount = slider.children.length
    const itemsPerScreen = parseInt(getComputedStyle(slider).getPropertyValue("--items-per-screen"))
    const sliderIndex = parseInt(getComputedStyle(slider).getPropertyValue("--slider-index"))
    const progressBarItemCount = Math.ceil(itemCount / itemsPerScreen)
    for (let i = 0; i < progressBarItemCount; i++) {
        const barItem = document.createElement("div")
        barItem.classList.add("slider-progress-item")
        if (i === sliderIndex) {
            barItem.classList.add("active")
        }
        progressBar.append(barItem)
    }
}