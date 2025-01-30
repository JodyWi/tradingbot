document.addEventListener('DOMContentLoaded', function () {
    // document.getElementById('getBalanceBtn').addEventListener('click', function () {
    //     fetch('http://127.0.0.1:5000/api/1/balance?assets=XBT,ETH,ZAR')
    //         .then(response => response.json())
    //         .then(data => {
    //             document.getElementById('balanceOutput').textContent = JSON.stringify(data, null, 2);
    //         })
    //         .catch(error => {
    //             console.error('Error:', error);
    //             document.getElementById('balanceOutput').textContent = "Error fetching balance.";
    //         });
    // });


    document.getElementById('getBalanceBtn').addEventListener('click', function() {
        fetch('http://127.0.0.1:5000/api/1/balance?assets=ZAR')  // Update this URL to match the backend
            .then(response => response.json())
            .then(data => {
                document.getElementById('balanceOutput').textContent = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                console.error('Error:', error);  // Log the error to the console for debugging
                document.getElementById('balanceOutput').textContent = "Error fetching balance.";
            });
    });
    
});
