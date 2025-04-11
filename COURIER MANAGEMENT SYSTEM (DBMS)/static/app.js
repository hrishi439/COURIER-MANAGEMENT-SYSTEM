document.getElementById('orderForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent default form submission

    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;
    const phone = document.getElementById('phone').value;

    const formData = new FormData();
    formData.append('name', name);
    formData.append('address', address);
    formData.append('phone', phone);

    fetch('/place_order', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        alert(data);  // Display the response (tracking ID)
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('trackingForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent default form submission

    const trackingId = document.getElementById('trackingId').value;

    const formData = new FormData();
    formData.append('trackingId', trackingId);

    fetch('/track_order', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'Order Found') {
            document.getElementById('trackingResult').innerHTML = `
                <h3>Order Details</h3>
                <p>Name: ${data.name}</p>
                <p>Address: ${data.address}</p>
                <p>Phone: ${data.phone}</p>
                <p>Tracking ID: ${data.tracking_id}</p>
            `;
        } else {
            document.getElementById('trackingResult').innerHTML = `<p>${data.message}</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
