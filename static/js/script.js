// ── Password Toggle ──────────────────────────────────────────────────────────
function togglePassword(inputId, btn) {
  const input = document.getElementById(inputId);
  const icon = btn.querySelector('i');
  if (input.type === 'password') {
    input.type = 'text';
    icon.classList.replace('fa-eye', 'fa-eye-slash');
  } else {
    input.type = 'password';
    icon.classList.replace('fa-eye-slash', 'fa-eye');
  }
}

// ── Password Strength ────────────────────────────────────────────────────────
function checkStrength(val) {
  const fill = document.getElementById('strengthFill');
  const label = document.getElementById('strengthLabel');
  if (!fill) return;
  let score = 0;
  if (val.length >= 8) score++;
  if (/[A-Z]/.test(val)) score++;
  if (/[0-9]/.test(val)) score++;
  if (/[^A-Za-z0-9]/.test(val)) score++;
  const levels = [
    { w: '0%', color: 'transparent', text: '' },
    { w: '25%', color: '#ef4444', text: 'Weak' },
    { w: '50%', color: '#f59e0b', text: 'Fair' },
    { w: '75%', color: '#3b82f6', text: 'Good' },
    { w: '100%', color: '#22c55e', text: 'Strong' },
  ];
  const lvl = levels[score];
  fill.style.width = lvl.w;
  fill.style.background = lvl.color;
  label.textContent = lvl.text;
  label.style.color = lvl.color;
}

// ── Sidebar Toggle ───────────────────────────────────────────────────────────
function toggleSidebar() {
  document.getElementById('sidebar')?.classList.toggle('open');
}

// Close sidebar on outside click (mobile)
document.addEventListener('click', (e) => {
  const sidebar = document.getElementById('sidebar');
  const toggle = document.querySelector('.sidebar-toggle');
  if (sidebar && sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== toggle) {
    sidebar.classList.remove('open');
  }
});

// ── Trip Search Filter ───────────────────────────────────────────────────────
function filterTrips(query) {
  const cards = document.querySelectorAll('.trip-card');
  const q = query.toLowerCase();
  cards.forEach(card => {
    const name = card.dataset.name || '';
    card.style.display = name.includes(q) ? '' : 'none';
  });
}

// ── Filter by Status ─────────────────────────────────────────────────────────
function filterByStatus(status, btn) {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const today = new Date().toISOString().split('T')[0];
  document.querySelectorAll('.trip-card').forEach(card => {
    const start = card.dataset.start || '';
    if (status === 'all') { card.style.display = ''; return; }
    if (status === 'upcoming') card.style.display = (!start || start >= today) ? '' : 'none';
    if (status === 'past') card.style.display = (start && start < today) ? '' : 'none';
  });
}

// ── Auto-dismiss Flash Messages ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => el.remove(), 5000);
  });
});
