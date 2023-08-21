function toggleGrayScale(productId){
    var checkbox = document.getElementById(productId+"_checkbox")
    var products = document.getElementsByClassName(productId + " slideshow-container")
    if (checkbox.checked) {
        for(var i=0; i<products.length; i++){
            products[i].style.filter = "opacity(30%)"
        }
    } else {
        for(var i=0; i<products.length; i++){
            products[i].style.filter = "none"
        }
    }
}