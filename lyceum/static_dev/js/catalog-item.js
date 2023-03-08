window.onload = function() {
    const navigation = document.getElementsByClassName('catalog-item-navigation');
    for (let i = 0; i < navigation.length; ++i) {
        // console.log(navigation[i].classList[1].split('-')[2]);
        let url = navigation[i].getAttribute('data-url-redirect');
        navigation[i].addEventListener('click', Redirect(url));
    }
}

function Redirect(url) {
    console.log(url);
    return function location_change() {
        document.location.href = url;
    }
}