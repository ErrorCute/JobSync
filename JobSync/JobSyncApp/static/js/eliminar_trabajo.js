document.addEventListener("DOMContentLoaded", function() {
    const deleteButtons = document.querySelectorAll(".delete-button");
    let trabajoIdToDelete = null;

    deleteButtons.forEach(button => {
        button.addEventListener("click", function() {
            trabajoIdToDelete = this.getAttribute('data-id');
            const confirmModal = document.getElementById("confirmModal");
            $(confirmModal).modal('show');
        });
    });

    document.getElementById("confirmDelete").addEventListener("click", function() {
        if (trabajoIdToDelete) {
 
            const confirmModal = document.getElementById("confirmModal");
            $(confirmModal).modal('hide');

            showModal('Eliminado correctamente');
        }
    });
    
    function showModal(message) {
        const messageModal = document.getElementById("messageModal");
        messageModal.querySelector(".modal-body").textContent = message;
        $(messageModal).modal('show');
    }
});
