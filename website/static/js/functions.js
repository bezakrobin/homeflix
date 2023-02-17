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

const swiper = new Swiper('.swiper', {
    slidesPerView: 6,
    slidesPerGroup: 6,
    spaceBetween: 0,
    direction: 'horizontal',
    loop: true,
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
        100: {
          slidesPerView: 2,
          slidesPerGroup: 1,
          spaceBetween: 10,
        },
        640: {
          slidesPerView: 3,
          slidesPerGroup: 2,
          spaceBetween: 10,
        },
        768: {
          slidesPerView: 4,
          slidesPerGroup: 3,
          spaceBetween: 10,
        },
        1024: {
          slidesPerView: 6,
          slidesPerGroup: 6,
          spaceBetween: 10,
        },
    }
});

var swiperSlide = document.getElementsByName("swiper-slide");
swiperSlide.forEach(element => {
    element.addEventListener("mouseenter", () => {   
        element.querySelector('.bottom-left').setAttribute('class', 'bottom-left white');
    });
});

swiperSlide.forEach(element => {
    element.addEventListener("mouseleave", () => {   
        element.querySelector('.bottom-left').setAttribute('class', 'bottom-left transparent');
    });
});