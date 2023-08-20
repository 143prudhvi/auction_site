var slideIndex = 1;
var products = document.getElementsByClassName("slideshow-container");
for (i = 0; i < products.length; i++){
    showSlides(slideIndex, products[i].getAttribute("data-id"))
}

function plusSlides(n, productId) {
    showSlides(slideIndex += n, productId);
}

function showSlides(n, productId) {
    var i;
    var slides = document.getElementsByClassName(productId + " mySlides");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex-1].style.display = "block";
}