function openProductModal(productId){
    var productModal = document.getElementsByClassName(productId + " modal")
    for(var i= 0; i < productModal.length; i++ ){
        productModal[i].style.display = "block";
    }
}

function closeProductModal(productId){
    var modal = document.getElementsByClassName(productId + " modal");
    for(var i= 0; i < modal.length; i++ ){
        modal[i].style.display = "none";
    }
}

