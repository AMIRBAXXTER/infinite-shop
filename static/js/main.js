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
