function colorStock(product_id) {
    let colorBotton = document.querySelectorAll('.color-variable')
    colorBotton.forEach(function (element) {
        element.addEventListener('click', function () {
            event.preventDefault()
            colorBotton.forEach(function (element) {
                element.classList.remove('border-danger')
            })
            element.classList.add('border-danger')
            $.ajax({
                url: '/product-color-stock/',
                method: 'GET',
                data: {
                    product_id: product_id,
                    product_color: element.getAttribute('data-color')
                },
                success: function (data) {
                    let colorStock = document.querySelector('#color-stock')
                    let colorTitle = document.querySelector('#color-title')
                    colorStock.innerHTML = data.stock
                    colorTitle.innerHTML = data.title
                    colorTitle.setAttribute('style', `color: ${data.color};`)
                },
            })

        })
    })
}

function setParentId(product_id) {
    let parentId = document.querySelector('#parent-id')
    parentId.value = product_id
    document.querySelector('#for-view').scrollIntoView({behavior: 'smooth'})
    document.querySelector(('#comment-text')).focus()
}

function addComment(product_id) {
    event.preventDefault()
    let parentId = document.querySelector('#parent-id')
    let comments = document.querySelector('#comments')
    let comment = document.querySelector('#comment-text')
    $.ajax({
        url: '/add-comment/',
        method: 'GET',
        data: {
            product_id: product_id,
            comment: comment.value,
            parent: parentId.value,
        },
        success: function (res) {
            $('#comments-cont').html(res)
            comment.value = ''
            if (parentId.value === '') {
                document.querySelector('#comment-start').scrollIntoView({behavior: 'smooth'})
            } else {
                document.querySelector('#comment-box' + parentId.value).scrollIntoView({behavior: 'smooth'})
            }
        },
    })

}

function orderFilterStyle() {
    let currentUrl = window.location.href
    for (let link of document.querySelectorAll('.order-filter')) {
        if (currentUrl.includes('?order-by=' + link.getAttribute('data-filter'))) {
            link.classList.add('active')
        }
    }
}

window.onload = orderFilterStyle

function orderBy(type) {
    event.preventDefault()
    const form = document.querySelector('#order-form')
    const input = document.querySelector('#order-type')
    console.log(type)
    input.value = type
    console.log(input.value)
    form.submit()
}

function sliderRange(max) {

    if ($('#steps-slider').length) {
        var slider = document.getElementById('steps-slider');

        noUiSlider.create(slider, {
            direction: 'rtl',
            start: [0, max],
            connect: true,
            step: 100000,
            range: {
                'min': 0,
                'max': max
            }
        });

        slider.noUiSlider.on('update', function (values) {
            $('#encode4365gbf265g43d-range-from').text(Math.round(values[0]));
            $('#encode4365gbf265g43d-range-to').text(Math.round(values[1]));
        });
    }
}

function priceFilter() {
    event.preventDefault()
    const lowPrice = document.querySelector('#low-price')
    const highPrice = document.querySelector('#high-price')
    const lowPriceVal = document.querySelector('.low-price-value')
    const highPriceVal = document.querySelector('.high-price-value')
    const form = document.querySelector('#price-filter')
    lowPrice.value = lowPriceVal.innerHTML
    highPrice.value = highPriceVal.innerHTML
    form.submit()

}