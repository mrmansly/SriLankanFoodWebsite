// This utils file holds common functions that are repeated for each product in the food menu and tightly coupled with
// id's in product-item-row.html.
import {updateCartItemDetails} from './cart-utils.js';

export function incrementQuantityHandler(productId) {
    saveQuantity(productId, 1)
        .then(data => {
            // make sure decrement button is enabled if it wasn't previously now that the quantity is > 0
            const form = getProductItemForm(productId);
            const minusQuantityElement = getMinusIconElementFromForm(form);
            minusQuantityElement.classList.remove("quantity-button-disabled");
            return data;
        })
        .catch(error => console.log(error));
}

function getMinusIconElementFromForm(form) {
    return form.getElementsByClassName("minus-icon")[0];
}

export function decrementQuantityHandler(productId) {
    const form = getProductItemForm(productId);
    const minusQuantityElement = getMinusIconElementFromForm(form);
    if (!minusQuantityElement.classList.contains("quantity-button-disabled")) {
        saveQuantity(productId, -1)
            .then(data => {
                if (Number(form["quantity"].value) === 0) {
                    // disable the minus button to prevent quantity going into -ve.
                    minusQuantityElement.classList.add("quantity-button-disabled");
                }
                return data;
            })
            .catch(error => console.log(error));
    }
}

export function getProductItemForm(productId) {
    return document.getElementById("product-item-form-"+productId);
}

function saveQuantity(productId, increment) {
    const form = getProductItemForm(productId);
    const newQuantity = Number(form['quantity'].value) + increment;
    form["quantity"].value = newQuantity;
    const instructions = form["instructions"].value;
    return updateCartItemDetails(newQuantity, productId, instructions);
}

export function setUpdateButtonDisabledStatus(form, disableFlag) {
    const updateButton = form.getElementsByClassName("update-button")[0];
    updateButton.disabled = disableFlag;
}

export function addListenerForFormSubmit(productId) {
    const formElement = getProductItemForm(productId);

    formElement.addEventListener("submit", (event) => {
        const formData = new FormData(event.target);
        event.preventDefault();
        updateCartItemDetails(formData.get('quantity'), formData.get('product_id'), formData.get('instructions'))
            .then(data => {
                // disable the Update button to indicate the save has taken place
                setUpdateButtonDisabledStatus(formElement, true);
                return data;
            })
            .catch(error => {
                console.log("Form Submit Button: " + error);
            });
    });
}

