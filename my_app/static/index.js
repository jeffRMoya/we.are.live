// these functions are taking in an id and posting it to that url
// allows me to get the data in my python script from that url
// the url itself does not have GET access, so we can't actually access it online
function addToList(eventId) {
    fetch('/add-to-list', {
        method: 'POST',
        body: JSON.stringify({eventId: eventId})
    })
}

function removeEvent(id) {
    fetch('/delete-event', {
        method: 'POST',
        body: JSON.stringify({evtId: id})
    }).then((_res) => {
        window.location.href = "/watch-list";
    });
}