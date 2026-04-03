document.addEventListener('DOMContentLoaded', function() {
    
    // --- SCRIPT PARA O MURAL DE EVENTOS INTERATIVO ---
    const muralThumbnails = document.querySelectorAll('.thumbnail-img');
    const muralContentPanels = document.querySelectorAll('.mural-content');
    
    if (muralThumbnails.length > 0 && muralContentPanels.length > 0) {
        let muralCurrentIndex = 0;
        const muralIntervalTime = 5000;
        let muralBannerInterval;

        // FUNÇÃO ATUALIZADA: Agora busca pelo ID do alvo
        const showMuralBanner = (targetId) => {
            // Esconde todos os painéis e desativa todas as miniaturas
            muralContentPanels.forEach(panel => panel.classList.remove('active'));
            muralThumbnails.forEach(thumb => thumb.classList.remove('active-thumbnail'));

            // Encontra o painel e a miniatura corretos usando o targetId
            const targetPanel = document.getElementById(targetId);
            const targetThumbnail = document.querySelector(`.thumbnail-img[data-target-id="${targetId}"]`);

            if (targetPanel && targetThumbnail) {
                targetPanel.classList.add('active');
                targetThumbnail.classList.add('active-thumbnail');

                // Atualiza o índice atual para o carrossel continuar da posição correta
                muralThumbnails.forEach((thumb, index) => {
                    if (thumb === targetThumbnail) {
                        muralCurrentIndex = index;
                    }
                });
            }
        };

        const showNextMuralBanner = () => {
            muralCurrentIndex = (muralCurrentIndex + 1) % muralThumbnails.length;
            const nextThumbnail = muralThumbnails[muralCurrentIndex];
            const nextTargetId = nextThumbnail.getAttribute('data-target-id');
            showMuralBanner(nextTargetId);
        };

        const startMuralCarousel = () => {
            clearInterval(muralBannerInterval); // Limpa o intervalo anterior para evitar aceleração
            muralBannerInterval = setInterval(showNextMuralBanner, muralIntervalTime);
        };

        // EVENTO DE CLIQUE ATUALIZADO
        muralThumbnails.forEach(thumb => {
            thumb.addEventListener('click', () => {
                const targetId = thumb.getAttribute('data-target-id');
                showMuralBanner(targetId);
                startMuralCarousel(); // Reinicia o temporizador do carrossel após um clique manual
            });
        });

        // Inicia o mural mostrando o primeiro item
        const firstTargetId = muralThumbnails[0].getAttribute('data-target-id');
        showMuralBanner(firstTargetId);
        startMuralCarousel();
    }

    // --- SCRIPT PARA O LIGHTBOX DAS GALERIAS (MESTRES, ALUNOS E ATIVIDADES) ---
    // (Seu código do lightbox continua aqui, sem alterações)
    const lightbox = document.getElementById('lightbox');
    const imagesToEnlarge = document.querySelectorAll('.master-card img, .student-card img');

    if (lightbox && imagesToEnlarge.length > 0) {
        const lightboxImg = document.getElementById('lightbox-img');
        const closeBtn = document.querySelector('.lightbox-close');

        imagesToEnlarge.forEach(image => {
            image.addEventListener('click', function() {
                lightbox.classList.add('active');
                lightboxImg.src = this.src;
            });
        });

        const closeLightbox = () => {
            lightbox.classList.remove('active');
        };

        closeBtn.addEventListener('click', closeLightbox);
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) {
                closeLightbox();
            }
        });
    }
});