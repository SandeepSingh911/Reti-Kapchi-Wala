console.log("hello")

$(document).ready(function () {
    $('.plus-cart').click(function fn(e) {

        e.preventDefault();

        var id = $(this).attr("pid").toString();
        var elm = this.parentNode.children[2]

        $.ajax({
            type: "GET",
            url: "{% url 'myapp:plus_cart' %}",
            data: {
                prod_id: id
            },
            success: function (data) {
                elm.innerText = data.quantity
                document.getElementById("product_cost").innerText = data.product_amount
                document.getElementById("amount").innerText = data.amount
                document.getElementById("totalamount").innerText = data.total_amount

            }
        })
    })
})

$(document).ready(function () {
    $('.minus-cart').click(function fn(e) {

        e.preventDefault();

        var id = $(this).attr("pid").toString();
        var elm = this.parentNode.children[2]

        $.ajax({
            type: "GET",
            url: "{% url 'myapp:minus_cart' %}",
            data: {
                prod_id: id
            },
            success: function (data) {
                elm.innerText = data.quantity
                document.getElementById("product_cost").innerText = data.product_amount
                document.getElementById("amount").innerText = data.amount
                document.getElementById("totalamount").innerText = data.total_amount

            }
        })
    })
})

$(document).ready(function () {
    $('.remove-cart').click(function fn(e) {

        e.preventDefault();

        var id = $(this).attr("pid").toString();
        var elm = this


        $.ajax({
            type: "GET",
            url: "{% url 'myapp:remove_cart' %}",
            data: {
                prod_id: id
            },
            success: function (data) {
                document.getElementById("amount").innerText = data.amount
                document.getElementById("totalamount").innerText = data.total_amount
                elm.parentNode.parentNode.parentNode.parentNode.remove()

            }
        })
    })
})

$(document).ready(function () {
    $('.remove-wishlist').click(function fn(e) {

        e.preventDefault();

        var id = $(this).attr("pid").toString();
        var elm = this
        console.log(id)

        $.ajax({
            type: "GET",
            url: "{% url 'myapp:remove_wishlist' %}",
            data: {
                prod_id: id
            },
            success: function (data) {
                elm.parentNode.parentNode.parentNode.parentNode.remove()

            }
        })
    })
})


addEventListener("load", function () {
    setTimeout(hideURLbar, 0);
}, false);

function hideURLbar() {
    window.scrollTo(0, 1);
}