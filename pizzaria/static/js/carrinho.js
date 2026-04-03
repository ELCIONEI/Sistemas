const PizzaCart = {
    items: [],

    async init() {
        try {
            const response = await fetch('/get_cart');
            const data = await response.json();
            this.items = data.items || [];
            localStorage.setItem('pizzaCart', JSON.stringify(this.items));
        } catch (err) {
            this.items = JSON.parse(localStorage.getItem('pizzaCart')) || [];
        }
        this.updateBadge();
        this.setupButtons();
        this.setupModal(); // Nova chamada para organizar o modal
    },

    setupButtons() {
        document.addEventListener('click', async (e) => {
            const target = e.target.closest('.btn, .btn-qty, .btn-secondary, .btn-remove');
            if (!target) return;

            const nome = target.getAttribute('data-nome');

            if (target.id === 'btn-finalizar') {
                e.preventDefault();
                this.enviarWhatsApp();
                return;
            }

            if (target.getAttribute('href') && target.getAttribute('href').includes('/limpar')) {
                localStorage.removeItem('pizzaCart');
                this.items = [];
                this.updateBadge();
                return; 
            }

            if (target.hasAttribute('data-preco')) {
                e.preventDefault();
                const preco = parseFloat(target.getAttribute('data-preco'));
                this.items.push({ nome, preco });
                this.saveAndSync();
                return;
            }

            if (target.classList.contains('btn-qty')) {
                const action = target.getAttribute('data-action');
                if (action === 'increase') {
                    const original = this.items.find(i => i.nome === nome);
                    if (original) this.items.push({ ...original });
                } else if (action === 'decrease') {
                    const index = this.items.findIndex(i => i.nome === nome);
                    if (index !== -1) this.items.splice(index, 1);
                }
                this.saveAndSync();
            }
            
            if (target.classList.contains('btn-remove')) {
                e.preventDefault();
                if (nome) {
                    this.items = this.items.filter(item => item.nome !== nome);
                    this.saveAndSync();
                }
            }
        });
    },

    // Centralizei a lógica do Modal aqui para ficar organizado
    setupModal() {
        const modal = document.getElementById("modal-cadastro");
        const btn = document.getElementById("open-modal");
        const span = document.querySelector(".close-modal");

        if(btn && modal) {
            btn.onclick = (e) => {
                e.preventDefault();
                modal.style.display = "flex";
            }
        }

        if(span && modal) {
            span.onclick = () => modal.style.display = "none";
        }

        window.onclick = (event) => {
            if (event.target == modal) modal.style.display = "none";
        }
    },

    enviarWhatsApp() {
        if (this.items.length === 0) {
            alert("Seu carrinho está vazio!");
            return;
        }

        const resumo = this.items.reduce((acc, item) => {
            if (!acc[item.nome]) {
                acc[item.nome] = { qtd: 0, precoUnitario: item.preco };
            }
            acc[item.nome].qtd += 1;
            return acc;
        }, {});

        let mensagem = "*🍕 Novo Pedido - Pizza Amiga*\n";
        mensagem += "----------------------------------\n\n";
        
        let totalPedido = 0;
        for (const nome in resumo) {
            const { qtd, precoUnitario } = resumo[nome];
            const subtotal = qtd * precoUnitario;
            totalPedido += subtotal;
            mensagem += `✅ *${qtd}x* ${nome}\n   _Subtotal: R$ ${subtotal.toFixed(2)}_\n\n`;
        }

        mensagem += "----------------------------------\n";
        mensagem += `💰 *Total: R$ ${totalPedido.toFixed(2)}*\n\n`;
        mensagem += "👉 *Forma de pagamento:* (a combinar)";

        const numeroTelefone = "5561981953090"; 
        const url = `https://api.whatsapp.com/send?phone=${numeroTelefone}&text=${encodeURIComponent(mensagem)}`;

        window.open(url, '_blank');
    },

    async saveAndSync() {
        localStorage.setItem('pizzaCart', JSON.stringify(this.items));
        try {
            await fetch('/update_cart_session', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ items: this.items })
            });
            
            if (window.location.pathname.includes('/carrinho')) {
                window.location.reload();
            } else {
                this.updateBadge();
            }
        } catch (err) {
            console.error("Erro na sincronização:", err);
        }
    },

    updateBadge() {
        const badge = document.getElementById('cart-count');
        if (badge) {
            const count = this.items.length;
            badge.innerText = count;
            badge.style.display = count > 0 ? 'flex' : 'none';
        }
    }
};

document.addEventListener('DOMContentLoaded', () => PizzaCart.init());