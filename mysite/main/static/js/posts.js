const allPostsTab = document.getElementById('all-posts-tab')
const allPostsList = document.getElementById('all-posts-list')

const favoritesTab = document.getElementById('favorites-tab')
const favoritesList = document.getElementById('favorites-list')

const myPostsTab = document.getElementById('my-posts-tab');
const myPostsList = document.getElementById('my-posts-list')

allPostsTab.classList.add('selected-tab');
favoritesList.style.display = 'none';
myPostsList.style.display = 'none';

favoritesTab.addEventListener('click', () => {
    allPostsTab.classList.remove('selected-tab');
    myPostsTab.classList.remove('selected-tab');
    favoritesTab.classList.add('selected-tab');

    allPostsList.style.display = 'none';
    myPostsList.style.display = 'none';
    favoritesList.style.display = 'block';
})

allPostsTab.addEventListener('click', () => {
    favoritesTab.classList.remove('selected-tab');
    myPostsTab.classList.remove('selected-tab');
    allPostsTab.classList.add('selected-tab');

    allPostsList.style.display = 'block';
    myPostsList.style.display = 'none';
    favoritesList.style.display = 'none';
})

myPostsTab.addEventListener('click', () => {
    favoritesTab.classList.remove('selected-tab');
    allPostsTab.classList.remove('selected-tab');
    myPostsTab.classList.add('selected-tab');

    allPostsList.style.display = 'none';
    myPostsList.style.display = 'block';
    favoritesList.style.display = 'none';
})


const dropdownBtn = document.getElementById('category-dropdown-btn');
const dropdownMenu = document.getElementById('category-dropdown-menu');

dropdownBtn.addEventListener('click', function () {
    dropdownMenu.classList.toggle('hidden');
});

// close the dropdown if clicked outside
document.addEventListener('click', function (event) {
    if (!dropdownBtn.contains(event.target) && !dropdownMenu.contains(event.target)) {
        dropdownMenu.classList.add('hidden');
    }
});
