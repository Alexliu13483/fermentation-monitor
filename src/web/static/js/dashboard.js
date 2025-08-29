// Dashboard JavaScript functionality

let sizeChart;

document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    updateDashboard();
    
    // Update dashboard every 30 seconds
    setInterval(updateDashboard, 30000);
});

function initializeCharts() {
    // Dough size chart
    const sizeCtx = document.getElementById('sizeChart').getContext('2d');
    sizeChart = new Chart(sizeCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Dough Size',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.1)',
                yAxisID: 'y'
            }, {
                label: 'Size Change (%)',
                data: [],
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.1)',
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
                        text: 'Dough Size'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Size Change (%)'
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
}

function updateDashboard() {
    updateCurrentStatus();
    updateSizeChart();
    updateSessionsList();
}

function updateCurrentStatus() {
    fetch('/api/current-status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('current-dough-size').textContent = 
                data.dough_size ? `${data.dough_size.toFixed(1)} units` : '-- units';
            document.getElementById('size-change').textContent = 
                data.size_change_percent ? `${data.size_change_percent.toFixed(1)}%` : '--%';
            document.getElementById('camera-status').textContent = 
                data.camera_status || '--';
        })
        .catch(error => {
            console.error('Error updating current status:', error);
        });
}

function updateSizeChart() {
    fetch('/api/image-metrics?hours=24')
        .then(response => response.json())
        .then(data => {
            const labels = data.map(item => 
                new Date(item.timestamp * 1000).toLocaleTimeString('en-US', {
                    hour: '2-digit',
                    minute: '2-digit'
                })
            ).reverse();
            
            const doughSizes = data.map(item => item.dough_size || 0).reverse();
            const sizeChanges = data.map(item => item.size_change || 0).reverse();
            
            sizeChart.data.labels = labels;
            sizeChart.data.datasets[0].data = doughSizes;
            sizeChart.data.datasets[1].data = sizeChanges;
            sizeChart.update();
        })
        .catch(error => {
            console.error('Error updating size chart:', error);
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
                        <p>No active fermentation sessions</p>
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
                                        Started: ${new Date(session.start_time * 1000).toLocaleString('en-US')}
                                    </p>
                                    ${session.notes ? `<p class="card-text"><small>${session.notes}</small></p>` : ''}
                                </div>
                                <div class="text-end">
                                    <small class="text-muted">
                                        Running for ${Math.floor((Date.now() / 1000 - session.start_time) / 3600)} hours
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
        alert('Please enter session name');
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
        alert('Error creating session');
    });
}