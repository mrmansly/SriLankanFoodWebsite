// Put async javascript calls in here to the server that do not require a full page reload.

function updateCartItemQuantity(cartId, quantity, productId, instructions, csrfToken) {
    return fetch("/api-gateway/update-cart-item-quantity", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            quantity: quantity,
            product_id: productId,
            instructions: instructions,
            cart_id: cartId
        })
    }).then(response => response.json());
}
