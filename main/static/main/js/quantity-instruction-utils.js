import {updateCartItemDetails} from "./cart-utils.js";

/**
 * Utils class for managing the quantity changes and instruction changes that are triggered from either the Menu page,
 * or a page containing order details (order-details.html).
 */

function getReadOnlyInstructionsElement(parentElement) {
    return parentElement.getElementsByClassName("read-only-instructions")[0];
}

function getReadOnlyInstructions(parentElement) {
    return getReadOnlyInstructionsElement(parentElement).innerText;
}

function showReadOnlyInstructions(parentElement, show) {
    getReadOnlyInstructionsElement(parentElement).style.display = show ? 'block' : 'none';
}

function setReadOnlyInstructions(parentElement, instructions) {
    getReadOnlyInstructionsElement(parentElement).innerText = instructions;
}

function showEditInstructions(parentElement, show) {
    const element = parentElement.getElementsByClassName("edit-instructions")[0];
    element.style.display = show ? 'flex' : 'none';

    if (show) {
        parentElement.querySelector('#instructions').value = getReadOnlyInstructions(parentElement);
    }

    const editIconElement = parentElement.getElementsByClassName("edit-icon")[0];
    editIconElement.style.display = show ? 'none' : 'block';
}

function getEditInstructions(parentElement) {
    return getEditInstructionsElement(parentElement).value;
}

function getEditInstructionsElement(parentElement) {
    return parentElement.querySelector('#instructions');
}

function setEditInstructions(parentElement, instructions) {
    getEditInstructionsElement(parentElement).value = instructions;
}

export function saveInstructionsHandler(parentElement, product_id) {
    saveInstruction(parentElement, product_id)
        .then(data => {
            // update the readonly element with the change
            setReadOnlyInstructions(parentElement, parentElement.querySelector('#instructions').value);
            showReadOnlyInstructions(parentElement, true);
            showEditInstructions(parentElement, false);
        })
        .catch(error => {
            console.log("Failed to update cart item successfully - " + error);
            // rollback the instruction change if an error occurred.
        })
}

export function cancelInstructionsHandler(parentElement) {
    showEditInstructions(parentElement, false);
    showReadOnlyInstructions(parentElement, true);

    // revert the edit instructions back to the original value
    setEditInstructions(parentElement, getReadOnlyInstructions(parentElement));
}

export function prepareEditInstructionsHandler(parentElement) {
    showEditInstructions(parentElement, true);
    showReadOnlyInstructions(parentElement, false);
}

export function incrementQuantityHandler(parentElement, productId) {
    return saveQuantity(parentElement, productId, 1)
        .then(data => {
            // make sure decrement button is enabled if it wasn't previously now that the quantity is > 0
            const minusQuantityElement = getMinusIconElement(parentElement);
            minusQuantityElement.classList.remove("quantity-button-disabled");
            return data;
        })
        .catch(error => console.log(error));
}

function getQuantityElement(parentElement) {
    return parentElement.querySelector('#quantity');
}

export function getQuantityValue(parentElement) {
    const quantityElement = getQuantityElement(parentElement);
    return Number(quantityElement.textContent);
}

function isDecrementQuantityAllowed(parentElement) {
    const minusIconElement = getMinusIconElement(parentElement);
    return !minusIconElement.classList.contains("quantity-button-disabled");
}

function setQuantityValue(parentElement, newValue) {
    const quantityText = getQuantityElement(parentElement);
    quantityText.textContent = newValue;
}

function saveQuantity(parentElement, productId, increment) {
    const newQuantity = getQuantityValue(parentElement) + increment;
    setQuantityValue(parentElement, newQuantity);
    // const instructions = getReadOnlyInstructions(getParentInstructionsElement(productId));
    const instructions = getReadOnlyInstructions(parentElement);
    return updateCartItemDetails(newQuantity, productId, instructions);
}

export function saveInstruction(parentElement, productId) {
    const instructions = getEditInstructions(parentElement);

    // submit an API call to save the instruction
    return updateCartItemDetails(getQuantityValue(parentElement), productId, instructions);
}

export function decrementQuantityHandler(parentElement, productId) {

    if (isDecrementQuantityAllowed(parentElement)) {
        return saveQuantity(parentElement, productId, -1)
            .then(data => {

                // const quantityForm = getQuantityForm(productId);
                if (getQuantityValue(parentElement) === 0) {
                    const minusIconElement = getMinusIconElement(parentElement);
                    minusIconElement.classList.add("quantity-button-disabled");
                }

                return data;
            })
            .catch(error => console.log(error));
    }

}

export function getMinusIconElement(parentElement) {
    return parentElement.getElementsByClassName("minus-icon")[0];
}

