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
                    let productCount = document.querySelector('#product-count')
                    let stockInput = document.querySelector('#color-id-input')
                    colorStock.innerHTML = data.stock
                    colorTitle.innerHTML = data.title
                    colorTitle.setAttribute('style', `color: ${data.color};`)
                    stockInput.value = data.id
                    productCount.max = data.stock
                    productCount.value = 1
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
    if (provincesSelectBox.val()){
        selectBoxUpdate(citySelectBox.val())
    }
    citySelectBox.html('<option value="" selected="">---------</option>')
    function selectBoxUpdate (prevCity) {
        let provinceId = provincesSelectBox.val()
        if (provinceId){
            $.ajax({
            url: '/get-city/',
            method: 'GET',
            data: {
                province_id: provinceId,
            },
            success: function (data) {
                citySelectBox.html('<option value="" selected="">---------</option>')
                for (let city of data.cities) {
                    let option = document.createElement('option')
                    option.value = city[1]
                    option.innerHTML = city[0]
                    citySelectBox.append(option)
                    console.log(prevCity)
                    if (prevCity){
                        citySelectBox.val(prevCity)
                    }
                }
            },
        })
        }else {
            citySelectBox.html('<option value="" selected="">---------</option>')
        }

    }
    provincesSelectBox.on('change', selectBoxUpdate)

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
            province: provinceId.value,
            city: cityId.value,
            address: address.value,
            postal_code: postalCode.value,
            receiver_name: receiverName.value,
            address_id: addressIdValue,
            submit_type: submitButton.value,
        },
        success: function (res) {
            cityId.innerHTML = '<option value="" selected="">---------</option>'
            provinceId.value = ''
            address.value = ''
            postalCode.value = ''
            receiverName.value = ''
            let container = null
            if (res.includes('option')){
                container = $('#form-cont')
            }else {
                container = $('#address-cont')
            }

            container.html(res)
            let idInput = document.querySelector('#address-id')
            if (idInput){idInput.value = ''}
            submitButton.innerHTML = 'ثبت'
            submitButton.blur()
            submitButton.value = 'add'
            $('.address-title').text('افزودن آدرس جدید')
            alert('آدرس با موفقیت ثبت شد.')

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
            let container = $('#form-cont')
            container.html(res)
            let idInput = document.querySelector('#address-id')
            idInput.value = id
            let submitButton = document.querySelector('#submit-button')
            submitButton.value = 'edit'
            submitButton.innerHTML = 'ویرایش'
            let title = document.querySelector('.address-title')
            title.innerHTML = 'ویرایش آدرس'
            selectBoxOptions()
        },
    })
}

function addProductToCart(product_id) {
    event.preventDefault()
    let colorId = document.querySelector('#color-id-input').value
    let count = document.querySelector('#product-count').value
    if (count === '') {
        count = 1
    }

    $.ajax({
        url: '/add-to-cart/',
        method: 'GET',
        data: {
            product_id: product_id,
            color_id: colorId,
            count: count
        },
        success: function (data) {
            if (data.status === true) {
                setTimeout(function () {
                    alert('محصول با موفقیت اضافه شد.')
                }, 500)
            } else if (data.status === 'color_id') {
                setTimeout(function () {
                    alert('ابتدا یک رنگ انتخاب کنید.')
                }, 500)
            }else if (data.status == false){
                setTimeout(function () {
                    alert('متاسفانه خطایی رخ داد دوباره امتحان کنید.')
                }, 500)
            }
        },
    })
}

function emptyCart() {
    event.preventDefault()
    $.ajax({
        url: '/empty-cart/',
        method: 'GET',
        success: function (data) {
            if (data) {
                let cartProducts = document.querySelector('#cart-products-partial')
                cartProducts.innerHTML = data
                setTimeout(function () {
                    alert('سبد خرید شما خالی شد.')
                }, 500)
            } else {
                setTimeout(function () {
                    alert('خطایی رخ داد.')
                }, 500)
            }
        },
    })
}

function removeProduct() {
    event.preventDefault()
    let deleteButton = event.target.closest('.product-remove')
    let productId = deleteButton.getAttribute('data-product-id')
    let colorId = deleteButton.getAttribute('data-color-id')
    $.ajax({
        url: '/remove-product/',
        method: 'GET',
        data: {
            product_id: productId,
            color_id: colorId,
        },
        success: function (data) {
            if (data) {
                deleteButton.closest('.product').remove()
                $('#factor').html(data)
                if ($('.product').length === 0) {
                    let cont = $('#products-cont')
                    let div = document.createElement('div')
                    div.className = 'col-12 alert alert-warning'
                    div.innerHTML = 'محصولی در سبد خرید شما وجود ندارد.'
                    cont.append(div)
                }

                setTimeout(function () {
                    alert('محصول با موفقیت حذف شد.')
                }, 500)
            } else {
                setTimeout(function () {
                    alert('خطایی رخ داد.')
                }, 500)
            }
        },
    })
}
