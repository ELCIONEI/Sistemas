// js/script.js

document.addEventListener('DOMContentLoaded', function() {

    // --- LÓGICA PARA O CARROSSEL DO BANNER (HERO) ---
    const hero = document.getElementById('hero-carousel');
    if (hero) {
        const images = [
            'images/peca11.jpg',
            'images/peca13.jpg',
            'images/peca9.jpg'
        ];
        let currentImageIndex = 0;

        function changeBackgroundImage() {
            currentImageIndex = (currentImageIndex + 1) % images.length;
            hero.style.backgroundImage = `linear-gradient(to top, rgba(0, 0, 0, 0.9) 10%, transparent 50%), url('${images[currentImageIndex]}')`;
        }
        setInterval(changeBackgroundImage, 5000);
    }

    // --- LÓGICA PARA O NOVO CARROSSEL DE VÍDEOS ---
    const videoCarousel = document.querySelector('.video-carousel');
    if (videoCarousel) {
        const prevBtn = document.querySelector('.prev-btn');
        const nextBtn = document.querySelector('.next-btn');
        const slides = document.querySelectorAll('.video-slide');
        let currentIndex = 0;
        const totalSlides = slides.length;

        function updateCarousel() {
            const offset = -currentIndex * 100;
            videoCarousel.style.transform = `translateX(${offset}%)`;
        }

        nextBtn.addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % totalSlides;
            updateCarousel();
        });

        prevBtn.addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
            updateCarousel();
        });
    }
});

// js/script.js

document.addEventListener('DOMContentLoaded', function() {
    
    // ... (todo o código dos carrosséis que já existe) ...


    // --- LÓGICA PARA O VISUALIZADOR DE IMAGEM (MODAL) ---
    const modal = document.getElementById('image-modal');
    if (modal) {
        const modalImg = document.getElementById('modal-image');
        const clickableImages = document.querySelectorAll('.clickable-image');
        const closeModalBtn = document.querySelector('.close-modal-btn');

        // Abre o modal quando uma imagem clicável é pressionada
        clickableImages.forEach(img => {
            img.onclick = function() {
                modal.style.display = "flex"; // Usa flex para centralizar
                modalImg.src = this.src;
            }
        });

        // Fecha o modal ao clicar no 'X'
        closeModalBtn.onclick = function() {
            modal.style.display = "none";
        }

        // Fecha o modal ao clicar fora da imagem (no fundo escuro)
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
    }

});