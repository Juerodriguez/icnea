function isMobileDevice() {
    return (typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1);
}

function loadFrontend(e) {
    if (isMobileDevice()) {
        window.location.replace(window.location.href + "mobile");
    } else {
        window.location.replace(window.location.href + "desktop");
    }
}