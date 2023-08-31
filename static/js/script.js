// Add this code after the existing code in scripts.js

// Artist sorting dropdown
const artistSortDropdown = document.getElementById('artist-sort');
const artistList = document.getElementById('artist-list');

artistSortDropdown.addEventListener('change', () => {
    const selectedValue = artistSortDropdown.value;
    const sortedArtists = sortArtists(selectedValue);
    updateArtistList(sortedArtists);
});

// Update the sortArtists function
function sortArtists(sortType) {
    if (sortType === 'alphabetical') {
        const sortedArtists = Object.keys(artistCounts).sort();
        return sortedArtists;
    } else if (sortType === 'count') {
        const sortedArtists = Object.keys(artistCounts).sort((a, b) => artistCounts[b] - artistCounts[a]);
        return sortedArtists;
    } else if (sortType === 'countLowToHigh') {
        const sortedArtists = Object.keys(artistCounts).sort((a, b) => artistCounts[a] - artistCounts[b]);
        return sortedArtists;
    } else if (sortType === 'reverseAlphabetical') {
        const sortedArtists = Object.keys(artistCounts).sort((a, b) => b.localeCompare(a));
        return sortedArtists;
    }
}

function updateArtistList(sortedArtists) {
    artistList.innerHTML = ''; // Clear the existing list
    sortedArtists.forEach(artist => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `<span class="detail-name">${artist}</span>: ${artistCounts[artist]}`;
        artistList.appendChild(listItem);
    });
}

// Track popularity sorting dropdown
const trackSortDropdown = document.getElementById('track-sort');
const trackList = document.getElementById('track-list');

trackSortDropdown.addEventListener('change', () => {
    const selectedValue = trackSortDropdown.value;
    const sortedTracks = sortTracks(selectedValue);
    updateTrackList(sortedTracks);
});

// Update the sortTracks function
function sortTracks(sortType) {
    if (sortType === 'popularity') {
        return sortedTrackPopularity;
    } else if (sortType === 'alphabetical') {
        return sortedTrackPopularity.slice().sort((a, b) => a[0].localeCompare(b[0]));
    } else if (sortType === 'popularityLowToHigh') {
        return sortedTrackPopularity.slice().sort((a, b) => a[1] - b[1]);
    } else if (sortType === 'reverseAlphabetical') {
        return sortedTrackPopularity.slice().sort((a, b) => b[0].localeCompare(a[0]));
    }
}

function updateTrackList(sortedTracks) {
    trackList.innerHTML = ''; // Clear the existing list
    sortedTracks.forEach(track => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `<span class="detail-name">${track[0]}</span>: ${track[1]}`;
        // listItem.textContent = `${track[0]} (Popularity: ${track[1]})`;
        trackList.appendChild(listItem);
    });
}
