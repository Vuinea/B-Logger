const allPostsTab = document.getElementById('all-posts-tab')
const allPostsList = document.getElementById('all-posts-list')

const favoritesTab = document.getElementById('favorites-tab')
const favoritesList = document.getElementById('favorites-list')

allPostsTab.classList.add('selected-tab');
favoritesList.style.display = 'none';


favoritesTab.addEventListener('click', () => {
    allPostsTab.classList.remove('selected-tab');
    favoritesTab.classList.add('selected-tab');

    allPostsList.style.display = 'none';
    favoritesList.style.display = 'block';
})

allPostsTab.addEventListener('click', () => {
    favoritesTab.classList.remove('selected-tab');
    allPostsTab.classList.add('selected-tab');

    allPostsList.style.display = 'block';
    favoritesList.style.display = 'none';
})


