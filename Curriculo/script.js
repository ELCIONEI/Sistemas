/**
 * Função para inicializar um carrossel.
 * @param {string} seletor - O seletor CSS do container do carrossel (ex: '#galeria-cisco').
 */
function inicializarCarrossel(seletor) {
    const carousel = document.querySelector(seletor);
    // Se o elemento do carrossel não existir na página, a função para aqui.
    if (!carousel) {
        console.warn(`Carrossel com seletor "${seletor}" não encontrado.`);
        return;
    }

    // Seleciona os elementos INTERNOS de cada carrossel
    const slide = carousel.querySelector('.carousel-slide');
    const items = carousel.querySelectorAll('.carousel-item');
    const prevBtn = carousel.querySelector('.prev-btn');
    const nextBtn = carousel.querySelector('.next-btn');
    const dotsContainer = carousel.querySelector('.carousel-dots');

    // Se algum elemento essencial estiver faltando, a função para aqui.
    if (!slide || !prevBtn || !nextBtn || !dotsContainer) {
        console.error(`Estrutura do carrossel "${seletor}" está incompleta.`);
        return;
    }

    let currentIndex = 0;
    const totalItems = items.length;

    // --- Cria os pontos de navegação ---
    // Limpa pontos antigos antes de criar novos, para evitar duplicação
    dotsContainer.innerHTML = ''; 
    for (let i = 0; i < totalItems; i++) {
        const dot = document.createElement('span'); // 'span' é semanticamente melhor para isso
        dot.classList.add('dot');
        dot.addEventListener('click', () => {
            goToSlide(i);
        });
        dotsContainer.appendChild(dot);
    }
    const dots = dotsContainer.querySelectorAll('.dot');

    // --- Função principal para ir para um slide ---
    function goToSlide(index) {
        // Lógica para o carrossel "infinito"
        if (index < 0) {
            index = totalItems - 1;
        } else if (index >= totalItems) {
            index = 0;
        }

        slide.style.transform = `translateX(-${index * 100}%)`;
        currentIndex = index;
        updateDots();
    }

    // --- Função para atualizar qual ponto está ativo ---
    function updateDots() {
        if (dots.length > 0) {
            dots.forEach((dot, index) => {
                if (index === currentIndex) {
                    dot.classList.add('active');
                } else {
                    dot.classList.remove('active');
                }
            });
        }
    }
    
    // --- Event Listeners para os botões ---
    nextBtn.addEventListener('click', () => {
        goToSlide(currentIndex + 1);
    });

    prevBtn.addEventListener('click', () => {
        goToSlide(currentIndex - 1);
    });

    // --- Inicia o carrossel no primeiro slide ---
    goToSlide(0);
}

// --- INICIALIZAÇÃO DOS CARROSSÉIS ---
// O código só roda depois que todo o HTML da página foi carregado.
document.addEventListener('DOMContentLoaded', () => {
    // Chame a função para CADA carrossel que você tem na página.
    inicializarCarrossel('#galeria-hashtag');
    inicializarCarrossel('#galeria-cisco');
    inicializarCarrossel('#galeria-dio');
    inicializarCarrossel('#galeria-certificacoes');
});
