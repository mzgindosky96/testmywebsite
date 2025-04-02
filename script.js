// Weather Functions
async function fetchWeather() {
    const apiKey = '79de4918edc0fb684a957d2e926c4eaa';
    const city = 'Duhok,IQ';
    const url = `https://api.openweathermap.org/data/2.5/forecast?q=${city}&units=metric&appid=${apiKey}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        data.list ? displayWeather(data) : showWeatherError();
    } catch (error) {
        console.error('Error fetching weather data:', error);
        showWeatherError();
    }
}

function displayWeather(data) {
    const weatherContainer = document.querySelector('.weather-details');
    weatherContainer.innerHTML = '';
    
    // Aggregate daily forecasts
    const dailyForecasts = data.list.reduce((acc, forecast) => {
        const date = new Date(forecast.dt * 1000).toLocaleDateString('en-US', { 
            weekday: 'long', 
            month: 'short', 
            day: 'numeric' 
        });
        if (!acc[date]) {
            acc[date] = {
                temp: Math.round(forecast.main.temp),
                description: forecast.weather[0].main,
                icon: getWeatherIcon(forecast.weather[0].id)
            };
        }
        return acc;
    }, {});

    // Create weather cards
    Object.entries(dailyForecasts).slice(0, 3).forEach(([day, forecast]) => {
        const weatherCard = document.createElement('div');
        weatherCard.className = 'weather-card';
        weatherCard.innerHTML = `
            <div class="floating-icon">
                <i class="fas ${forecast.icon} weather-icon"></i>
            </div>
            <div class="temperature">${forecast.temp}°C</div>
            <div class="weather-condition">${forecast.description}</div>
            <p>${getWeatherMessage(forecast.description)}</p>
        `;
        weatherContainer.appendChild(weatherCard);
    });
}

function getWeatherIcon(weatherId) {
    if (weatherId >= 200 && weatherId < 300) return 'fa-bolt';
    if (weatherId >= 300 && weatherId < 600) return 'fa-cloud-rain';
    if (weatherId >= 600 && weatherId < 700) return 'fa-snowflake';
    if (weatherId === 800) return 'fa-sun';
    if (weatherId > 800) return 'fa-cloud';
    return 'fa-cloud-sun';
}

function getWeatherMessage(condition) {
    const messages = {
        'Clear': 'Perfect day for outdoor shopping!',
        'Clouds': 'Light cloud cover expected',
        'Rain': 'Don\'t forget your umbrella!',
        'Thunderstorm': 'Seek indoor shelter if storm occurs',
        'Snow': 'Watch for slippery surfaces'
    };
    return messages[condition] || 'Check back for updates!';
}

function showWeatherError() {
    document.querySelector('.weather-details').innerHTML = `
        <div class="weather-card error">
            <i class="fas fa-exclamation-triangle weather-icon"></i>
            <p>Unable to load weather data. Please try again later.</p>
        </div>
    `;
}

// Visitor Counter
let totalVisitors = localStorage.getItem('totalVisitors') || 0;
let onlineUsers = new Set();

function updateVisitorCount() {
    // Generate unique session ID
    const sessionId = sessionStorage.getItem('sessionId') || Date.now().toString();
    
    if (!sessionStorage.getItem('sessionId')) {
        totalVisitors++;
        localStorage.setItem('totalVisitors', totalVisitors);
        sessionStorage.setItem('sessionId', sessionId);
    }

    onlineUsers.add(sessionId);
    localStorage.setItem('onlineUsers', JSON.stringify([...onlineUsers]));
    
    document.getElementById('total-visitors').textContent = totalVisitors;
    document.getElementById('online-count').textContent = onlineUsers.size;
}


// Price Table Editor
document.querySelectorAll('#prices tr').forEach(row => {
    row.addEventListener('dblclick', () => {
        const itemName = row.cells[0].textContent;
        const currentPrice = row.cells[1].textContent;
        const newPrice = prompt(`Edit price for ${itemName}:`, currentPrice);
        
        if (newPrice && newPrice !== currentPrice) {
            row.cells[1].textContent = newPrice;
            row.style.animation = 'highlightUpdate 1s';
            row.addEventListener('animationend', () => row.style.animation = '');
        }
    });
});

// Map Interaction
document.querySelector('#map iframe').addEventListener('click', () => {
    window.open(document.querySelector('#map iframe').src.replace('/embed', '/map'), '_blank');
});

// Initialize Page
window.addEventListener('load', () => {
    fetchWeather();
    updateVisitorCount();
    
    // Load existing online users
    const storedUsers = localStorage.getItem('onlineUsers');
    onlineUsers = new Set(storedUsers ? JSON.parse(storedUsers) : []);
    
    // Cleanup expired sessions
    window.addEventListener('beforeunload', () => {
        onlineUsers.delete(sessionStorage.getItem('sessionId'));
        localStorage.setItem('onlineUsers', JSON.stringify([...onlineUsers]));
    });
});

// Post item
document.getElementById('item-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('name', document.getElementById('item-name').value);
    formData.append('description', document.getElementById('item-description').value);
    formData.append('price', document.getElementById('item-price').value);
    formData.append('image', document.getElementById('item-image').files[0]);

    try {
        const response = await fetch('post_item.php', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        
        if (result.status === 'success') {
            displayItems();
            this.reset();
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

// Display items
async function displayItems() {
    try {
        const response = await fetch('get_items.php');
        const items = await response.json();
        const container = document.getElementById('items-list');
        container.innerHTML = '';

        items.forEach(item => {
            const itemCard = document.createElement('div');
            itemCard.className = 'item-card';
            itemCard.innerHTML = `
                <img src="${item.image}" class="item-image" alt="${item.name}">
                <div class="item-info">
                    <h4>${item.name}</h4>
                    <p>${item.description}</p>
                    <div class="item-price">${Number(item.price).toLocaleString()} IQD</div>
                    <small>Posted: ${new Date(item.created_at).toLocaleDateString()}</small>
                </div>
            `;
            container.appendChild(itemCard);
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

// Initial display
displayItems();

document.getElementById('item-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('name', document.getElementById('item-name').value);
    formData.append('description', document.getElementById('item-description').value);
    formData.append('price', document.getElementById('item-price').value);
    formData.append('image', document.getElementById('item-image').files[0]);
    formData.append('secret_code', document.getElementById('secret-code').value);

    try {
        const response = await fetch('post_item.php', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        
        if (result.status === 'success') {
            displayItems();
            this.reset();
            alert('Item posted successfully!');
        } else {
            alert('Error: ' + (result.message || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Network error - please try again');
    }
});

// Keep displayItems() function the same as before

// Animation Keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes highlightUpdate {
        0% { background-color: #ffd70050; }
        100% { background-color: transparent; }
    }
`;
document.head.appendChild(style);
