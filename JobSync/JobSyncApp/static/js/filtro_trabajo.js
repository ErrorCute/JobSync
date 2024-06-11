document.addEventListener('DOMContentLoaded', function() {
    const comunaFilter = document.getElementById('comuna-filter');
    const estadoFilter = document.getElementById('estado-filter');
    const fechaFilter = document.getElementById('fecha-filter');
    const cards = document.querySelectorAll('.card');

    function filtrarTarjetas() {
        const selectedComuna = comunaFilter.value;
        const selectedEstado = estadoFilter.value;
        const selectedFecha = fechaFilter.value;

        cards.forEach(card => {
            const comuna = card.dataset.comuna;
            const estadoCard = card.dataset.estado;
            const fechaCard = card.dataset.fecha;

            const comunaMatch = selectedComuna === '' || comuna === selectedComuna;
            const estadoMatch = selectedEstado === '' || estadoCard === selectedEstado;
            const fechaMatch = selectedFecha === '' || fechaCard === selectedFecha;

            if (comunaMatch && estadoMatch && fechaMatch) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    comunaFilter.addEventListener('change', filtrarTarjetas);
    estadoFilter.addEventListener('change', filtrarTarjetas);
    fechaFilter.addEventListener('change', filtrarTarjetas);
});
