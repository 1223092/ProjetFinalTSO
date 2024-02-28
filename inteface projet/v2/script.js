
### JavaScript (script.js)

```javascript
// Toggle control button state and sidebar navigation

// Function to toggle the state of a control button
function toggleControl(button) {
    const isOn = button.textContent.includes('On');
    button.classList.toggle('on', !isOn);
    button.classList.toggle('off', isOn);
    button.textContent = `${button.textContent.split(':')[0]} : ${isOn ? 'Off' : 'On'}`;
}

// Event listener for control buttons
document.querySelectorAll('.control-button').forEach(button => {
    button.addEventListener('click', function() {
        toggleControl(this);
        // Here, you would also handle the backend update, such as an API call.
    });
});

// Function to activate a sidebar menu item and deactivate others
function activateMenuItem(clickedItem) {
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
        item.dataset.content && document.getElementById(item.dataset.content + '-content').classList.remove('active');
    });
    clickedItem.classList.add('active');
    const contentId = clickedItem.dataset.content + '-content';
    document.getElementById(contentId).classList.add('active');
}

// Event listener for sidebar navigation menu items with content switch
document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', function() {
        activateMenuItem(this);
    });
});

// Initialize the first tab as active
document.querySelector('.menu-item[data-content="dashboard"]').click();
