// Barrett Realty - Main JavaScript with Animations

document.addEventListener('DOMContentLoaded', function() {
    // Page loader
    const loader = document.querySelector('.page-loader');
    if (loader) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                loader.classList.add('hidden');
            }, 500);
        });
    }

    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuToggle && navLinks) {
        mobileMenuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            this.classList.toggle('active');
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                mobileMenuToggle.classList.remove('active');
            });
        });
    }

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');

    function handleScroll() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    window.addEventListener('scroll', handleScroll);
    handleScroll();

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                const navHeight = navbar.offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ===================================
    // SCROLL REVEAL ANIMATIONS
    // ===================================

    // Add reveal classes to elements
    function addRevealClasses() {
        // Service cards
        document.querySelectorAll('.service-card').forEach((card, index) => {
            card.classList.add('reveal', `stagger-${(index % 3) + 1}`);
        });

        // Property cards
        document.querySelectorAll('.property-card').forEach((card, index) => {
            card.classList.add('reveal', `stagger-${(index % 3) + 1}`);
        });

        // Testimonial cards
        document.querySelectorAll('.testimonial-card').forEach((card, index) => {
            card.classList.add('reveal', `stagger-${(index % 3) + 1}`);
        });

        // Section headers
        document.querySelectorAll('.section-header').forEach(header => {
            header.classList.add('reveal');
        });

        // About content
        const aboutContent = document.querySelector('.about-content');
        if (aboutContent) aboutContent.classList.add('reveal-left');

        const aboutImage = document.querySelector('.about-image');
        if (aboutImage) aboutImage.classList.add('reveal-right');

        // Contact sections
        const contactInfo = document.querySelector('.contact-info');
        if (contactInfo) contactInfo.classList.add('reveal-left');

        const contactForm = document.querySelector('.contact-form-wrapper');
        if (contactForm) contactForm.classList.add('reveal-right');

        // CTA content
        const ctaContent = document.querySelector('.cta-content');
        if (ctaContent) ctaContent.classList.add('reveal-scale');

        // Credential items
        document.querySelectorAll('.credential-item').forEach((item, index) => {
            item.classList.add('reveal', `stagger-${(index % 4) + 1}`);
        });

        // Feature items
        document.querySelectorAll('.feature-item').forEach((item, index) => {
            item.classList.add('reveal', `stagger-${(index % 4) + 1}`);
        });
    }

    addRevealClasses();

    // Intersection Observer for reveal animations
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    // Observe all reveal elements
    document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale').forEach(el => {
        revealObserver.observe(el);
    });

    // ===================================
    // PARALLAX EFFECT FOR HERO
    // ===================================

    const heroBackground = document.querySelector('.hero-background');

    if (heroBackground) {
        let ticking = false;

        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    const scrolled = window.pageYOffset;
                    const rate = scrolled * 0.3;

                    if (scrolled < window.innerHeight) {
                        heroBackground.style.transform = `scale(${1 + scrolled * 0.0002}) translateY(${rate}px)`;
                    }

                    ticking = false;
                });

                ticking = true;
            }
        });
    }

    // ===================================
    // COUNTER ANIMATION FOR STATS
    // ===================================

    function animateCounter(element, target, duration = 2000) {
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target + (element.dataset.suffix || '');
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current) + (element.dataset.suffix || '');
            }
        }, 16);
    }

    // Observe stats for counter animation
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statNumber = entry.target.querySelector('.stat-number');
                if (statNumber && !statNumber.dataset.animated) {
                    const text = statNumber.textContent;
                    const number = parseInt(text.replace(/\D/g, ''));
                    const suffix = text.replace(/[0-9]/g, '');

                    statNumber.dataset.suffix = suffix;
                    statNumber.dataset.animated = 'true';
                    animateCounter(statNumber, number);
                }
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.stat-item').forEach(stat => {
        statsObserver.observe(stat);
    });

    // ===================================
    // FORM HANDLING
    // ===================================

    const contactFormEl = document.getElementById('contactForm');

    if (contactFormEl) {
        contactFormEl.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });

            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;

            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;
            submitBtn.style.transform = 'scale(0.98)';

            setTimeout(() => {
                submitBtn.textContent = 'Message Sent!';
                submitBtn.style.background = '#4caf50';
                submitBtn.style.transform = 'scale(1)';

                setTimeout(() => {
                    this.reset();
                    submitBtn.textContent = originalText;
                    submitBtn.style.background = '';
                    submitBtn.disabled = false;

                    // Success animation
                    const wrapper = document.querySelector('.contact-form-wrapper');
                    wrapper.style.transform = 'scale(1.02)';
                    setTimeout(() => {
                        wrapper.style.transform = '';
                    }, 200);

                    alert('Thank you for contacting Barrett Realty! We will be in touch within 24 hours.');
                }, 1000);
            }, 1500);

            console.log('Form submitted:', data);
        });
    }

    // ===================================
    // PHONE NUMBER FORMATTING
    // ===================================

    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 0) {
                if (value.length <= 3) {
                    value = '(' + value;
                } else if (value.length <= 6) {
                    value = '(' + value.substring(0, 3) + ') ' + value.substring(3);
                } else {
                    value = '(' + value.substring(0, 3) + ') ' + value.substring(3, 6) + '-' + value.substring(6, 10);
                }
            }
            e.target.value = value;
        });
    }

    // ===================================
    // HOVER EFFECTS ENHANCEMENT
    // ===================================

    // Property card image zoom on hover
    document.querySelectorAll('.property-card').forEach(card => {
        const image = card.querySelector('.property-image');
        if (image) {
            card.addEventListener('mouseenter', () => {
                image.style.transform = 'scale(1.05)';
            });
            card.addEventListener('mouseleave', () => {
                image.style.transform = 'scale(1)';
            });
        }
    });

    // ===================================
    // SCROLL PROGRESS INDICATOR
    // ===================================

    // Create scroll progress bar
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        z-index: 9999;
        transition: width 0.1s ease;
        width: 0%;
    `;
    document.body.appendChild(progressBar);

    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        progressBar.style.width = scrollPercent + '%';
    });

    // ===================================
    // CURSOR FOLLOWER (Optional - Desktop Only)
    // ===================================

    if (window.innerWidth > 1024) {
        const cursor = document.createElement('div');
        cursor.style.cssText = `
            position: fixed;
            width: 20px;
            height: 20px;
            border: 2px solid var(--primary);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9998;
            transition: transform 0.15s ease, opacity 0.15s ease;
            opacity: 0;
        `;
        document.body.appendChild(cursor);

        document.addEventListener('mousemove', (e) => {
            cursor.style.opacity = '1';
            cursor.style.left = e.clientX - 10 + 'px';
            cursor.style.top = e.clientY - 10 + 'px';
        });

        document.addEventListener('mouseleave', () => {
            cursor.style.opacity = '0';
        });

        // Scale cursor on interactive elements
        document.querySelectorAll('a, button, .btn, .service-card, .property-card, .testimonial-card').forEach(el => {
            el.addEventListener('mouseenter', () => {
                cursor.style.transform = 'scale(2)';
                cursor.style.borderColor = 'var(--accent)';
            });
            el.addEventListener('mouseleave', () => {
                cursor.style.transform = 'scale(1)';
                cursor.style.borderColor = 'var(--primary)';
            });
        });
    }

    // ===================================
    // LAZY LOADING IMAGES
    // ===================================

    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.classList.add('loaded');
                    }
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
});

// Track page views
function trackPageView(page) {
    console.log('Page viewed:', page || window.location.pathname);
}

trackPageView();
