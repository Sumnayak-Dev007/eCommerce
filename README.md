## Integrate JQuery :

Download the latest jQuery (minified)

Go to 👉 jQuery Releases visit: https://releases.jquery.com/
.

Click on the latest minified link (something like jquery-3.7.1.min.js).

It will open in your browser as plain text.

Copy all content and paste it into a file in your Django project:

📂 static/js/jquery.js

2. Create a custom JavaScript file

Inside the same folder, create:

📂 static/js/custom.js

This is where you will write your own scripts.

Example inside custom.js:

// custom.js
$(document).ready(function() {
    console.log("Custom JS loaded with jQuery!");
});

3. Include scripts in base.html

At the bottom of your body tag (so page loads first, JS later), add:


start writing your required javascript in the custom.js in the same folder as jquery.js

## Integrate Alertify js:

visit :https://alertifyjs.com/guide.html

paste the first script at the bottom of base.html<!-- JavaScript -->
<script src="//cdn.jsdelivr.net/npm/alertifyjs@1.14.0/build/alertify.min.js"></script>
<br/>

paste the first two css links in the head of base.html

Go to components --> Notifier --> Position

paste the script at the bottom : and modify it like this :

<script>
  alertify.set('notifier','position', 'top-right');
   {% for msg in messages %} 
    alertify.success('{{msg}}');
  {%  endfor %}
</script>

that's it you will see all messages set in your views : )

# Integrating Razorpay Payment Gateway 🚀

This guide provides a step-by-step explanation for integrating Razorpay, a popular payment gateway, into your web application. By following these instructions, you can seamlessly enable payments via Razorpay and handle order processing efficiently.

---


## 🛠️ Steps to Integrate Razorpay

### 1. Create the Payment Button
Add a button to your HTML file to trigger the payment process:
```html
<button class="razrpay">Pay with Razorpay</button>

2. Include Razorpay Script
Add the Razorpay checkout script to your HTML file "checkout.html" under {% block script %} {% endblock %}
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>

3. Write Custom jQuery in checkout.js
Create a static JavaScript file (checkout.js) and include it in your HTML file below the Razorpay script in base.html/main.html below the script template tag:

<script src="static/js/checkout.js"></script>

📜 jQuery Code for Razorpay Integration
Below is the jQuery code to handle the Razorpay payment process. Place this code in your checkout.js file:

$(document).ready(function () {
    $('.razrpay').on('click', function (e) {
        e.preventDefault();

        // Collect user data from the form
        var fname = $("[name='first_name']").val();
        var lname = $("[name='last_name']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var country = $("[name='country']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        // Validate form fields
        if (!fname || !lname || !email || !phone || !address || !city || !state || !country || !pincode) {
            swal("Alert!", "All Fields Are Mandatory!", "error");
            return false;
        }

        // Fetch payment amount from the backend
        $.ajax({
            type: "GET",
            url: "/get_amount/",
            success: function (response) {
                console.log(response);

                // Razorpay options
                var options = {
                    "key": "KEY_ID", // Enter your Razorpay Key ID
                    "amount": response.amount * 100, // Amount in paise
                    "currency": "INR",
                    "name": "Suman Website Developer", // Your business name
                    "description": "Transaction Interface", // Payment description
                    "image": "https://example.com/your_logo", // Your logo URL
                    "handler": function (responseb) {
                        // Handle payment success
                        alert(responseb.razorpay_payment_id);

                        // Prepare order data
                        var data = {
                            "fname": fname,
                            "lname": lname,
                            "email": email,
                            "phone": phone,
                            "address": address,
                            "city": city,
                            "state": state,
                            "country": country,
                            "pincode": pincode,
                            "payment_mode": "Paid by Razorpay",
                            "payment_id": responseb.razorpay_payment_id,
                            csrfmiddlewaretoken: token,
                        };

                        // Send order data to the backend
                        $.ajax({
                            type: "POST",
                            url: "/placeorder/",
                            data: data,
                            success: function (responsec) {
                                swal("Congratulations!", responsec.status, "success", {
                                    button: "OK",
                                }).then(() => {
                                    window.location.href = '/my-orders/';
                                });
                            }
                        });
                    },
                    "prefill": {
                        "name": fname + " " + lname,
                        "email": email,
                        "contact": phone,
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                };

                // Open Razorpay payment interface
                var rzp1 = new Razorpay(options);
                rzp1.open();
            }
        });
    });
});

🧩 Step-by-Step Explanation
1. Prepare User Data
Collect user details from the form fields:

var fname = $("[name='first_name']").val();
var lname = $("[name='last_name']").val();
var email = $("[name='email']").val();
var phone = $("[name='phone']").val();
var address = $("[name='address']").val();
var city = $("[name='city']").val();
var state = $("[name='state']").val();
var country = $("[name='country']").val();
var pincode = $("[name='pincode']").val();
var token = $("[name='csrfmiddlewaretoken']").val();

2. Fetch Payment Amount
Use an AJAX call to fetch the total amount from the backend:
$.ajax({
    type: "GET",
    url: "/get_amount/",
    success: function (response) {
        console.log(response);
    }
});

3. Configure Razorpay Options
Set up the Razorpay options object with your business details, payment amount, and user data:

To Get your API key: 
First of all clicling on you profile --> enable test mode.
Go to : Razorpay Dashboard--> Settings --> API key --> copy your API ket paste below

var options = {
    "key": "KEY_ID",
    "amount": response.amount * 100, 
    "currency": "INR",
    "name": "Suman Website Developer",
    "description": "Transaction Interface",
    "image": "https://example.com/your_logo",
    "handler": function (responseb) {
        // Handle payment success
    },
    "prefill": {
        "name": fname + " " + lname,
        "email": email,
        "contact": phone,
    },
    "theme": {
        "color": "#3399cc"
    }
};

4. Send Order Data to Backend
After a successful payment, send the order details to the backend for processing:
handler(resposneb){
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
        swal("Congratulations!", responsec.status, "success", {
            button: "OK",
        }).then(() => {
            window.location.href = '/my-orders/';
        });
    }
});
}


Make sure you are receiving this payment_id and payment_mode in the backend to add it in the Order table
add JsonResponse in the backend for this paymeny_mode:

payMode = request.POST.get('payment_mode')
        if (payMode == "Paid by Razorpay" or payMode == "Paid by Paypal" ):
            return JsonResponse({'status':"Your order has been placed successfully"})




🔗 Backend Integration
1. Add URL Path
Include the get_amount/ path in your urls.py:
path('get_amount/', views.get_amount, name='amount'),

2. Write View Logic
Implement the get_amount view to calculate the total amount:

def get_amount(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price = total_price + item.Product.selling_price * item.product_qty

    return JsonResponse({
        'amount': total_price
    })

### 3. **Generate Razorpay Key**
To integrate Razorpay, you need to generate a **Key ID** and **Key Secret** from the Razorpay Dashboard. Follow these steps:

1. **Log in to Razorpay Dashboard**:
   - Go to [Razorpay](https://razorpay.com/) and log in to your account.

2. **Select Mode**:
   - Choose between **Test Mode** (for testing) or **Live Mode** (for production).

3. **Navigate to API Keys**:
   - Go to **Account & Settings → API Keys** (under Website and app settings).

4. **Generate Key**:
   - Click on **Generate Key** to create a new **Key ID** and **Key Secret**.

5. **Use the Key**:
   - Replace `"KEY_ID"` in the Razorpay options object with your generated **Key ID**:
     ```javascript
     "key": "YOUR_KEY_ID", // Replace with your Razorpay Key ID
     ```

🎉 Success!
Once integrated, users can make payments via Razorpay, and the order details will be processed and stored in your backend. Redirect users to the my-orders/ page to view their order receipts.

### 4. **Configure Razorpay Options**
After generating your Razorpay Key, configure the Razorpay options object with the following details:

1. **Set the Amount**:
   - Use the amount fetched from the backend via AJAX (`response.amount`):
     ```javascript
     "amount": response.amount * 100, // Amount in paise (e.g., 50000 = ₹500)
     ```

2. **Add Business Details**:
   - Fill in your business name, description, and logo:
     ```javascript
     "name": "Suman Website Developer", // Your business name
     "description": "Transaction Interface", // Payment description
     "image": "https://example.com/your_logo", // Your logo URL
     ```

3. **Prefill User Data**:
   - Automatically fill in the customer's details using the data collected from the form:
     ```javascript
     "prefill": {
         "name": fname + " " + lname, // Customer's full name
         "email": email, // Customer's email
         "contact": phone // Customer's phone number
     },
     ```

4. **Customize Theme (Optional)**:
   - You can customize the Razorpay payment modal's theme by setting a color:
     ```javascript
     "theme": {
         "color": "#3399cc" // Set your preferred color
     }
     ```

---

### 5. **Handle Payment Success**
Once the payment is successful, the `handler` function will be triggered. Inside this function:

1. **Capture Payment ID**:
   - Extract the `razorpay_payment_id` from the response:
     ```javascript
     "handler": function (responseb) {
         alert(responseb.razorpay_payment_id); // Payment ID
     }
     ```

2. **Prepare Order Data**:
   - Collect all the necessary order details to send to the backend:
     ```javascript
     var data = {
         "fname": fname,
         "lname": lname,
         "email": email,
         "phone": phone,
         "address": address,
         "city": city,
         "state": state,
         "country": country,
         "pincode": pincode,
         "payment_mode": "Paid by Razorpay",
         "payment_id": responseb.razorpay_payment_id,
         csrfmiddlewaretoken: token,
     };
     ```

3. **Send Order Data to Backend**:
   - Use an AJAX POST request to send the order details to the backend:
     ```javascript
     $.ajax({
         type: "POST",
         url: "/placeorder/",
         data: data,
         success: function (responsec) {
             swal("Congratulations!", responsec.status, "success", {
                 button: "OK",
             }).then(() => {
                 window.location.href = '/my-orders/'; // Redirect to orders page
             });
         }
     });
     ```

---

### 6. **Backend Implementation**
1. **Add URL Path**:
   - Include the `placeorder/` path in your `urls.py`:
     ```python
     path('placeorder/', views.placeorder, name='placeorder'),
     ```

2. **Write View Logic**:
   - Implement the `placeorder` view to process the order details and save them to the database:
     ```python
     from django.http import JsonResponse

     def placeorder(request):
         if request.method == 'POST':
             # Extract data from the request
             fname = request.POST.get('fname')
             lname = request.POST.get('lname')
             email = request.POST.get('email')
             phone = request.POST.get('phone')
             address = request.POST.get('address')
             city = request.POST.get('city')
             state = request.POST.get('state')
             country = request.POST.get('country')
             pincode = request.POST.get('pincode')
             payment_mode = request.POST.get('payment_mode')
             payment_id = request.POST.get('payment_id')

             # Save order details to the database
             order = Order.objects.create(
                 first_name=fname,
                 last_name=lname,
                 email=email,
                 phone=phone,
                 address=address,
                 city=city,
                 state=state,
                 country=country,
                 pincode=pincode,
                 payment_mode=payment_mode,
                 payment_id=payment_id,
             )

             # Return success response
             return JsonResponse({
                 'status': 'Order placed successfully!',
             })
     ```

---

### 7. **Redirect to Orders Page**
After successfully placing the order, redirect the user to the `my-orders/` page where they can view their order receipts:
```javascript
window.location.href = '/my-orders/';
```

🎉 Success!
Congratulations! You have successfully integrated Razorpay into your website. Users can now make payments, and their order details will be processed and stored in your backend.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Razorpay Documentation

Special thanks to the developers who contributed to this integration.

## How to set Navbar active :
<ul class="navbar">
  <li class="{% if request.resolver_match.url_name == 'home' %}active{% endif %}">
      <a href="{% url 'home' %}">Home</a>
  </li>



## Integration with PayPal:
JavaScripts SDK method : https://developer.paypal.com/sdk/js/reference/#buttons
add this script in the page before body tag
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID"></script>

Navigate to PayPal Developers Dashboard >> Testing Tools >> Sandbox Accounts >> create Account >> Create App >> CLIENT_ID 
 Copy and paste in place of CLIENT_ID

 Create Pay pal Button 
 <div id="paypal-button-container"></div>

 Paste this script below paypal script 
 <script>
  paypal.Buttons({
    createOrder: function(data, actions) {
      return actions.order.create({
        purchase_units: [{
          amount: {
            value: '10.00' // The amount you want to charge
          }
        }]
      });
    },
    onApprove: function(data, actions) {
      return actions.order.capture().then(function(details) {
        alert('Transaction completed by ' + details.payer.name.given_name);
      });
    }
  }).render('#paypal-button-container'); // Render the button into the div
</script>

replace the price with {{ total_price }}

# Check If Button is Displayed on Browser

# include this in settings.py to prevent browser from opening about:blank in different tab:: SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'

# Create a Personal sandbox account to test if users are able to pay or not
 use their email and password to test

# Check Your Transaction Details Here https://developer.paypal.com/dashboard/notifications


# Integrate Sweet Alert

# Use CDN:

```html
<script src="https://unpkg.com/sweetalert/dist/sweetalert.min.js"></script>
```
2. Start using it in your JavaScript:

swal("Good job!", "You clicked the button!", "success");



Made with ❤️ by Suman. Happy coding! 🚀
