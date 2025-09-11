// Main JavaScript for Job Matching Platform Analysis

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all charts
    initializeCharts();
    
    // Add smooth scrolling
    addSmoothScrolling();
    
    // Add animation on scroll
    addScrollAnimations();
    
    // Initialize tooltips
    initializeTooltips();
});

function initializeCharts() {
    // Market Growth Chart
    const marketCtx = document.getElementById('marketGrowthChart');
    if (marketCtx) {
        new Chart(marketCtx, {
            type: 'line',
            data: {
                labels: ['2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'],
                datasets: [{
                    label: 'Market Size (Billions USD)',
                    data: [8.2, 9.1, 10.3, 11.5, 12.4, 13.2, 15.1, 17.3, 19.8, 22.7, 26.0, 29.8],
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Recruitment Technology Market Growth (2019-2030)',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Market Size (Billions USD)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Year'
                        }
                    }
                }
            }
        });
    }

    // AI Adoption Chart
    const aiCtx = document.getElementById('aiAdoptionChart');
    if (aiCtx) {
        new Chart(aiCtx, {
            type: 'doughnut',
            data: {
                labels: ['Using AI', 'Not Using AI'],
                datasets: [{
                    data: [52, 48],
                    backgroundColor: ['#10b981', '#e5e7eb'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'AI Adoption in Recruitment (2024)',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // Future Projections Chart
    const futureCtx = document.getElementById('futureProjectionsChart');
    if (futureCtx) {
        new Chart(futureCtx, {
            type: 'bar',
            data: {
                labels: ['AI Adoption', 'Remote Work', 'Gig Economy', 'Market Size'],
                datasets: [{
                    label: '2024',
                    data: [52, 45, 32, 13.2],
                    backgroundColor: '#2563eb'
                }, {
                    label: '2030',
                    data: [94, 65, 56, 29.8],
                    backgroundColor: '#10b981'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Future Projections (2024 vs 2030)',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Percentage / Billions USD'
                        }
                    }
                }
            }
        });
    }

    // Financial Projections Chart
    const financialCtx = document.getElementById('financialProjectionsChart');
    if (financialCtx) {
        new Chart(financialCtx, {
            type: 'line',
            data: {
                labels: ['Year 1', 'Year 2', 'Year 3'],
                datasets: [{
                    label: 'Revenue (Millions)',
                    data: [3.6, 10.8, 27.0],
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }, {
                    label: 'Profit (Millions)',
                    data: [2.6, 8.6, 23.5],
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Financial Projections (Freemium Model)',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Millions USD'
                        }
                    }
                }
            }
        });
    }
}

function addSmoothScrolling() {
    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function addScrollAnimations() {
    // Create intersection observer for animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, {
        threshold: 0.1
    });

    // Observe all metric cards and feature cards
    document.querySelectorAll('.metric-card, .feature-card, .business-tier').forEach(card => {
        observer.observe(card);
    });
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 1
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('en-US').format(number);
}

function formatPercentage(number) {
    return new Intl.NumberFormat('en-US', {
        style: 'percent',
        minimumFractionDigits: 1,
        maximumFractionDigits: 1
    }).format(number / 100);
}

// API functions
async function fetchMarketData() {
    try {
        const response = await fetch('/api/market-data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching market data:', error);
        return null;
    }
}

async function fetchFinancialProjections() {
    try {
        const response = await fetch('/api/financial-projections');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching financial projections:', error);
        return null;
    }
}

// Export functions for use in other scripts
window.JobMatchingPlatform = {
    formatCurrency,
    formatNumber,
    formatPercentage,
    fetchMarketData,
    fetchFinancialProjections
};


