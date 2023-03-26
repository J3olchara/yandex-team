window.onload = function() {
    const navigation = document.getElementsByClassName('catalog-item-navigation');
    for (let i = 0; i < navigation.length; ++i) {
        // console.log(navigation[i].classList[1].split('-')[2]);
        let url = navigation[i].getAttribute('data-url-redirect');
        navigation[i].addEventListener('click', Redirect(url));
    }
    clockUpdate();
    setInterval(clockUpdate, 1000);
}

function change_language_form(form) {
    console.log(form);
    form.submit();
}