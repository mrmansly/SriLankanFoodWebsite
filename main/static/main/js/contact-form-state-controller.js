
const CATEGORY_TYPE = {
    "REVIEW": 1,
    "FEEDBACK": 2,
    "QUESTION": 3,
    "WEBSITE": 4
};

function setState(typeInput, productInput, ratingInput) {
    switch ( Number(typeInput.value) ) {
        case CATEGORY_TYPE.REVIEW:
            productInput.parentElement.classList.remove('hide-field');
            ratingInput.parentElement.classList.remove('hide-field');
            // all fields enabled
            break;
        case CATEGORY_TYPE.FEEDBACK:
            // all fields enabled (excluding Rating)
            productInput.parentElement.classList.remove('hide-field');
            ratingInput.parentElement.classList.add('hide-field');
            break;
        case CATEGORY_TYPE.QUESTION:
            productInput.parentElement.classList.remove('hide-field');
            ratingInput.parentElement.classList.add('hide-field');
            break;
        // all fields enabled (excluding Rating)
        case CATEGORY_TYPE.WEBSITE:
        // all fields enabled (excluding Product and Rating)
            productInput.parentElement.classList.add('hide-field');
            ratingInput.parentElement.classList.add('hide-field');
            break;
    }
}