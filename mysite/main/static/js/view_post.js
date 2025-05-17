const favoriteBtn = document.getElementById('favorite-btn');

const fullUrl = window.location.href;
const url = fullUrl.slice(0, fullUrl.length - 1)
const postId = url.substring(url.lastIndexOf('/') + 1);

let notFavoriteSVG = `
            <svg xmlns="http://www.w3.org/2000/svg" class="favorite-icon bi bi-heart" viewBox="0 0 16 16">
                <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
            </svg>
        `


let favoriteSVG = `
    <svg xmlns="http://www.w3.org/2000/svg" class="filled-favorite-icon favorite-icon bi bi-heart-fill" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
    </svg>
    `

favoriteBtn.onclick = () => {
    svg = favoriteBtn.children[0];
    let replacementSvg;
    // it is a favorite
    if (svg.classList.contains('filled-favorite-icon')) {
        replacementSvg = notFavoriteSVG;

    // it is not a favorite
    } else {
        replacementSvg = favoriteSVG;
    }
    let postUrl = `/posts/manage_favorite/${postId}/`
        // send a request to the server to remove the post from favorites
        fetch(postUrl,{
            method: 'POST'
        })
        .then((response) => {
            favoriteBtn.innerHTML = replacementSvg; 
        })
}

const fullStar = `
<svg class="star" xmlns="http://www.w3.org/2000/svg" width="16" height="16" class="bi bi-star-fill" viewBox="0 0 16 16">
    <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
</svg>
`

const emptyStar = `
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star" viewBox="0 0 16 16">
    <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.56.56 0 0 0-.163-.505L1.71 6.745l4.052-.576a.53.53 0 0 0 .393-.288L8 2.223l1.847 3.658a.53.53 0 0 0 .393.288l4.052.575-2.906 2.77a.56.56 0 0 0-.163.506l.694 3.957-3.686-1.894a.5.5 0 0 0-.461 0z"/>
</svg>
`

const fillStars = () => {
    console.log('aslifjsa');
    // console.log(this.id);
}

const starBtns = document.querySelectorAll('.star-btn');

starBtns.forEach((starBtn) => {
    starBtn.onclick = () => {
        let postUrl = `/posts/rate_post/${postId}`
        let rating = starBtn.id[starBtn.id.length - 1];
        const formData = new FormData();
        formData.append('rating', rating)
        fetch(postUrl,{
            method: 'POST',
            body: formData,
        })
        .then((response) => {
            let fullStars = rating;
            for (let i = 0; i < fullStars; i++) {
                starBtns[i].innerHTML = fullStar;
            }
            for (let i = fullStars; i < 5; i++) {
                starBtns[i].innerHTML = emptyStar;
            }
        })

    }
})


