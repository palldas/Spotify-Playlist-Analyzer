const playlistLinks = document.querySelectorAll('.playlist-link');

playlistLinks.forEach(link => {
    link.addEventListener('click', event => {
        event.preventDefault();
        const playlistName = link.textContent;
        window.location.href = `/playlist/${encodeURIComponent(playlistName)}`;
    });
});
