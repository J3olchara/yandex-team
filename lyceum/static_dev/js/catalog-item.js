

function Redirect(url) {
    console.log(url);
    return function location_change() {
        document.location.href = url;
    }
}