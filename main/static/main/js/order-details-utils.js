// This utils file holds functionality that is tightly coupled with id's in order-details.html
import {updateCartItemDetails} from './cart-utils.js';
import {
    calculateExtendedPrice,
    calculateGSTPrice,
    calculateRevisedSubTotalPrice,
    calculateTotalPrice
} from "./price-calculator.js";
import {removePriceFormatting, dollarFormat} from "./formatting-utils.js";

function getReadOnlyInstructionsElement(product_id) {
    return getInstructionsForm(product_id).getElementsByClassName("instructions")[0];
}

function getReadOnlyInstructions(product_id) {
    return getReadOnlyInstructionsElement(product_id).innerText;
}

function getInstructionsForm(product_id) {
    const formId = product_id + "-instructions-form";
    return document.getElementById(formId);
}

function getEditInstructionsFormElement(product_id) {
    const form = getInstructionsForm(product_id);
    return form['instructions'];
}

function getQuantityForm(product_id) {
    const formId = product_id + "-quantity-form";
    return document.getElementById(formId);
}

function getQuantity(product_id) {
    return getQuantityForm(product_id)["quantity"].value;
}

export function saveInstruction(product_id) {
    const form = getInstructionsForm(product_id);

    const instructionsElement = form['instructions'];
    const instructions = instructionsElement.value;

    // submit an API call to save the instruction
    return updateCartItemDetails(getQuantity(product_id), product_id, instructions);
}

export function saveQuantity(product_id, increment) {
    const form = getQuantityForm(product_id);

    const newQuantity = Number(form['quantity'].value) + increment;
    form['quantity'].value = newQuantity;

    const instructions = getReadOnlyInstructions(product_id);
    return updateCartItemDetails(newQuantity, product_id, instructions);
}

export function prepareEditInstructionsHandler(product_id) {
    showEditInstructions(product_id, true);
    showReadOnlyInstructions(product_id, false);
}

function showEditInstructions(product_id, show) {
    const form = getInstructionsForm(product_id);
    const element = form.getElementsByClassName("edit-instructions")[0];
    element.style.display = show ? 'flex' : 'none';

    const editIconElement = form.getElementsByClassName("edit-icon")[0];
    editIconElement.style.display = show ? 'none' : 'block';
}

function showReadOnlyInstructions(product_id, show) {
    getReadOnlyInstructionsElement(product_id).style.display = show ? 'block' : 'none';
}

function setReadOnlyInstructions(product_id, instructions) {
    getReadOnlyInstructionsElement(product_id).innerText = instructions;
}

function setEditInstructions(product_id, instructions) {
    getEditInstructionsFormElement(product_id).value = instructions;
}

export function cancelInstructionsHandler(product_id) {
    showEditInstructions(product_id, false);
    showReadOnlyInstructions(product_id, true);

    // revert the edit instructions back to the original value
    setEditInstructions(product_id, getReadOnlyInstructions(product_id));
}

export function saveInstructionsHandler(product_id) {
    saveInstruction(product_id)
        .then(data => {
            const instructionsForm = getInstructionsForm(product_id);
            // update the readonly element with the change
            const readonlyInstructionsElement = getReadOnlyInstructionsElement(product_id);
            readonlyInstructionsElement.innerText = instructionsForm['instructions'].value;

            showReadOnlyInstructions(product_id, true);
            showEditInstructions(product_id, false);
        })
        .catch(error => {
            console.log("Failed to update cart item successfully - " + error);
            // rollback the instruction change if an error occurred.
        })
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
    const discount = removePriceFormatting(document.getElementById("summaryDiscount").textContent);
    const revisedSubTotalPrice = calculateRevisedSubTotalPrice(subTotalPrice, discount);
    updateElementWithPrice('summaryRevisedSubTotal', revisedSubTotalPrice);
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

export function incrementQuantityHandler(productId) {
    saveQuantity(productId, 1)
        .then(data => {

            const quantityForm = getQuantityForm(productId);
            if (Number(quantityForm["quantity"].value) > 0) {
                const minusIconElement = getMinusIconElementFromForm(quantityForm);
                minusIconElement.classList.remove("quantity-button-disabled");
            }

            // update the Price fields in the table.
            updateProductPriceWithQuantityChange(data, productId);
        })
        .catch(error => console.log(error));

}

export function getMinusIconElementFromForm(form) {
    return form.getElementsByClassName("minus-icon")[0];
}

/**
 * The event listener for handling clicks on the minus icon has not been removed even if it's been "disabled".
 * Therefore, this check needs to be in place before a minus quantity is allowed to be processed.
 *
 * @param productId
 * @returns {boolean}
 */
function isDecrementQuantityAllowed(productId) {
    const form = getQuantityForm(productId);
    const minusIconElement = getMinusIconElementFromForm(form);
    return !minusIconElement.classList.contains("quantity-button-disabled");
}

export function decrementQuantityHandler(productId) {

    if (isDecrementQuantityAllowed(productId)) {
        saveQuantity(productId, -1)
            .then(data => {

                const quantityForm = getQuantityForm(productId);
                if (Number(quantityForm["quantity"].value) === 0) {
                    const minusIconElement = getMinusIconElementFromForm(quantityForm);
                    minusIconElement.classList.add("quantity-button-disabled");
                }

                // update the Price fields in the table.
                updateProductPriceWithQuantityChange(data, productId);
            })
            .catch(error => console.log(error));
    }
}
