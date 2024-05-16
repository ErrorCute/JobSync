
document.addEventListener("DOMContentLoaded", function() {
    var confirmarBtn = document.getElementById("confirmarBtn");
    var confirmarCambiosBtn = document.getElementById("confirmarCambiosBtn");

    if (confirmarBtn) {
        confirmarBtn.addEventListener("click", function() {
            $('#confirmarModal').modal('show');
        });
    }

    if (confirmarCambiosBtn) {
        confirmarCambiosBtn.addEventListener("click", function() {
            document.getElementById("modificarUsuarioForm").submit();
        });
    }
});
