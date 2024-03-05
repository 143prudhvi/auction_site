function groupItems(){
    checkBoxes = document.getElementsByClassName('group-items');
    nonGroupedIds = []
    groupedIds = []
    for (var i = 0; i < checkBoxes.length; i++) {
        if(checkBoxes[i].checked){
            itemId = checkBoxes[i].getAttribute("data-item-id")
            isGrouped = checkBoxes[i].getAttribute("data-is-grouped")
            if(isGrouped == "True"){
                groupedIds.push(itemId)
            }else{
                nonGroupedIds.push(itemId)
            }
        }
    }

    if(groupedIds.length + nonGroupedIds.length < 2){
        showStatusMessage("Check atleast 2 checkboxes to group items", "error");
    }else{
        fetch("/groupItems" + "?groupedIds=" + groupedIds.join() + "&nonGroupedIds=" + nonGroupedIds.join() )
            .then(response => response.json())
            .then((data) => {
                showStatusMessage(data.message, data.status);
            })
            .catch((error) => {
                showStatusMessage("Something Went Wrong", "error");
            })
    }

    
}

function removeGroupItems(){
    checkBoxes = document.getElementsByClassName('group-items');
    itemIds = []
    for (var i = 0; i < checkBoxes.length; i++) {
        if(checkBoxes[i].checked){
            itemIds.push(checkBoxes[i].getAttribute("data-item-id"))
        }
    }
    fetch("/removeGroupItems" + "?itemIds=" + itemIds.join() )
        .then(response => response.json())
        .then((data) => {
            showStatusMessage(data.message, data.status);
        })
        .catch((error) => {
            showStatusMessage("Something Went Wrong", "error");
        })
}

function addGroupItem(){
    inputBox = document.getElementById('add-group-item-id');
    fetch("/addGroupItem" + "?itemId=" + inputBox.value + "&groupId=" + inputBox.getAttribute("data-group-id") )
        .then(response => response.json())
        .then((data) => {
            showStatusMessage(data.message, data.status);
        })
        .catch((error) => {
            showStatusMessage("Something Went Wrong", "error");
        })
}