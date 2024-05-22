document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    form.addEventListener("submit", function(event) {
        event.preventDefault();
        // Aquí iría la lógica para enviar el formulario via AJAX si es necesario
        showModal('Trabajo modificado correctamente');
    });

    function showModal(message) {
        const modal = document.getElementById("messageModal");
        modal.querySelector(".modal-body").textContent = message;
        $(modal).modal('show');
    }
});