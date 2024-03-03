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
    input.value = type
    form.submit()
}

function sliderRange(max) {
    const currentUrl = window.location.href;
    let url = new URL(currentUrl)
    let params = url.searchParams
    let lowPrice = params.get('low-price')
    let highPrice = params.get('high-price')

    if ($('#steps-slider').length) {
        let slider = document.getElementById('steps-slider');

        noUiSlider.create(slider, {
            direction: 'rtl',
            start: [lowPrice || 0, highPrice || max],
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

function addProductToFavorite(id) {
    let likeButton = $('#like')
    event.preventDefault()
    $.ajax({
        url: '/add-favorite/',
        method: 'GET',
        data: {
            product_id: id,
        },
        success: function (data) {
            if (data.liked) {
                likeButton.removeClass('bi-heart')
                likeButton.addClass('bi-heart-fill')
                setTimeout(function () {
                    alert('محصول به لیست مورد علاقه های شما اضافه شد.')
                }, 500)

            } else {
                likeButton.removeClass('bi-heart-fill')
                likeButton.addClass('bi-heart')
                setTimeout(function () {
                    alert('محصول از لیست مورد علاقه های شما حذف شد.')
                }, 500)
            }
        },
    })

}

function tabStyle() {
    let currentUrl = window.location.href
    let tabs = document.querySelectorAll('.profile-tab')
    tabs.forEach(function (element) {
        console.log(element.getAttribute('href'))
        console.log(currentUrl)
        if (currentUrl.includes(element.getAttribute('href'))) {
            element.classList.add('active')
        }
    })
}

function selectBoxOptions() {
    let citySelectBox = $('#id_city')
    let provincesSelectBox = $('#id_province')
    citySelectBox.html('')
    provincesSelectBox.on('change', function () {
        let provinceId = this.value
        $.ajax({
            url: '/get-city/',
            method: 'GET',
            data: {
                province_id: provinceId,
            },
            success: function (data) {
                citySelectBox.html('')
                for (let city of data.cities) {
                    let option = document.createElement('option')
                    option.value = city[1]
                    option.innerHTML = city[0]
                    citySelectBox.append(option)
                }
            },
        })
    })

}

function addAddress() {
    event.preventDefault()
    let provinceId = document.querySelector('#id_province')
    let cityId = document.querySelector('#id_city')
    let address = document.querySelector('#id_address')
    let postalCode = document.querySelector('#id_postal_code')
    let receiverName = document.querySelector('#id_receiver_name')
    let addressId = document.querySelector('#address-id')
    let addressIdValue = null
    let submitButton = document.querySelector('#submit-button')
    if (addressId){addressIdValue = addressId.value}
    $.ajax({
        url: '/add-address/',
        method: 'GET',
        data: {
            province_id: provinceId.value,
            city_id: cityId.value,
            address: address.value,
            postal_code: postalCode.value,
            receiver_name: receiverName.value,
            address_id: addressIdValue,
            submit_type: submitButton.value,
        },
        success: function (res) {
            console.log(res)
            cityId.value = ''
            address.value = ''
            postalCode.value = ''
            receiverName.value = ''
            let container = $('#address-cont')
            container.html(res)
            let idInput = document.querySelector('#address-id')
            if (idInput){idInput.value = ''}
            submitButton.innerHTML = 'ثبت'
            submitButton.blur()
            submitButton.value = 'add'
            $('.address-title').text('افزودن آدرس جدید')

        },
    })
}

function deleteAddress(id) {
    event.preventDefault()
    let isConfirmed = confirm('آیا این آدرس را حذف می کنید؟')
    if (isConfirmed) {
        $.ajax({
            url: '/delete-address/',
            method: 'GET',
            data: {
                address_id: id,
            },
            success: function (res) {
                let container = $('#address-cont')
                container.html(res)
                setTimeout(function () {
                    alert('آدرس با موفقیت حذف شد.')
                }, 100)
            },
        })
    }

}

function activateAddress(id) {
    event.preventDefault()
    $.ajax({
        url: '/activate-address/',
        method: 'GET',
        data: {
            address_id: id,
        },
        success: function (res) {
            let container = $('#address-cont')
            container.html(res)
            setTimeout(function () {
                alert('آدرس با موفقیت فعال شد.')
            }, 100)
        },
    })
}

function editAddress(id) {

    event.preventDefault()
    $.ajax({
        url: '/edit-address/',
        method: 'GET',
        data: {
            address_id: id,
        },
        success: function (res) {
            let container = $('#new-address')
            container.html(res)
            let idInput = document.querySelector('#address-id')
            idInput.value = id
            selectBoxOptions()
        },
    })
}
