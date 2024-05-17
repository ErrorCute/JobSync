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
    var cardContainer = document.querySelector(".card-container");
    var registerButton = document.getElementById("registerButton");

    if (cardContainer.children.length > 1) {
        var lastCard = cardContainer.querySelector(".card:last-child");


        var buttonTop = lastCard.offsetTop + lastCard.offsetHeight / 3 - registerButton.offsetHeight / 2;
        var buttonLeft = lastCard.offsetLeft + lastCard.offsetWidth + 20; 

        registerButton.style.position = "absolute";
        registerButton.style.top = buttonTop + "px";
        registerButton.style.left = buttonLeft + "px";
    } else {

        registerButton.style.position = "relative";
        registerButton.style.top = "20px"; 
        registerButton.style.left = "0";
    }
});