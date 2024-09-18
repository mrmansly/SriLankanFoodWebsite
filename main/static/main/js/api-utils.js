// Put async javascript calls in here to the server that do not require a full page reload.

export function updateCartItem(cartId, quantity, productId, instructions) {
    return fetch("/api-gateway/update-cart-item-quantity", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            cart_id: cartId,
            quantity: quantity,
            product_id: productId,
            instructions: instructions === undefined ? null : instructions
        })
    }).then(response => response.json());
}

function getCSRFToken() {
    // token stored in base.html template
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

