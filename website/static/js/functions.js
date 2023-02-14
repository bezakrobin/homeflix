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
    const progressBar = handle.closest(".slider-row").querySelector(".slider-progress-bar")
    const slider = handle.closest(".slider-container").querySelector(".slider")
    const sliderIndex = parseInt(getComputedStyle(slider).getPropertyValue("--slider-index"))
    const progressBarItemCount = progressBar.children.length
    if (handle.classList.contains("left-handle")) {
        if (sliderIndex - 1 < 0) {
            slider.style.setProperty("--slider-index", progressBarItemCount - 1)
            progressBar.children[sliderIndex].classList.remove('active')
            progressBar.children[progressBarItemCount - 1].classList.add('active')
        } else {
            slider.style.setProperty("--slider-index", sliderIndex - 1)
            progressBar.children[sliderIndex].classList.remove('active')
            progressBar.children[sliderIndex - 1].classList.add('active')
        }
    }
    if (handle.classList.contains("right-handle")) {
        if (sliderIndex + 1 >= progressBarItemCount) {
            slider.style.setProperty("--slider-index", 0)
            progressBar.children[sliderIndex].classList.remove('active')
            progressBar.children[0].classList.add('active')
        } else {
            slider.style.setProperty("--slider-index", sliderIndex + 1)
            progressBar.children[sliderIndex].classList.remove('active')
            progressBar.children[sliderIndex + 1].classList.add('active')
        }
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