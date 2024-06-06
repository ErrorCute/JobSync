document.getElementById('comuna-filter').addEventListener('change', function() {
    var selectedComuna = this.value;
    var cards = document.querySelectorAll('.card');

    cards.forEach(function(card) {
        var comuna = card.dataset.comuna;
        card.style.display = (selectedComuna === '' || comuna === selectedComuna) ? 'block' : 'none';
    });
})