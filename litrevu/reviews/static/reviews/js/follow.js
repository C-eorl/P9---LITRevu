/**
 * Gestion des abonnements utilisateurs
 */

class FollowManager {
    constructor() {
        this.input = document.querySelector("input[name='name']");
        this.searchGrid = document.getElementById("follow_searchGrid");
        this.csrfToken = this.getCookie("csrftoken");
        this.searchTimer = null;
        this.searchDelay = 300; 
        
        this.init();
    }

    /**
     * Initialisation des événements
     */
    init() {
        if (this.input) {
            this.input.addEventListener("input", () => this.handleSearchInput());
        }
        
        this.initUnsubscribeButtons();
        this.initCancelButtons();
        this.initSeeMoreButtons();
    }

    /**
     * Récupère le token CSRF depuis les cookies
     */
    getCookie(name) {
        if (!document.cookie) return null;
        
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
        return null;
    }

    /**
     * Gère l'événement de saisie dans le champ de recherche
     */
    handleSearchInput() {
        clearTimeout(this.searchTimer);
        this.searchTimer = setTimeout(() => this.searchUser(), this.searchDelay);
    }

    /**
     * Recherche des utilisateurs via AJAX
     */
    async searchUser() {
        const query = this.input.value.trim();

        if (!query) {
            this.showMessage("Commencez à taper pour chercher un utilisateur.");
            return;
        }

        try {
            const response = await fetch(
                `/reviews/search_user/?q=${encodeURIComponent(query)}`
            );
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const users = await response.json();

            if (users.length === 0) {
                this.showMessage("Aucun utilisateur trouvé.");
                return;
            }

            this.displayUsers(users);
        } catch (error) {
            console.error("Erreur lors de la recherche:", error);
            this.showMessage("Une erreur est survenue pendant la recherche.");
        }
    }

    /**
     * Affiche un message dans la grille de recherche
     */
    showMessage(message) {
        this.searchGrid.innerHTML = `<p>${message}</p>`;
        this.searchGrid.classList.add("message");
    }

    /**
     * Affiche la liste des utilisateurs trouvés
     */
    displayUsers(users) {
        this.searchGrid.classList.remove("message");
        
        this.searchGrid.innerHTML = "";

        // Ajouter chaque carte DOM directement
        users.forEach(user => {
            const card = this.createUserCard(user);
            this.searchGrid.appendChild(card);
            
        this.searchGrid.querySelectorAll(".front-btn.sub").forEach(button => {
            button.addEventListener("click", (e) => this.handleFollowClick(e));
        });
    });
    }

    /**
     * Crée une carte utilisateur sécurisée
     */
    createUserCard(user) {
        // Container principal
        const itemGrid = document.createElement('div');
        itemGrid.classList.add('item-grid');

        const card = document.createElement('div');
        card.classList.add('card');

        const cardFront = document.createElement('div');
        cardFront.classList.add('card-front');

        // Image
        const img = document.createElement('img');
        img.src = user.image; 
        img.alt = user.username;

        // Nom utilisateur
        const span = document.createElement('span');
        span.textContent = user.username; 

        // Bouton Abonner
        const button = document.createElement('button');
        button.classList.add('front-btn', 'sub');
        button.dataset.username = user.username;
        button.textContent = "Abonner";

        button.addEventListener('click', () => {
            this.followUser(user.username);
        });

        cardFront.appendChild(img);
        cardFront.appendChild(span);
        cardFront.appendChild(button);

        card.appendChild(cardFront);
        itemGrid.appendChild(card);

        return itemGrid; 
    }

    /**
     * Gère le clic sur un bouton d'abonnement
     */
    async handleFollowClick(event) {
        const button = event.target;
        const username = button.dataset.username;
        const card = button.closest(".item-grid");

        // Désactiver le bouton pendant la requête
        button.disabled = true;

        try {
            const response = await fetch("/reviews/follow_user/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": this.csrfToken,
                },
                body: `username=${encodeURIComponent(username)}`,
            });

            const data = await response.json();

            if (data.success) {
                this.showFollowSuccess(button, card);
            } else {
                alert(data.error || "Erreur lors de l'abonnement");
                button.disabled = false;
            }
        } catch (error) {
            console.error("Erreur réseau:", error);
            alert("Erreur réseau lors de l'abonnement");
            button.disabled = false;
        }
    }

    /**
     * Affiche le succès de l'abonnement
     */
    showFollowSuccess(button, card) {
        button.textContent = "Abonné ✔";
        button.classList.add("success");
        
        setTimeout(() => {
            card.style.opacity = "0";
            setTimeout(() => card.remove(), 300);
        }, 2000);
    }

    /**
     * Initialise les boutons de désabonnement (animation flip)
     */
    initUnsubscribeButtons() {
        document.querySelectorAll(".card .unsub").forEach(button => {
            button.addEventListener("click", () => {
                const card = button.closest(".card");
                card.classList.add("flipped");
            });
        });
    }

    /**
     * Initialise les boutons d'annulation
     */
    initCancelButtons() {
        document.querySelectorAll(".cancel-btn").forEach(button => {
            button.addEventListener("click", () => {
                const card = button.closest(".card");
                card.classList.remove("flipped");
            });
        });
    }

    /**
     * Initialise les boutons "Voir plus"
     */
    initSeeMoreButtons() {
        document.querySelectorAll(".see-more-btn").forEach(button => {
            const grid = button.closest("section").querySelector(".grid-section");
            
            button.addEventListener("click", () => {
                grid.classList.toggle("expanded");
                button.textContent = grid.classList.contains("expanded") 
                    ? "Voir moins" 
                    : "Voir plus";
            });
        });
    }
}

// Initialisation au chargement du DOM
document.addEventListener("DOMContentLoaded", () => {
    new FollowManager();
});