document.addEventListener("DOMContentLoaded", () => {
    const input = document.querySelector("input[name='name']");
    const searchGrid = document.getElementById("follow_searchGrid");
    const csrftoken = getCookie("csrftoken");
    let timer;

    //  Fonction pour récupérer le CSRF token depuis le cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    //  Recherche d'utilisateur
    async function searchUser() {
        const query = input.value.trim();

        if (!query) {
            searchGrid.innerHTML = "<p>Commencez à taper pour chercher un utilisateur.</p>";
            searchGrid.classList.add("message");
            return;
        }

        try {
            const response = await fetch(`/reviews/search_user/?q=${encodeURIComponent(query)}`);
            const users = await response.json();

            if (users.length === 0) {
                searchGrid.innerHTML = "<p>Aucun utilisateur trouvé.</p>";
                searchGrid.classList.add("message");
                return;
            }

            searchGrid.classList.remove("message");
            searchGrid.innerHTML = users
                .map(
                    (user) => `
                    <div class="item-grid">
                        <div class="card">
                            <div class="card-front">
                                <img src="${user.image}" alt="${user.username}">
                                <span>${user.username}</span>
                                <button class="front-btn sub" data-username="${user.username}">Abonner</button>
                            </div>
                        </div>
                    </div>
                `
                )
                .join("");

            // Ajouter listeners sur tous les boutons "Abonner"
            searchGrid.querySelectorAll(".front-btn.sub").forEach((button) => {
                button.addEventListener("click", async (e) => {
                    const username = e.target.dataset.username;
                    const card = e.target.closest(".item-grid");

                    try {
                        const response = await fetch("/reviews/follow_user/", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/x-www-form-urlencoded",
                                "X-CSRFToken": csrftoken,
                            },
                            body: `username=${encodeURIComponent(username)}`,
                        });

                        const data = await response.json();

                        if (data.success) {
                            e.target.textContent = "Abonné ✔";
                            e.target.disabled = true;
                            e.target.classList.add("success");
                            setTimeout(() => {
                                card.remove();
                            }, 3000);
                        } else {
                            alert(data.error || "Erreur lors de l’abonnement");
                        }
                    } catch (error) {
                        console.error("Erreur:", error);
                        alert("Erreur réseau");
                    }
                });
            });
        } catch (error) {
            console.error("Erreur:", error);
            searchGrid.innerHTML = "<p>Une erreur est survenue pendant la recherche.</p>";
            searchGrid.classList.add("message");
        }
    }

    //  Appel la recherche avec délai de 300ms
    input.addEventListener("input", () => {
        clearTimeout(timer);
        timer = setTimeout(searchUser, 300);
    });

    // applique l'animation pour le  Boutons "Désabonner"
    document.querySelectorAll(".card .unsub").forEach((button) => {
        button.addEventListener("click", () => {
            const card = button.closest(".card");
            card.classList.add("flipped");
        });
    });

    document.querySelectorAll(".cancel-btn").forEach((button) => {
        button.addEventListener("click", () => {
            const card = button.closest(".card");
            card.classList.remove("flipped");
        });
    });

    // Boutons "Voir plus"
    document.querySelectorAll(".see-more-btn").forEach((btn) => {
        const grid = btn.closest("section").querySelector(".grid-section");
        btn.addEventListener("click", () => {
            grid.classList.toggle("expanded");
            btn.textContent = grid.classList.contains("expanded") ? "Voir moins" : "Voir plus";
        });
    });
});
