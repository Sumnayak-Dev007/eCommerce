$(document).ready(function () {
    $('.razrpay').on('click',(function (e) { 
        e.preventDefault();
        
        var first_name = $("[name='first_name']").val();
        var last_name = $("[name='last_name']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var country = $("[name='country']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        if (first_name == "" || last_name == "" || email == "" || phone == "" || address == "" || city == "" || state == "" || country == "" || pincode == "")
            {
                
                Swal.fire({
                    title: "Alert!",
                    text: "All Fields Are Mandatory!",
                    icon: "error",
                    confirmButtonText: "OK"
                  });
                  return false;
                  
            }
        else{

            $.ajax({
                type: "GET",
                url: "/get_amount/",
                success: function (response) {
                    console.log(response)


                    var options = {
                        "key": "rzp_test_SynZgwM03IZBsB", // Enter the Key ID generated from the Dashboard
                        "amount": response.amount * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "Suman Website Developer", //your business name
                        "description": "Transaction Interface", //Your Message
                        "image": "https://example.com/your_logo",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb){
                            alert(responseb.razorpay_payment_id);
                            data ={
                                "first_name":first_name, 
                                "last_name":last_name,
                                "email":email,
                                "phone":phone, 
                                "address":address, 
                                "city":city,
                                "state":state, 
                                "country":country, 
                                "pincode":pincode,
                                "payment_mode":"Paid by Razorpay",
                                "payment_id":responseb.razorpay_payment_id,
                                csrfmiddlewaretoken:token,
                            }
                            $.ajax({
                                type: "POST",
                                url: "/placeorder/",
                                data: data,
                                success: function (responsec) {
                                    Swal.fire({
                                        title: "Congratulations!",
                                        text: responsec.status,  // Ensure responsec.status is a valid string
                                        icon: "success",
                                        confirmButtonText: "OK"
                                      }).then(() => {
                                        window.location.href = "/my-orders/";  // Redirect after clicking OK
                                      });
                                }
                            });
                           
                        },
                        "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                            "name": first_name+" "+last_name, //your customer's name
                            "email": email, 
                            "contact": phone  //Provide the customer's phone number for better conversion rates 
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }
            });

            
        }
    }));

    
});