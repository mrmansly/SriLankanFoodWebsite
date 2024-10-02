// helper function for adding click listeners to order items and menu items.
export function addClickListener(parentElement, productId, className, listenerFunction) {
    const classElements = parentElement.getElementsByClassName(className);
    for (let element of classElements) {
        element.addEventListener("click", () => listenerFunction(parentElement, productId));
    }
}

