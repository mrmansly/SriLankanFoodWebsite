import {updateCartItem} from './api-utils.js';

function getCartId() {
    return document.querySelector('meta[name="cart_id"]').getAttribute('content');
}

export function updateCartItemDetails(quantity, product_id, instructions) {
    return updateCartItem(getCartId(), quantity, product_id, instructions)
        .then(data => {
            const items = data['cart_items'].reduce((accumulator, currentValue) => {
                return accumulator + currentValue['quantity'];
            }, 0);

            updateCartItems(items);
            return data;
        });
}
