/* Shapeshifters Healthcare — Main JS */

// ── Mobile nav toggle ────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  const hamburger = document.querySelector('.hamburger');
  const nav = document.querySelector('.site-nav');
  if (hamburger && nav) {
    hamburger.addEventListener('click', function () {
      nav.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', nav.classList.contains('open'));
    });
  }

  // ── Auto-generate table of contents from H2s ────────
  const tocList = document.getElementById('toc-list');
  if (tocList) {
    const headings = document.querySelectorAll('.prose h2');
    headings.forEach(function (h, i) {
      if (!h.id) h.id = 'section-' + i;
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.textContent;
      li.appendChild(a);
      tocList.appendChild(li);
    });
    if (headings.length === 0 && tocList.closest('.toc')) {
      tocList.closest('.toc').style.display = 'none';
    }
  }

  // ── Lazy-load images ─────────────────────────────────
  if ('IntersectionObserver' in window) {
    const lazyImages = document.querySelectorAll('img[data-src]');
    const imgObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          imgObserver.unobserve(img);
        }
      });
    });
    lazyImages.forEach(function (img) { imgObserver.observe(img); });
  }

  // ── FAQ accordion ────────────────────────────────────
  document.querySelectorAll('.faq-question').forEach(function (question) {
    question.addEventListener('click', function () {
      const answer = this.nextElementSibling;
      const isOpen = answer.style.display === 'block';
      // Close all
      document.querySelectorAll('.faq-answer').forEach(function (a) { a.style.display = 'none'; });
      document.querySelectorAll('.faq-question').forEach(function (q) { q.setAttribute('aria-expanded', 'false'); });
      // Open clicked
      if (!isOpen) {
        answer.style.display = 'block';
        this.setAttribute('aria-expanded', 'true');
      }
    });
    // Hide answers initially
    const answer = question.nextElementSibling;
    if (answer && answer.classList.contains('faq-answer')) {
      answer.style.display = 'none';
    }
  });

  // ── Smooth scroll for anchor links ───────────────────
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
});
