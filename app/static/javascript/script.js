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



// function filterArticlesByCategory(category) {
//     const allArticlesDivs = document.querySelectorAll('.exposition-images');
//     allArticlesDivs.forEach((ArticlesDiv) => {
//         if (ArticlesDiv.dataset.category === category || category === 'all') {
//             ArticlesDiv.style.display = 'block';
//         } else {
//             ArticlesDiv.style.display = 'none';
//         }
//     });
// }

// document.addEventListener('DOMContentLoaded', function () {
//     filterArticlesByCategory('all');

//     const categoryItems = document.querySelectorAll('.Menu li[data-category]');
// categoryItems.forEach((item) => {
//     item.addEventListener('click', function () {
//         const selectedCategory = this.dataset.category;
//         filterArticlesByCategory(selectedCategory);
//     });
// });
// });



function filterArticlesByCategory(category) {
    const allArticlesDivs = document.querySelectorAll('.exposition-images');
    allArticlesDivs.forEach((ArticlesDiv) => {
        if (category === 'all' || ArticlesDiv.dataset.category === category) {
            ArticlesDiv.style.display = 'block';
        } else {
            ArticlesDiv.style.display = 'none';
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const allCategoriesTitle = document.getElementById('all-categories');

    // Au chargement de la page, afficher toutes les catégories
    filterArticlesByCategory('all');

    // Ajouter un écouteur de clic à l'élément h2 pour afficher toutes les catégories
    allCategoriesTitle.addEventListener('click', function () {
        filterArticlesByCategory('all');
    });

    const categoryItems = document.querySelectorAll('.Menu li[data-category]');
    categoryItems.forEach((item) => {
        item.addEventListener('click', function () {
            const selectedCategory = this.dataset.category;
            filterArticlesByCategory(selectedCategory);
        });
    });
});




document.addEventListener('DOMContentLoaded', function () {
    const expositionImages = document.querySelectorAll('.exposition-images');

    expositionImages.forEach(function (image) {
        const icon = image.querySelector('.fa-cart-shopping');

        image.addEventListener('click', function () {
            icon.classList.toggle('active');
        });

        image.addEventListener('mouseover', function () {
            icon.classList.add('fas', 'fa-heart');
        });

        image.addEventListener('mouseout', function () {
            if (!icon.classList.contains('active')) {
                icon.classList.remove('fas', 'fa-heart');
            }
        });
    });
});


   