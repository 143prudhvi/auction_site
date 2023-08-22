var slideIndex = 1;
var products = document.getElementsByClassName("slideshow-container");
for (i = 0; i < products.length; i++){
    showSlides(slideIndex, products[i].getAttribute("data-id"), "mySlides")
    showSlides(slideIndex, products[i].getAttribute("data-id"), "modal-image-container");

}

function plusSlides(n, productId, type) {
    showSlides(slideIndex += n, productId, type);
}

function showSlides(n, productId, type) {
    var i;
    var slides = document.getElementsByClassName(productId + " " + type);
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex-1].style.display = "block";
}