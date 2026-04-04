document.addEventListener('DOMContentLoaded', () => {
    // LÓGICA PARA O FORMULÁRIO DE LOGIN
    const loginForm = document.getElementById('login-form');

    // Este 'if' garante que o código só tente rodar se o formulário de login existir na página
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            // Impede que o navegador envie o formulário da maneira tradicional
            event.preventDefault();

            const formData = new FormData(loginForm);

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    body: formData,
                });

                // Pega a resposta JSON do servidor
                const data = await response.json();

                if (data.success) {
                    // Se o login deu certo, redireciona para a URL que o servidor mandou
                    window.location.href = data.redirect_url;
                } else {
                    // Se deu errado, mostra um alerta
                    alert('Erro no login: ' + data.message);
                }
            } catch (error) {
                console.error('Erro de conexão:', error);
                alert('Não foi possível conectar ao servidor.');
            }
        });
    }
});

// FUNÇÃO DE LOGOUT (usada nas outras páginas)
function logout() {
    fetch('/logout', {
        method: 'POST',
    }).then(() => {
        // Redireciona para a página inicial após o logout
        window.location.href = '/';
    });
}