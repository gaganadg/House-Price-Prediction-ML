function predictPrice() {
    const lot_area = document.getElementById("lot_area").value;
    const bedrooms = document.getElementById("bedrooms").value;
    const bathrooms = document.getElementById("bathrooms").value;

    if (!lot_area || !bedrooms || !bathrooms) {
        alert("Please fill in all fields");
        return;
    }

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            lot_area: lot_area,
            bedrooms: bedrooms,
            bathrooms: bathrooms
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("result").innerHTML =
                `<p style='color:red;'>Error: ${data.error}</p>`;
        } else {
            document.getElementById("result").innerHTML =
                `<h2>Predicted Price: $${data.price_usd} (₹${data.price_inr})</h2>`;
        }
    });
}
