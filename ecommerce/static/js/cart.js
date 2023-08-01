var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'action:', action);

        console.log('USER:', user);
        if (user === 'AnonymousUser') {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
    });
}

function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data...');

    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        location.reload();
    });
}

var removeBtns = document.getElementsByClassName('remove-item');

for (var i = 0; i < removeBtns.length; i++) {
    removeBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('Removing product with id:', productId, 'action:', action);

        if (user === 'AnonymousUser') {
            removeCookieItem(productId, action);
            location.reload();
        } else {
            if (action === 'remove') {
                // Pass the clicked element explicitly to the function
                removeUserCartItems(this, productId, action);
            }
        }
    });
}

function removeUserCartItems(clickedElement, productId, action) {
    console.log('User is logged in, sending data to remove items...');

    var url = '/remove_items/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        if (data.message === 'Items removed') {
            // Refresh the cart total displayed in the navbar
            document.getElementById('cart-total').innerText = data.cart_total;
            document.getElementById("current-total").innerHTML = data.current_total;
            document.getElementById("currnet_items_count").innerHTML = data.cart_total;

            // Remove the row containing the deleted item using the clickedElement
            var row = clickedElement.parentNode.parentNode;
            row.parentNode.removeChild(row);
            
            
        } else {
            console.log('Error:', data.error);
        }
    });
}
