document.addEventListener("DOMContentLoaded", function () {
    const colors = ["#d63384", "#ffc107", "#6f42c1", "#6c757d"];

    const pieCtx = document.getElementById("pieChart");
    if (pieCtx) {
        new Chart(pieCtx, {
            type: "pie",
            data: {
                labels: chartLabels,
                datasets: [
                    {
                        data: chartData,
                        backgroundColor: colors,
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: "bottom",
                    },
                },
            },
        });
    }

    const barCtx = document.getElementById("barChart");
    if (barCtx) {
        new Chart(barCtx, {
            type: "bar",
            data: {
                labels: chartLabels,
                datasets: [
                    {
                        label: "Number of Reports",
                        data: chartData,
                        backgroundColor: colors,
                    },
                ],
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                        },
                    },
                },
                plugins: {
                    legend: {
                        display: false,
                    },
                },
            },
        });
    }
});