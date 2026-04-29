// DreamSpin Casino - Elite JavaScript System

// ================================
// Theme Management
// ================================
const ThemeManager = {
    init() {
        this.themeToggle = document.getElementById('themeToggle');
        this.themeIcon = document.querySelector('.theme-icon');
        this.currentTheme = localStorage.getItem('theme') || 'light';
        
        this.setTheme(this.currentTheme);
        this.bindEvents();
    },

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        if (this.themeIcon) {
            this.themeIcon.textContent = theme === 'light' ? '🌙' : '☀️';
        }
    },

    toggle() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.currentTheme = newTheme;
        this.setTheme(newTheme);
    },

    bindEvents() {
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => this.toggle());
        }
    }
};

// ================================
// Hamburger Menu
// ================================
const MenuManager = {
    init() {
        this.hamburger = document.getElementById('hamburger');
        this.navMenu = document.getElementById('navMenu');
        
        if (this.hamburger && this.navMenu) {
            this.bindEvents();
        }
    },

    toggle() {
        this.navMenu.classList.toggle('active');
        this.hamburger.classList.toggle('active');
        document.body.style.overflow = this.navMenu.classList.contains('active') ? 'hidden' : '';
    },

    close() {
        this.navMenu.classList.remove('active');
        this.hamburger.classList.remove('active');
        document.body.style.overflow = '';
    },

    bindEvents() {
        // Toggle on hamburger click
        this.hamburger.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggle();
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!this.navMenu.contains(e.target) && !this.hamburger.contains(e.target)) {
                this.close();
            }
        });

        // Close on link click
        this.navMenu.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => this.close());
        });
    }
};

// ================================
// Flash Message Management
// ================================
const FlashManager = {
    init() {
        this.messages = document.querySelectorAll('.flash-messages > div');
        this.autoDismiss();
    },

    autoDismiss() {
        this.messages.forEach(message => {
            // Add close button
            const closeBtn = document.createElement('span');
            closeBtn.innerHTML = '×';
            closeBtn.style.cssText = 'float: right; cursor: pointer; font-size: 1.5rem; margin-left: 1rem; opacity: 0.8;';
            closeBtn.onclick = () => this.dismiss(message);
            message.prepend(closeBtn);

            // Auto dismiss after 5 seconds
            setTimeout(() => this.dismiss(message), 5000);
        });
    },

    dismiss(message) {
        message.style.opacity = '0';
        message.style.transform = 'translateX(100%)';
        setTimeout(() => message.remove(), 300);
    }
};

// ================================
// Balance Display Management
// ================================
window.updateBalance = (newBalance) => {
    const balanceDisplay = document.getElementById('balanceDisplay');
    if (balanceDisplay) {
        // Animate the update
        balanceDisplay.style.transform = 'scale(1.2)';
        balanceDisplay.style.color = 'var(--success-color)';
        
        setTimeout(() => {
            balanceDisplay.textContent = '$' + parseFloat(newBalance).toFixed(2);
            balanceDisplay.style.transform = 'scale(1)';
        }, 150);
    }
};

// ================================
// Navigation Helper
// ================================
window.goToDeposit = () => {
    window.location.href = '/deposit/crypto';
};

// ================================
// Smooth Scroll Enhancement
// ================================
const SmoothScroll = {
    init() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
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
};

// ================================
// Intersection Observer for Animations
// ================================
const AnimationObserver = {
    init() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, {
            threshold: 0.1
        });

        document.querySelectorAll('.card, .stat-card, .game-card').forEach(el => {
            observer.observe(el);
        });
    }
};

// ================================
// Performance Monitoring
// ================================
const PerformanceMonitor = {
    init() {
        if ('performance' in window) {
            window.addEventListener('load', () => {
                const perfData = window.performance.timing;
                const loadTime = perfData.loadEventEnd - perfData.navigationStart;
                console.log(`🚀 Page loaded in ${loadTime}ms`);
            });
        }
    }
};

// ================================
// Initialize Everything
// ================================
document.addEventListener('DOMContentLoaded', () => {
    // Core Systems
    ThemeManager.init();
    MenuManager.init();
    FlashManager.init();
    SmoothScroll.init();
    AnimationObserver.init();
    PerformanceMonitor.init();

    // Log initialization
    console.log('🎰 DreamSpin Casino - Elite System Loaded');
});

// ================================
// Export for Testing
// ================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ThemeManager,
        MenuManager,
        FlashManager,
        updateBalance: window.updateBalance,
        goToDeposit: window.goToDeposit
    };
}