var loading = false;

function loadMoreItems() {
    if (!loading) {
        loading = true;
        var url = document.getElementById('load-more').getAttribute('data-url');
        var offset = document.getElementById('load-more').getAttribute('data-offset');
        var selectedPlatform = document.getElementById('load-more').getAttribute('data-selected-platform');
        var selectedBrand = document.getElementById('load-more').getAttribute('data-selected-brand');
        var selectedSeller = document.getElementById('load-more').getAttribute('data-selected-seller');
        var titleSearch = document.getElementById('load-more').getAttribute('data-title-search');
        var imageExist = document.getElementById('load-more').getAttribute('data-image-exist');
        var duplicateGroup = document.getElementById('load-more').getAttribute('data-duplicate-group');


        fetch(url + '?offset=' + offset + '&brand=' + selectedBrand + '&seller=' + selectedSeller + '&title_search=' + titleSearch + '&platform=' + selectedPlatform + '&image_exist=' + imageExist + '&duplicate_group=' + duplicateGroup )
            .then(response => response.json())
            .then((data) => {
                itemList = ""
                data.items.forEach((item) => {
                    first = true
                    modalFirst = true
                    item_div = ""
                    item_div += '<div class="' + item.fields.itemId + ' slideshow-container" data-id="'+ item.fields.itemId+ '" style="opacity:'  
                    if(item.fields.matchedCount){
                        item_div += '0.3;">'
                    }else{
                        item_div += '1.0;">'
                    }
                    item_div += '<input type="checkbox" id="'+ item.fields.itemId+ '_checkbox" class="group-items" data-item-id="' + item.fields.itemId +  '" data-is-grouped="' + item.fields.isGrouped + '" name="product-grey-scale-checkbox"'
                    if(item.fields.matchedCount){
                        item_div += 'checked>'
                    }else{
                        item_div += '>'
                    }
                    item_div +=  '<div class="slideshow-content" id="' + item.fields.itemId + 'slideshow-content" data-match-url="/getMatchedIds" onclick="openProductModal(\'' +  item.fields.itemId + '\')">'
                    for(let key in data.item_images){
                        if(item.fields.itemId == key ){
                            data.item_images[key].forEach((image_link) => {
                                if(first){
                                    item_div += '<div class="' + item.fields.itemId + ' mySlides" style="display: block;"><img class="slideshow-img" src="'+ image_link +'" alt="Product Image"></div>'
                                    first = false
                                }else{
                                    item_div += '<div class="' + item.fields.itemId + ' mySlides" style="display: none;"><img class="slideshow-img" src="'+ image_link +'" alt="Product Image"></div>'
                                }
                            })
                        }
                    }
                    item_div += '</div><div class="prev-next-links">'
                    item_div += '<a class="prev" onclick="plusSlides(-1, \'' + item.fields.itemId + '\' , \'mySlides\')">&#10094;</a>'
                    item_div += '<a class="next" onclick="plusSlides(1, \'' + item.fields.itemId + '\' , \'mySlides\')">&#10095;</a></div>'
                    item_div += '<strong class="product-id">' + item.fields.itemId + '</strong>'
                    item_div += '<div class="item-count" style="font-size:10px; ">Matched Items Count : <strong >' + item.fields.matchedCount + '</strong></div>'
                    if(item.fields.groupId){
                        item_div += '<div class="group-link"> <a href="/group/' + item.fields.groupId + '">' + item.fields.groupId + '</a> </div>'
                    }
                    item_div += '</div>'
                    item_div += '<div class="' + item.fields.itemId +' modal"><div class="modal-content"><div class="product-card">'
                    for(let key in data.item_images){
                        if(item.fields.itemId == key ){
                            data.item_images[key].forEach((image_link) => {
                                if(modalFirst){
                                    item_div += '<div class="' + item.fields.itemId + ' modal-image-container" style="display: block;"><img class="modal-img" src="'+ image_link +'" alt="Product Image"></div>'
                                    modalFirst = false
                                }else{
                                    item_div += '<div class="' + item.fields.itemId + ' modal-image-container" style="display: none;"><img class="modal-img" src="'+ image_link +'" alt="Product Image"></div>'
                                }
                            })
                        }
                    }
                                
                    item_div += '<div class="prev-next-links">'
                    item_div += '<a class="prev" onclick="plusSlides(-1, \'' + item.fields.itemId + '\' , \'modal-image-container\')">&#10094;</a>'
                    item_div += '<a class="next" onclick="plusSlides(1, \'' + item.fields.itemId + '\' , \'modal-image-container\')">&#10095;</a></div></div>'
                    item_div += '<div class="product-details"><div class="modal-product-id"><label class="detail-label">Product Id</label> <span>' + item.fields.itemId + '</span></div>'
                    item_div += '<div class="modal-match-itemid"><label class="detail-label">Matched Items <strong style="font-size:16px;">' + item.fields.matchedCount + '</strong></label><textarea rows="4" cols="30" placeholder="Matched Item Id" id="' + item.fields.itemId + '_matchInput" '
                    if(item.fields.matchedCount){
                        item_div += 'disabled '
                    }
                    item_div += '></textarea><button id="' + item.fields.itemId + '_matchButton" data-url="/saveMatchedItems" onclick="matchAction(\'' + item.fields.itemId + '\')">'
                    if(item.fields.matchedCount){
                        item_div += 'Edit'
                    }else{
                        item_div += 'Save'
                    }
                    item_div += '</button></div>'
                    item_div += '<div class="product-title"><label class="detail-label">Title</label> <span>' + item.fields.title + '</span></div>'
                    item_div += '<div class="product-seller"><label class="detail-label">Seller</label> <span>' + item.fields.sellerName + '</span></div>'
                    item_div += '<div class="product-brand"><label class="detail-label">Brand</label> <span>' + item.fields.brand + '</span></div>'
                    item_div += '<div class="product-price"><label class="detail-label">Price</label> <span>' + item.fields.price + '</span></div>'
                    item_div += '<div class="product-description"><label class="detail-label">Features</label>'
                    if(item.fields.platform == "eBay"){
                        item_div += '<iframe src="https://vi.vipr.ebaydesc.com/ws/eBayISAPI.dll?ViewItemDescV4&item=' + item.fields.itemId + '" width="100%" height="300" frameborder="0" allowfullscreen></iframe>'
                    }else{
                        item_div += '<div class="product-description-list">' + item.fields.itemDescription + '</div> '
                    }
                    item_div += '</div></div>'
                    item_div += '<div class="close-btn" onclick="closeProductModal(\'' + item.fields.itemId + '\')" ><img class="close-img" src="static/Images/close.png" /></div><div class="navigate-to-product"><a href="' + item.fields.url + '" target="_blank"><img class="close-img" src="static/Images/website.png" /></a></div></div></div>'
                    itemList += item_div
                })
                var itemsContainer = document.getElementById('items-container');
                itemsContainer.innerHTML += itemList
                document.getElementById('load-more').setAttribute('data-offset', parseInt(offset) + 24);
                loading = false;
            })
            .catch(error => {
                console.error('Error:', error);
                loading = false;
            });
    }
}

document.getElementById('load-more').addEventListener('click', loadMoreItems);