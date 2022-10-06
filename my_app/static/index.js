function addToList(eventId) {
    fetch('/add-to-list', {
        method: 'POST',
        body: JSON.stringify({eventId: eventId})
    }).then((_res) => {
        console.log(_res);
    });
}

function removeEvent(id) {
    fetch('/delete-event', {
        method: 'POST',
        body: JSON.stringify({evtId: id})
    }).then((_res) => {
        window.location.href = "/watch-list";
    });
}