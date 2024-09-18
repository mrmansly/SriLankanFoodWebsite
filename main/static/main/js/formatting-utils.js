const dollarFormatter = new Intl.NumberFormat('en-AU', {
    style: 'currency',
    currency: 'AUD'
});

export function removePriceFormatting(value) {
    const index = value.indexOf("$");
    if (index > -1) {
        // handle +ve and -ve values (where $ sign is 2nd char in string)
        value = value.substring(0,index) + value.substring(index+1);
    }
    return Number(value);
}

export function dollarFormat(value) {
    return dollarFormatter.format(value);
}