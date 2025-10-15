document.addEventListener('DOMContentLoaded', () => {
    const banner = document.getElementById('banner');
    if (banner) {
        banner.addEventListener('animationend', () => {
            banner.style.display = 'none';
        });
    }
});
