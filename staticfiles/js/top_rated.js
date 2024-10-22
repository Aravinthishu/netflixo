
    const carousel = document.getElementById('carousel');
    let scrollAmount = 0;

    document.getElementById('next').onclick = function () {
        const cardWidth = document.querySelector('.w-1/5').offsetWidth + 16; // card width + margin
        const maxScroll = carousel.scrollWidth - carousel.offsetWidth;
        scrollAmount = Math.min(scrollAmount + cardWidth, maxScroll);
        carousel.style.transform = `translateX(-${scrollAmount}px)`;
    };

    document.getElementById('prev').onclick = function () {
        const cardWidth = document.querySelector('.w-1/5').offsetWidth + 16; // card width + margin
        scrollAmount = Math.max(scrollAmount - cardWidth, 0);
        carousel.style.transform = `translateX(-${scrollAmount}px)`;
    };
