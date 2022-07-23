/**
 * To set font styles for the selected option in the Country dropdown field in profile form.
 * On the profile form this field is not required, therefore can't set the styles by using
 * the not valid selector. So instead set the styles based on the value.
 */

/**
 * listen for change on select element, if value is empty then set font styles to
 * match placeholder, otherwise set font styles to match other inputs
 */
function countrySelectColour() {
    $('#id_default_country').change(function() {
        if(!$(this).val()) {
            $(this).css({'color': '#6c757d', 'font-weight': '100', 'font-size': '90%'});
        } else {
            $(this).css({'color': '#1c1c1c', 'font-weight': '400', 'font-size': '1rem'});
        }
    });
}

/** on page load, set country select box to placeholder style if no value (i.e blank label)
 * and initialise countrySelectColour function to listen for change on the element
*/
document.addEventListener("DOMContentLoaded", function () {
    if(!$('#id_default_country').val()) {
        $('#id_default_country').css({'color': '#6c757d', 'font-weight': '100', 'font-size': '90%'});
    }
    countrySelectColour();
});