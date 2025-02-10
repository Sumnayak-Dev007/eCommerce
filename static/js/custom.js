$(document).ready(function () {

    // Add to Cart
    $('.addtoCart').on('click', function (e) { 
        e.preventDefault();

        var $productData = $(this).closest('.product_data');
        var product_id = $productData.find('.prod_id').val();
        var prod_qty = $productData.find('#quantity').val();
        var token = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            type: "POST",
            url: "/add-to-cart/",
            data: {
                'product_id': product_id,
                'prod_qty': prod_qty,
                csrfmiddlewaretoken: token
            },
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", token);  // Add CSRF token to the header
            },
            success: function (response) {
                console.log(response);
                alertify.success(response.status);
            },
            error: function (xhr, status, error) {
                console.error("Error:", status, error);
                alertify.error('There was an issue with your request. Please try again.');
            }
        });
        
    });

    // Update Cart Quantity
    $('.updateQuantity').on('click', function (e) { 
        e.preventDefault();

        var $productData = $(this).closest('.prod_val');
        var product_id = $productData.find('.prodss_id').val();
        var prod_qty = $productData.find('.prodss').val();
        var token = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            type: "POST",
            url: "/updatecart/",
            data: {
                'product_id': product_id,
                'prod_qty': prod_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response);
                alertify.success(response.status);
            },
            error: function (xhr, status, error) {
                console.error("Error:", status, error);
                alertify.error('There was an issue with your request. Please try again.');
            }
        });
        
    });

    $('.remove-btn').on('click',(function (e) { 
        e.preventDefault();
        var $productData = $(this).closest('.prod_val');
        var product_id = $productData.find('.prodss_id').val();
        var token = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            type: "POST",
            url: "/deletecart/",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status);
                location.reload();
            },
            error: function (xhr, status, error) {
                console.error("Error:", status, error);
                alertify.error('There was an issue with your request. Please try again.');
            }
        });
    }));

    $('.addto_w_list').on('click',(function (e) { 
        e.preventDefault();
        
        var $productData = $(this).closest('.product_data');
        var product_id = $productData.find('.prod_id').val();
        var token = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            type: "POST",
            url: "/add_w_list/",
            data: {
                'prod_id':product_id,
                csrfmiddlewaretoken:token
            },
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", token);  // Add CSRF token to the header
            },
            success: function (response) {
                console.log(response);
                alertify.success(response.status);
            },
            error: function (xhr, status, error) {
                console.error("Error:", status, error);
                alertify.error('There was an issue with your request. Please try again.');
            }
        });
    }));

    $('.remove_wish').on('click',(function (e) { 
        e.preventDefault();
        
        var $Data = $(this).closest('.wish_data');
        var prod_id = $Data.find('.prodss_id').val();
        var token = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            type: "POST",
            url: "/remove_wish/",
            data: {
                'prod_id':prod_id,
                csrfmiddlewaretoken:token
            },
            success: function (response) {
                console.log(response);
                alertify.success(response.status);
                location.reload();
            },
            error: function (xhr, status, error) {
                console.error("Error:", status, error);
                alertify.error('There was an issue with your request. Please try again.');
            }
        });
    }));

     
});
