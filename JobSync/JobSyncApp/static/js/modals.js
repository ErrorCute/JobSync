document.addEventListener('DOMContentLoaded', function() {
    const modals = document.querySelectorAll('.modal');
    const closeModals = document.querySelectorAll('.close-modal');
  
    closeModals.forEach(function(closeModal) {
      closeModal.addEventListener('click', function() {
        this.closest('.modal').classList.remove('modal-fade-show');
        this.closest('.modal').classList.add('modal-fade');
      });
    });
  
    document.addEventListener('click', function(e) {
      if (e.target.classList.contains('modal-fade')) {
        e.target.classList.remove('modal-fade-show');
        e.target.classList.add('modal-fade');
      }
    });
  });