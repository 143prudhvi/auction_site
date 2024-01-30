function openProductModal(itemId){
    var productModal = document.getElementsByClassName(itemId + " modal")
    for(var i= 0; i < productModal.length; i++ ){
        productModal[i].style.display = "block";
    }
    var url = document.getElementById(itemId + "slideshow-content").getAttribute('data-match-url')
    getMatchedIds(itemId, url)
}

function closeProductModal(itemId){
    var modal = document.getElementsByClassName(itemId + " modal");
    for(var i= 0; i < modal.length; i++ ){
        modal[i].style.display = "none";
    }
}

