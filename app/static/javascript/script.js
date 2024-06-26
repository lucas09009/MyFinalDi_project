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
            console.log(filterArticlesByCategory(selectedCategory));
        });
    });
});



function survol(){
    document.getElementById('articles-div-id').style.display = 'block'
}

function quitte(){
    document.getElementById('articles-div-id').style.display = 'none'
}
function survolPanier(){
    document.getElementById('panier-div-id').style.display = 'block'
}

function quittePanier(){
    document.getElementById('panier-div-id').style.display = 'none'
}

function survolFavoris(){
    document.getElementById('favoris-div-id').style.display = 'block'
}

function quitteFavoris(){
    document.getElementById('favoris-div-id').style.display = 'none'
}
function survolPromo(){
    document.getElementById('produits-defilants-child-id').style.display = 'block'
}

function quittePromo(){
    document.getElementById('produits-defilants-child-id').style.display = 'none'
}




