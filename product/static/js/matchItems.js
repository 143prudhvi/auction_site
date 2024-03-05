function showStatusMessage(message, className) {
    const statusBar = document.getElementById('statusBar');

    // Set the message and class
    statusBar.textContent = message;
    statusBar.className = className;

    // Show the status bar
    statusBar.classList.remove('hidden');

    // Hide the status bar after a certain duration (e.g., 5 seconds)
    setTimeout(() => {
        statusBar.classList.add('hidden');
    }, 5000);
}

function matchAction(itemId){
    var inputBox = document.getElementById(itemId + '_matchInput');
    var matchButton = document.getElementById(itemId + '_matchButton');
    if (inputBox.disabled) {
        inputBox.disabled = false;
        matchButton.innerHTML = 'Save';
    } else {
        inputBox.disabled = true;
        matchButton.innerHTML = 'Edit';
        url = matchButton.getAttribute('data-url');
        matchedId = inputBox.value;
        const statusBar = document.getElementById('statusBar');

        fetch(url + '?itemId=' + itemId + '&matchedId=' + matchedId)
        .then(response => response.json())
        .then((data) => {
            setTimeout(() => {
                showStatusMessage(data.message, data.status);
            }, 2000);
        })
        .catch((error) => {
            setTimeout(() => {
                showStatusMessage("Something Went Wrong", "error");
            }, 2000);
        })
    }
}

function getMatchedIds(itemId, url){
    var inputBox = document.getElementById(itemId + '_matchInput');
    var matchButton = document.getElementById(itemId + '_matchButton');
    fetch(url + '?itemId=' + itemId )
    .then(response => response.json())
    .then((data) => {
        if(data.status == "success" && data.numberOfRecords){
            inputBox.disabled = true;
            matchButton.innerHTML = 'Edit';
            inputBox.value = data.matchedIds
        }else if(data.status == "success" && !data.numberOfRecords){
            inputBox.value = ""
            matchButton.innerHTML = 'Save';
            inputBox.disabled = false;
        }else{

        }
    })
    .catch((error) => {
        setTimeout(() => {
            showStatusMessage("Something Went Wrong", "error");
        }, 2000);
    })
}