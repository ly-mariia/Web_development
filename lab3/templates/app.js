document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = 'http://localhost:8000';
    let token = localStorage.getItem('token');

    if (!token && !location.pathname.endsWith('/token.html')) {
        location.href = 'token.html';
    }

    document.getElementById('token-form')?.addEventListener('submit', (e) => {
        e.preventDefault();
        token = document.getElementById('token').value;
        localStorage.setItem('token', token);
        location.href = 'index.html';
    });

    const fetchItems = async () => {
        try {
            const response = await fetch(`${apiUrl}/items/`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                const items = await response.json();
                const itemsList = document.getElementById('items-list');
                itemsList.innerHTML = '';
                items.forEach((item, index) => {
                    if (item.name && item.price !== undefined) {
                        const itemRow = document.createElement('tr');
                        itemRow.innerHTML = `
                            <th scope="row">${index + 1}</th>
                            <td>${item.name}</td>
                            <td>$${item.price.toFixed(2)}</td>
                        `;
                        itemsList.appendChild(itemRow);
                    } else {
                        console.error('Invalid item data:', item);
                    }
                });
            } else {
                alert('Failed to fetch items');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const fetchCart = async (sort_by = 'name', order = 'asc') => {
        try {
            const response = await fetch(`${apiUrl}/cart_items_sorted/?sort_by=${sort_by}&order=${order}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                const cartItems = await response.json();
                const cartList = document.getElementById('cart-list');
                cartList.innerHTML = '';
                cartItems.forEach((item, index) => {
                    const cartRow = document.createElement('tr');
                    cartRow.innerHTML = `
                        <th scope="row">${index + 1}</th>
                        <td>${item.item.name}</td>
                        <td>$${item.item.price.toFixed(2)}</td>
                        <td>${item.quantity}</td>
                        <td>$${item.total.toFixed(2)}</td>
                    `;
                    cartList.appendChild(cartRow);
                });
            } else {
                alert('Failed to fetch cart');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    if (location.pathname.endsWith('/items.html')) {
        fetchItems();
    } else if (location.pathname.endsWith('/cart.html')) {
        fetchCart();

        document.getElementById('sort-button')?.addEventListener('click', () => {
            const sortBy = document.getElementById('sort-by').value;
            const order = document.getElementById('order').value;
            fetchCart(sortBy, order);
        });
    }
});
