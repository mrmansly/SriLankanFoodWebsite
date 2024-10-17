// This utils file holds functionality that is tightly coupled with id's in order-details.html
import {
    calculateExtendedPrice,
    calculateGSTPrice,
    calculateRevisedSubTotalPrice,
    calculateTotalPrice
} from "./price-calculator.js";
import {removePriceFormatting, dollarFormat} from "./formatting-utils.js";
import {
    incrementQuantityHandler as utilsIncrementQuantityHandler,
    decrementQuantityHandler as utilsDecrementQuantityHandler
} from "./quantity-instruction-utils.js";

export function incrementQuantityHandler(parentForm, productId, gstEnabled) {
    utilsIncrementQuantityHandler(parentForm, productId)
        .then(data => {
            // update the Price fields in the table.
            updateProductPriceWithQuantityChange(data, productId, gstEnabled);
        })
        .catch(error => console.log(error));
}

export function decrementQuantityHandler(parentElement, productId, gstEnabled) {
    const handler = utilsDecrementQuantityHandler(parentElement, productId);

    if (handler) {
        handler.then(data => updateProductPriceWithQuantityChange(data, productId, gstEnabled))
            .catch(error => console.log(error));
    }

}

function updateExtendedPriceOfCartItem(cartItem, productId) {

    const productRowElement = document.getElementById(productId + "-table-row");
    const extendedPriceElement = productRowElement.querySelector('#extendedPrice');
    let extendedPrice = 0;

    // cartItem will be undefined if quantity is 0
    if (cartItem) {
        extendedPrice = calculateExtendedPrice(cartItem['product']['price'], cartItem['quantity']);
    }

    extendedPriceElement.textContent = dollarFormat(extendedPrice);
}

function updatePriceSummary(cartItems, gstEnabled) {
    // calculate the extended price of all items
    const subTotalPrice = cartItems.reduce((accumulator, value) => {
        const extendedPrice = calculateExtendedPrice(value['product']['price'], value['quantity']);
        return accumulator + extendedPrice;
    }, 0);

    updateElementWithPrice('summarySubTotal', subTotalPrice);

    let discount = 0;
    let revisedSubTotalPrice;

    if (document.getElementById("summaryDiscount")) {
        // this section only applicable if there is a discount associated with the order
        discount = removePriceFormatting(document.getElementById("summaryDiscount").textContent);
        revisedSubTotalPrice = calculateRevisedSubTotalPrice(subTotalPrice, discount);
        updateElementWithPrice('summaryRevisedSubTotal', revisedSubTotalPrice);
    } else {
        revisedSubTotalPrice = calculateRevisedSubTotalPrice(subTotalPrice, discount);
    }

    const gstPrice = gstEnabled ? calculateGSTPrice(revisedSubTotalPrice) : 0;

    if (gstEnabled) {
        updateElementWithPrice('summaryGST', gstPrice);
    }

    updateElementWithPrice('summaryTotal', calculateTotalPrice(revisedSubTotalPrice, gstPrice));
}

function updateElementWithPrice(id, price) {
    const element = document.getElementById(id);
    element.textContent = dollarFormat(price);
}

function updateProductPriceWithQuantityChange(data, productId, gstEnabled) {
    const cartItems = data['cart_items'];
    const cartItemWithQuantityChange = cartItems.find(cartItem => cartItem.product.id === Number(productId));
    updateExtendedPriceOfCartItem(cartItemWithQuantityChange, productId);
    updatePriceSummary(cartItems, gstEnabled);
}
