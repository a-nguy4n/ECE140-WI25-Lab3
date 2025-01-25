
let count = 0;

// Get DOM elements we'll be updating
const counterDisplay = document.getElementById('counterDisplay');
const saveStatus = document.getElementById('saveStatus');

// Function to update the counter
function updateCounter(change) {
    count += change;
    counterDisplay.textContent = count;
    // Clear any previous save status
    saveStatus.textContent = '';
}

// Function to save the counter to the server
async function saveCounter() {
    try {
        // Send POST request to our FastAPI endpoint
        const response = await fetch('/save_count', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ count: count })
        });
        
        const data = await response.json();
        
        // Show save status
        saveStatus.textContent = data.message;

        if(data.count !== undefined){
            count = data.count;
            counterDisplay.textContent = count; 
        }
    } 
    
    catch (error) {
        saveStatus.textContent = 'Error saving count';
        saveStatus.style.color = 'red';
    }
}

// Initialize counter from server when page loads
async function initializeCounter() {
    try {
       
        const response = await fetch('/get_count');
        if (!response.ok){
            throw new Error(`Failed to fetch count: ${response.status}`);
        }

        const data = await response.json();
        count = data.count || 0; 
        counterDisplay.textContent = count; 
        return count;
    }
    catch (error) {
        console.error('Error initializing counter:', error);
    }
}

async function counterInitialAlert(){
    try{
        const initializedCount = await initializeCounter(); 
        if(initializedCount == 0){
            alert('Counter initialized'); 
        }
    }
    catch (error) {
        console.error('Counter not initialized');
    }

}

document.addEventListener('DOMContentLoaded', () => {
    counterInitialAlert();
    setConnectionStatus();
});


async function setConnectionStatus() {
    // once server counter is initialized with data from server
    // set div with id connectionStatus text content to "Connected" 
    // and color to green
    const connectionStatus = document.getElementById('connectionStatus');
    if(!connectionStatus){
        console.error('Connection Status Not Found');
        return;
    }

    try{
        const initializedCount = await initializeCounter();

        if(initializedCount !== null){
            connectionStatus.textContent = 'Connected';
            connectionStatus.style.color = 'green';
        }

        else{
            connectionStatus.textContent = 'Disconnected';
            connectionStatus.style.color = 'red';
        }
    }
    catch(error){
        console.error('Error setting connection status', error);
        connectionStatus.textContent = 'Error';
        connectionStatus.style.color = 'red'; 
    }
}
