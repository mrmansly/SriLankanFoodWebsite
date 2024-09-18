export function addClickListener(form, product_id, class_name, listenerFunction) {
    const classElements = form.getElementsByClassName(class_name);
    for (let element of classElements) {
        element.addEventListener("click", () => listenerFunction(product_id));
    }
}

