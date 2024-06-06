document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const url = this.dataset.url;
        window.location.href = url;
    });
});


document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const url = this.dataset.url;
        window.location.href = url;
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("search-input");
    const cards = document.querySelectorAll(".card");

    searchInput.addEventListener("input", function() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        cards.forEach(card => {
            const nombre = card.querySelector("p strong:first-of-type").nextSibling.textContent.toLowerCase();
            if (nombre.includes(searchTerm)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    });
});
