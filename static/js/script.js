/**
 * This file contains functions used throughout the site: select box sorting for shop
 * and markets pages, quantity inputs on cart and checkout, back to top btn, file name
 * for image upload field for markets and products.
 */

/**
 * Select dopdown box for sorting options on Shop and Markets pages. If it exists, listen for change on element.
 * On change, get current URL + get value from the select option. If value not 'reset', get sort and direction 
 * from select option value, set these into the search parameters on the url, then put new url into window
 * Otherwise, clear any sort and direction so that all results will be shown
 * Credit: initial code from Code Institute, amended/refactored
 *  */ 
function selectBoxSorting() { 
    if(document.getElementById("sorting-selector")) {
        document.getElementById("sorting-selector").addEventListener("change", function() {
            let currentUrl = new URL(window.location);
            if(this.value != "reset"){
                currentUrl.searchParams.set("sort", this.value.split("_")[0]);
                currentUrl.searchParams.set("direction", this.value.split("_")[1]);
                window.location.replace(currentUrl);
            } else {
                currentUrl.searchParams.delete("sort");
                currentUrl.searchParams.delete("direction");
                window.location.replace(currentUrl);
            }
        });
    }
}

/**
 * Handles the quantity input on the product details page and cart page in products/cart apps.
 * If quantity buttons exist, call enableDisableQtyBtns to check if input element value is outside range,
 * or call changeInputValue to increase/decrease input element value.
 * - on page load, call enableDisableQtyBtns so minus btn disabled (as input value is 1 on page load)
 * - on click event of button, call changeInputValue
 * - on change of input box (user using up/down arrows and not the buttons), call enableDisableQtyBtns
 *  */ 
function handleQuantityInput() {
    if(document.querySelectorAll(".btn-qty")){
        let quantityBtns = document.querySelectorAll(".btn-qty");
        for (let button of quantityBtns) {
            let itemId = button.getAttribute("data-item_id");
            enableDisableQtyBtns(itemId);
        }
        quantityBtns.forEach(button => button.addEventListener("click", function(event){
            event.preventDefault();
            let itemId = this.getAttribute("data-item_id");
            let direction = this.getAttribute("id").split("-")[0];
            changeInputValue(itemId, direction);
            }));
        $('.qty_input').change(function() {
            let itemId = this.getAttribute("data-item_id");
            enableDisableQtyBtns(itemId);
        });
    }
}

/**
 * Change the value in the quantity input box, either up or down depending on direction, then 
 * call enableDisableQtyBtns, passing itemId
 * @param {string} itemId the id of the product, to get the relevant input element
 * @param {string} direction the direction of change, either increment or decrement
 */
function changeInputValue(itemId, direction) {
    let inputElement = document.getElementById(`id_qty_${itemId}`);
    let oldValue = parseInt(inputElement.value);
    if(direction === "decrement") {
        inputElement.value = -- oldValue;
    } else if(direction === "increment") {
        inputElement.value = ++ oldValue;
    }
    enableDisableQtyBtns(itemId);
}

/**
 * Set disabled attribute on quantity buttons to true or false, depending on whether
 * the current value in the input box is inside or outside of the allowed range.
 * Credit: initial code from Code Institute, amended/refactored.
 * @param {string} itemId the id of the product, to get the relevant input element
 */
function enableDisableQtyBtns(itemId) {
    let inputElement = document.getElementById(`id_qty_${itemId}`);
    let currentValue = parseInt(inputElement.value);
    let minusDisabled = currentValue < 2;
    let plusDisabled = currentValue > 9;
    document.getElementById(`decrement-qty_${itemId}`).disabled = minusDisabled;
    document.getElementById(`increment-qty_${itemId}`).disabled = plusDisabled;
}

/**
 * Used in the cart page to submit the updated quantity. Using requestSubmit() in order to 
 * invoke html form constraint validation so min/max on form input is validated.
 */
function submitQuantityUpdateForm() {
    if($('.update-link')) {
        $('.update-link').click(function() {
            $(this).prev('.update-form')[0].requestSubmit();
        });
    }
}

/**
 * Used in the cart page to remove item. When link is clicked, get csrf token and create url using 
 * item id, post the data to the url, and reload the page when done.
 * Credit: Code Institute, with some modifications
 */
function removeItemFromCart() {
    if ($(".remove-link")) {
        $(".remove-item").click(function () {
            let csrfToken = this.getAttribute("data-csrf");
            let itemId = this.getAttribute("id").split("remove_")[1];
            let url = `/cart/remove/${itemId}/`;
            let data = {
                "csrfmiddlewaretoken": csrfToken
            };
            $.post(url, data)
                .done(function () {
                    location.reload();
                });
        });
    }
}

/**
 * listen for click on link, scroll back to top of page
 */
function scrollBackToTop() {
    if(document.querySelector(".btt-link")){
        document.querySelector(".btt-link").addEventListener("click", function() {
            window.scrollTo(0,0);
        });
    }
}

/**
 * Listen for change on file input for image upload on product + market form. On change,
 * set text in the paragraph below it to show the name of the file being uploaded.
 */
     function fileInputShowFileName() {
        if($("#id_image")){
            $("#id_image").change(function() {
                let file = $("#id_image")[0].files[0];
                $("#filename").text(`Image will be set to: ${file.name}`);
            });    
        }
    }

/** initialise the links/buttons that are listening for click/change events
*/
document.addEventListener("DOMContentLoaded", function () {
    selectBoxSorting();
    handleQuantityInput();
    submitQuantityUpdateForm();
    removeItemFromCart();
    scrollBackToTop();
    fileInputShowFileName();
});