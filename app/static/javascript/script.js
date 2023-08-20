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
    const notificationContainer = document.querySelector('.notification-container');

    expositionImages.forEach(function (image) {
        const icon = image.querySelector('.fa-cart-shopping');

        icon.addEventListener('click', function (event) {
            event.stopPropagation(); // Empêche la propagation de l'événement au conteneur parent

            icon.classList.toggle('active');

            if (icon.classList.contains('active')) {
                const notification = document.createElement('div');
                notification.classList.add('notification');
                notification.textContent = 'Article ajouté au panier';

                notificationContainer.appendChild(notification);

                setTimeout(function () {
                    notification.style.opacity = '0';
                    notification.addEventListener('transitionend', function () {
                        notification.remove();
                    }, { once: true });
                }, 6000);
            }
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










document.addEventListener('DOMContentLoaded', function () {
    const pageButtons = document.querySelectorAll('.page');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');

    let currentPage = 1; // Page actuelle

    // Gérer le clic sur un bouton de page
    pageButtons.forEach((button) => {
        button.addEventListener('click', function () {
            const newPage = parseInt(this.dataset.page);
            if (newPage !== currentPage) {
                currentPage = newPage;
                // Mettre à jour la logique pour afficher les articles de la nouvelle page
                // Ici, vous pourriez appeler une fonction pour mettre à jour les articles en fonction de la nouvelle page
                updateArticlesForPage(currentPage);
            }
        });
    });

    // Gérer le clic sur le bouton "Précédent"
    prevButton.addEventListener('click', function () {
        if (currentPage > 1) {
            currentPage--;
            updateArticlesForPage(currentPage);
        }
    });

    // Gérer le clic sur le bouton "Suivant"
    nextButton.addEventListener('click', function () {
        // Mettez à jour cette logique en fonction du nombre total de pages disponibles
        const totalPages = getTotalPages(); // Remplacez getTotalPages par votre propre logique
        if (currentPage < totalPages) {
            currentPage++;
            updateArticlesForPage(currentPage);
        }
    });

    // Mettre à jour les articles en fonction de la page sélectionnée
    function updateArticlesForPage(page) {
        // Mettez à jour la logique pour afficher les articles en fonction de la page
        // Vous pourriez utiliser votre fonction filterArticlesByCategory ici avec la page comme argument
    }
});




