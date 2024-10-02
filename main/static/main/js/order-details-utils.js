// This utils file holds functionality that is tightly coupled with id's in order-details.html
// import {updateCartItemDetails} from './cart-utils.js';
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

export function incrementQuantityHandler(parentForm, productId) {
    utilsIncrementQuantityHandler(parentForm, productId)
        .then(data => {
            // update the Price fields in the table.
            updateProductPriceWithQuantityChange(data, productId);
        })
        .catch(error => console.log(error));
}

export function decrementQuantityHandler(parentElement, productId) {
    const handler = utilsDecrementQuantityHandler(parentElement, productId);

    if (handler) {
        handler.then(data => updateProductPriceWithQuantityChange(data, productId))
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

function updatePriceSummary(cartItems) {
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

    const gstPrice = calculateGSTPrice(revisedSubTotalPrice);
    updateElementWithPrice('summaryGST', gstPrice);
    updateElementWithPrice('summaryTotal', calculateTotalPrice(revisedSubTotalPrice, gstPrice));
}

function updateElementWithPrice(id, price) {
    const element = document.getElementById(id);
    element.textContent = dollarFormat(price);
}

function updateProductPriceWithQuantityChange(data, productId) {
    const cartItems = data['cart_items'];
    const cartItemWithQuantityChange = cartItems.find(cartItem => cartItem.product.id === Number(productId));
    updateExtendedPriceOfCartItem(cartItemWithQuantityChange, productId);
    updatePriceSummary(cartItems);
}

// export function incrementQuantityHandler(form, productId) {
//     saveQuantity(form, productId, 1)
//         .then(data => {
//
//             if (Number(form["quantity"].value) > 0) {
//                 const minusIconElement = getMinusIconElementFromForm(form);
//                 minusIconElement.classList.remove("quantity-button-disabled");
//             }
//
//             // update the Price fields in the table.
//             updateProductPriceWithQuantityChange(data, productId);
//         })
//         .catch(error => console.log(error));
//
// }

// export function getMinusIconElement(quantitySection) {
//     return quantitySection.getElementsByClassName("minus-icon")[0];
// }



// function getEditInstructionsFormElement(form, product_id) {
//     return form['instructions'];
// }

// function getQuantityForm(product_id) {
//     const formId = product_id + "-quantity-form";
//     return document.getElementById(formId);
// }

// function getQuantity(product_id) {
//     return getQuantityForm(product_id)["quantity"].value;
// }

// export function saveInstruction(form, product_id) {
//     const instructionsElement = form['instructions'];
//     const instructions = instructionsElement.value;
//
//     // submit an API call to save the instruction
//     return updateCartItemDetails(getQuantity(product_id), product_id, instructions);
// }

// export function saveQuantity(form, product_id, increment) {
//     const newQuantity = Number(form['quantity'].value) + increment;
//     form['quantity'].value = newQuantity;
//
//     const instructions = getReadOnlyInstructions(getInstructionsForm(product_id), product_id);
//     return updateCartItemDetails(newQuantity, product_id, instructions);
// }

// export function prepareEditInstructionsHandler(form, product_id) {
//     showEditInstructions(form, product_id, true);
//     showReadOnlyInstructions(form, product_id, false);
// }

// function showEditInstructions(form, product_id, show) {
//     const element = form.getElementsByClassName("edit-instructions")[0];
//     element.style.display = show ? 'flex' : 'none';
//
//     const editIconElement = form.getElementsByClassName("edit-icon")[0];
//     editIconElement.style.display = show ? 'none' : 'block';
// }

// function showReadOnlyInstructions(form, product_id, show) {
//     getReadOnlyInstructionsElement(form, product_id).style.display = show ? 'block' : 'none';
// }

// function setReadOnlyInstructions(form, product_id, instructions) {
//     getReadOnlyInstructionsElement(form, product_id).innerText = instructions;
// }

// function setEditInstructions(form, product_id, instructions) {
//     getEditInstructionsFormElement(form, product_id).value = instructions;
// }

// export function cancelInstructionsHandler(form, product_id) {
//     showEditInstructions(form, product_id, false);
//     showReadOnlyInstructions(form, product_id, true);
//
//     // revert the edit instructions back to the original value
//     setEditInstructions(form, product_id, getReadOnlyInstructions(product_id));
// }

// export function saveInstructionsHandler(form, product_id) {
//     saveInstruction(form, product_id)
//         .then(data => {
//             // update the readonly element with the change
//             setReadOnlyInstructions(form, product_id, form['instructions'].value);
//
//             showReadOnlyInstructions(form, product_id, true);
//             showEditInstructions(form, product_id, false);
//         })
//         .catch(error => {
//             console.log("Failed to update cart item successfully - " + error);
//             // rollback the instruction change if an error occurred.
//         })
// }

