export function calculateExtendedPrice(unitPrice, quantity) {
    return Number(unitPrice * quantity);
}

export function calculateRevisedSubTotalPrice(subTotalPrice, discount) {
    return Number(subTotalPrice + discount);
}

export function calculateGSTPrice(price) {
    return Number(0.1 * price);
}

export function calculateTotalPrice(revisedSubTotalPrice, gstPrice) {
    return Number(revisedSubTotalPrice + gstPrice);
}
