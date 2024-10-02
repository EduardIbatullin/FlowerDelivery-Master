// static/js/scripts.js

// Функция для отрисовки графика продаж
function drawSalesChart(chartId, labels, data) {
    var ctx = document.getElementById(chartId).getContext('2d');
    var salesChart = new Chart(ctx, {
        type: 'bar',  // Измените тип графика, если хотите 'line' или 'bar'
        data: {
            labels: labels,
            datasets: [{
                label: 'Выручка',
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1000  // Настроить шаг оси Y, если необходимо
                    }
                }
            }
        }
    });
}
