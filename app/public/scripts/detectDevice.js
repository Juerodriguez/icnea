function isMobileDevice() {
    return (typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1);
}

function loadFrontend() {
    if (isMobileDevice()) {
        window.location.replace(window.location.href + "movile");
    } else {
        window.location.replace(window.location.href + "desktop");
    }
}

loadFrontend();