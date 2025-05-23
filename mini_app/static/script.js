document.addEventListener("DOMContentLoaded", async () => {
    const container = document.getElementById("products");
    
    // Запрашиваем товары с FastAPI-сервера
    const response = await fetch("/api/products");
    const products = await response.json();

    products.forEach(product => {
        container.innerHTML += `
            <div class="product">
                <img src="${product.image}" alt="${product.name}">
                <h3>${product.name}</h3>
                <p class="price">${product.price} руб.</p>
            </div>
        `;
    });

    Telegram.WebApp.expand();  // Раскрываем Mini App на весь экран
});