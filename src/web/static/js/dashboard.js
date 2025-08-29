// Dashboard JavaScript functionality

let sensorChart;
let fermentationChart;

document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    updateDashboard();
    
    // Update dashboard every 30 seconds
    setInterval(updateDashboard, 30000);
});

function initializeCharts() {
    // Sensor data chart (temperature and humidity)
    const sensorCtx = document.getElementById('sensorChart').getContext('2d');
    sensorChart = new Chart(sensorCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: '溫度 (°C)',
                data: [],
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                yAxisID: 'y'
            }, {
                label: '濕度 (%)',
                data: [],
                borderColor: 'rgb(54, 162, 235)',
                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                yAxisID: 'y1'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: '溫度 (°C)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: '濕度 (%)'
                    },
                    grid: {
                        drawOnChartArea: false,
                    }
                }
            },
            plugins: {
                legend: {
                    display: true
                }
            }
        }
    });

    // Fermentation activity chart
    const fermentationCtx = document.getElementById('fermentationChart').getContext('2d');
    fermentationChart = new Chart(fermentationCtx, {
        type: 'doughnut',
        data: {
            labels: ['發酵活動', '靜態'],
            datasets: [{
                data: [0, 100],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(201, 203, 207, 0.3)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function updateDashboard() {
    updateCurrentStatus();
    updateSensorChart();
    updateFermentationChart();
    updateSessionsList();
}

function updateCurrentStatus() {
    fetch('/api/current-status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('current-temp').textContent = 
                data.temperature ? `${data.temperature.toFixed(1)}°C` : '--°C';
            document.getElementById('current-humidity').textContent = 
                data.humidity ? `${data.humidity.toFixed(1)}%` : '--%';
            document.getElementById('fermentation-activity').textContent = 
                data.fermentation_activity.toFixed(1);
            document.getElementById('bubble-count').textContent = 
                data.bubble_count;
        })
        .catch(error => {
            console.error('Error updating current status:', error);
        });
}

function updateSensorChart() {
    fetch('/api/sensor-data?hours=24')
        .then(response => response.json())
        .then(data => {
            const labels = data.map(item => 
                new Date(item.timestamp * 1000).toLocaleTimeString('zh-TW', {
                    hour: '2-digit',
                    minute: '2-digit'
                })
            ).reverse();
            
            const temperatures = data.map(item => item.temperature).reverse();
            const humidities = data.map(item => item.humidity).reverse();
            
            sensorChart.data.labels = labels;
            sensorChart.data.datasets[0].data = temperatures;
            sensorChart.data.datasets[1].data = humidities;
            sensorChart.update();
        })
        .catch(error => {
            console.error('Error updating sensor chart:', error);
        });
}

function updateFermentationChart() {
    fetch('/api/image-metrics?hours=1')
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                const latest = data[0];
                const activity = Math.min(latest.surface_activity / 10, 100); // Normalize to 0-100
                
                fermentationChart.data.datasets[0].data = [activity, 100 - activity];
                fermentationChart.update();
            }
        })
        .catch(error => {
            console.error('Error updating fermentation chart:', error);
        });
}

function updateSessionsList() {
    fetch('/api/sessions')
        .then(response => response.json())
        .then(data => {
            const sessionsList = document.getElementById('sessions-list');
            
            if (data.length === 0) {
                sessionsList.innerHTML = `
                    <div class="text-center text-muted py-4">
                        <i class="fas fa-clipboard-list fa-2x mb-3"></i>
                        <p>目前沒有進行中的發酵階段</p>
                    </div>
                `;
            } else {
                sessionsList.innerHTML = data.map(session => `
                    <div class="card session-card session-active mb-3">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <h6 class="card-title mb-2">
                                        <span class="status-indicator status-active"></span>
                                        ${session.name}
                                    </h6>
                                    <p class="card-text text-muted mb-1">
                                        <i class="fas fa-clock me-1"></i>
                                        開始時間: ${new Date(session.start_time * 1000).toLocaleString('zh-TW')}
                                    </p>
                                    ${session.notes ? `<p class="card-text"><small>${session.notes}</small></p>` : ''}
                                </div>
                                <div class="text-end">
                                    <small class="text-muted">
                                        進行中 ${Math.floor((Date.now() / 1000 - session.start_time) / 3600)}小時
                                    </small>
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('');
            }
        })
        .catch(error => {
            console.error('Error updating sessions list:', error);
        });
}

function createSession() {
    const name = document.getElementById('sessionName').value;
    const notes = document.getElementById('sessionNotes').value;
    
    if (!name.trim()) {
        alert('請輸入階段名稱');
        return;
    }
    
    fetch('/api/sessions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            notes: notes
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'created') {
            // Clear form
            document.getElementById('sessionForm').reset();
            
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('newSessionModal'));
            modal.hide();
            
            // Update sessions list
            updateSessionsList();
        }
    })
    .catch(error => {
        console.error('Error creating session:', error);
        alert('建立階段時發生錯誤');
    });
}