/* =========================================================
   GITANJALI RUBBER STAMP PAGE — INTERACTIONS
========================================================= */
(function () {
    'use strict';

    /* -----------------------------------------------------
       1. SCROLL-TRIGGERED REVEAL (IntersectionObserver)
    ----------------------------------------------------- */
    const reveals = document.querySelectorAll('.stamp-reveal');

    if ('IntersectionObserver' in window) {
        const io = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });

        reveals.forEach((el) => io.observe(el));
    } else {
        reveals.forEach((el) => el.classList.add('is-visible'));
    }


    /* -----------------------------------------------------
       2. HERO TILT — mouse parallax on hero visual
    ----------------------------------------------------- */
    const tilt = document.querySelector('[data-tilt]');
    const showcase = tilt ? tilt.querySelector('.stamp-showcase-card') : null;
    const floaters = tilt ? tilt.querySelectorAll('.floating-stamp') : [];

    if (tilt && showcase && window.matchMedia('(hover: hover)').matches) {
        const MAX = 8; // degrees

        tilt.addEventListener('mousemove', (e) => {
            const rect = tilt.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;

            showcase.style.transform =
                `rotate(${3 + x * MAX}deg) translate3d(${x * 10}px, ${y * 10}px, 0)`;

            floaters.forEach((f, i) => {
                const dir = i % 2 === 0 ? 1 : -1;
                f.style.transform =
                    `translate3d(${x * 14 * dir}px, ${y * 12 * dir}px, 0)`;
            });
        });

        tilt.addEventListener('mouseleave', () => {
            showcase.style.transform = '';
            floaters.forEach((f) => (f.style.transform = ''));
        });
    }


    /* -----------------------------------------------------
       3. STAMP "PRESS" EFFECT — click on circular stamp
    ----------------------------------------------------- */
    const pressTargets = document.querySelectorAll('[data-press], .stamp-circle');

    pressTargets.forEach((el) => {
        el.addEventListener('click', () => {
            el.classList.remove('pressing');
            // force reflow so animation can replay
            void el.offsetWidth;
            el.classList.add('pressing');

            setTimeout(() => el.classList.remove('pressing'), 700);
        });
    });


    /* -----------------------------------------------------
       4. TRUST COUNTERS — animate numbers
    ----------------------------------------------------- */
    const counterWrap = document.querySelector('[data-counters]');

    if (counterWrap && 'IntersectionObserver' in window) {
        const counters = counterWrap.querySelectorAll('[data-count]');
        let started = false;

        const runCount = (el) => {
            const target = parseInt(el.getAttribute('data-count'), 10) || 0;
            const duration = 1400;
            const start = performance.now();

            const tick = (now) => {
                const p = Math.min((now - start) / duration, 1);
                // easeOutCubic
                const eased = 1 - Math.pow(1 - p, 3);
                el.textContent = String(Math.round(target * eased)).padStart(2, '0');
                if (p < 1) requestAnimationFrame(tick);
                else el.textContent = String(target).padStart(2, '0');
            };
            requestAnimationFrame(tick);
        };

        const counterIO = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting && !started) {
                    started = true;
                    counters.forEach(runCount);
                    counterIO.disconnect();
                }
            });
        }, { threshold: 0.5 });

        counterIO.observe(counterWrap);
    }


    /* -----------------------------------------------------
       5. SMOOTH ANCHOR SCROLL (#stamp-types)
    ----------------------------------------------------- */
    document.querySelectorAll('a[href^="#"]').forEach((a) => {
        a.addEventListener('click', (e) => {
            const id = a.getAttribute('href');
            if (id.length < 2) return;
            const target = document.querySelector(id);
            if (!target) return;
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });

})();

    /* -----------------------------------------------------
       6. CARD 9 VIDEO — play only when in view
    ----------------------------------------------------- */
    const cardVideo = document.querySelector('.stamp-card-video');

    if (cardVideo && 'IntersectionObserver' in window) {
        // Start paused so autoplay doesn't fire off-screen
        cardVideo.pause();

        const videoIO = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    // Some browsers reject play() if not muted; already muted in HTML
                    const playPromise = cardVideo.play();
                    if (playPromise && typeof playPromise.catch === 'function') {
                        playPromise.catch(() => { /* autoplay blocked — poster stays */ });
                    }
                } else {
                    cardVideo.pause();
                }
            });
        }, { threshold: 0.35 });

        videoIO.observe(cardVideo);

        // Pause when the tab is hidden (battery / CPU friendly)
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                cardVideo.pause();
            } else if (isElementInViewport(cardVideo)) {
                cardVideo.play().catch(() => {});
            }
        });
    }

    function isElementInViewport(el) {
        const r = el.getBoundingClientRect();
        return (
            r.top < (window.innerHeight || document.documentElement.clientHeight) &&
            r.bottom > 0
        );
    }

        /* -----------------------------------------------------
       7. CARD 9 VIDEO — unmute button
    ----------------------------------------------------- */
    const soundBtn = document.querySelector('.stamp-card-sound');
    const v = document.querySelector('.stamp-card-video');

    if (soundBtn && v) {
        soundBtn.addEventListener('click', () => {
            v.muted = !v.muted;
            v.classList.toggle('is-unmuted', !v.muted);
            if (!v.muted) v.play().catch(() => {});
        });
    }