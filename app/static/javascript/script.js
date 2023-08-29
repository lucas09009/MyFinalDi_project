let currentIndex = 0;
let images = document.querySelectorAll('.image_de_produits-defilants img');
let prevButton = document.querySelector('.fa-chevron-left');
let nextButton = document.querySelector('.fa-chevron-right');

function showImage(index) {
    if (index < 0) {
        index = images.length - 1;
    } else if (index >= images.length) {
        index = 0;
    }
    images.forEach(img => img.style.display = 'none');
    images[index].style.display = 'block';
    currentIndex = index;
}

function prevImage() {
    showImage(currentIndex - 1);
}

function nextImage() {
    showImage(currentIndex + 1);
}

prevButton.addEventListener('click', prevImage);
nextButton.addEventListener('click', nextImage);

setInterval(nextImage, 6000);



document.addEventListener("DOMContentLoaded", function() {
    const depliant = document.getElementById("users-info");

    depliant.addEventListener("click", function() {
        this.classList.toggle("active");
    });
});



function previewImage(input) {
    const uploadedImage = document.getElementById("uploadedImage");
    const uploadIcon = document.querySelector(".upload-icon");

    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function(e) {
            uploadedImage.src = e.target.result;
            uploadedImage.style.display = "block";
            uploadIcon.style.opacity = 0;
        };

        reader.readAsDataURL(input.files[0]);
    }
}



document.addEventListener('DOMContentLoaded', function () {
    const inventoryContainer = document.querySelector('.inventaire-des-articles');
    const cartCount = document.getElementById('cart-count');
    const notificationContainer = document.querySelector('.notification-container');

    let itemCount = 0;

    inventoryContainer.addEventListener('click', event => {
        if (event.target.classList.contains('cart-button')) {
            itemCount++;
            cartCount.textContent = itemCount;

            const icon = event.target.querySelector('.fa-cart-shopping');
            icon.classList.add('active');

            const notification = document.createElement('div');
            notification.classList.add('notification');
            notification.textContent = 'Article ajouté au panier';

            notificationContainer.appendChild(notification);

            setTimeout(function () {
                notification.style.opacity = '0';
                notification.addEventListener('transitionend', function () {
                    notification.remove();
                }, { once: true });
                icon.classList.remove('active');
            }, 6000);
        }
    });
});



// ...

// document.addEventListener('DOMContentLoaded', function () {
//     const allCategoriesTitle = document.getElementById('all-categories');

//     filterArticlesByCategory('all');

//     allCategoriesTitle.addEventListener('click', function () {
//         filterArticlesByCategory('all');
//     });

//     const categoryItems = document.querySelectorAll('.Menu li[data-category]');
//     categoryItems.forEach((item) => {
//         item.addEventListener('click', function () {
//             const selectedCategory = this.getAttribute('data-category'); 
//             filterArticlesByCategory(selectedCategory);
//         });
//     });
// });


document.addEventListener('DOMContentLoaded', function () {
    const pageButtons = document.querySelectorAll('.page');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');

    let currentPage = 1; 

    pageButtons.forEach((button) => {
        button.addEventListener('click', function () {
            const newPage = parseInt(this.dataset.page);
            if (newPage !== currentPage) {
                currentPage = newPage;
               
                updateArticlesForPage(currentPage);
            }
        });
    });

    prevButton.addEventListener('click', function () {
        if (currentPage > 1) {
            currentPage--;
            updateArticlesForPage(currentPage);
        }
    });

    nextButton.addEventListener('click', function () {
        const totalPages = getTotalPages();
        if (currentPage < totalPages) {
            currentPage++;
            updateArticlesForPage(currentPage);
        }
    });

    function updateArticlesForPage(page) {
    }
});



















function filterArticlesByCategory(category) {
    const allArticlesDivs = document.querySelectorAll('.exposition-images'); 
    allArticlesDivs.forEach((articleDiv) => {
        if (category === 'all' || articleDiv.dataset.category === category) {
            console.log(articleDiv.dataset.category)
            console.log(category)
            articleDiv.style.display = 'block';
        } else {
            articleDiv.style.display = 'none';
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const allCategoriesTitle = document.getElementById('all-categories');

    filterArticlesByCategory('all');

    allCategoriesTitle.addEventListener('click', function () {
        filterArticlesByCategory('all');
    });

    const categoryItems = document.querySelectorAll('.Menu li[data-category]');
    console.log(categoryItems)
    categoryItems.forEach((item) => {
        item.addEventListener('click', function () {
            const selectedCategory = this.getAttribute('data-category'); 
            filterArticlesByCategory(selectedCategory);
                console.log(selectedCategory);
            console.log(item);
        });
    });
});
