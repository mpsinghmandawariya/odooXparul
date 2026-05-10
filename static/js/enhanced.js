// ══════════════════════════════════════════════════════════════════════════════
// TRAVELOOP - Enhanced JavaScript
// ══════════════════════════════════════════════════════════════════════════════

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

// ══════════════════════════════════════════════════════════════════════════════
// ENHANCED FEATURES - Phase 6
// ══════════════════════════════════════════════════════════════════════════════

// ── Toast Notification System ────────────────────────────────────────────────
const Toast = {
  container: null,
  
  init() {
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.className = 'toast-container';
      this.container.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        display: flex;
        flex-direction: column;
        gap: 10px;
      `;
      document.body.appendChild(this.container);
    }
  },
  
  show(message, type = 'info', duration = 3000) {
    this.init();
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icons = {
      success: 'fa-check-circle',
      error: 'fa-exclamation-circle',
      warning: 'fa-exclamation-triangle',
      info: 'fa-info-circle'
    };
    
    const colors = {
      success: '#22c55e',
      error: '#ef4444',
      warning: '#f59e0b',
      info: '#3b82f6'
    };
    
    toast.style.cssText = `
      background: rgba(30, 41, 59, 0.95);
      backdrop-filter: blur(10px);
      border: 1px solid ${colors[type]};
      border-left: 4px solid ${colors[type]};
      border-radius: 8px;
      padding: 12px 16px;
      min-width: 300px;
      max-width: 400px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
      display: flex;
      align-items: center;
      gap: 12px;
      color: #f8fafc;
      animation: slideIn 0.3s ease;
    `;
    
    toast.innerHTML = `
      <i class="fa ${icons[type]}" style="color: ${colors[type]}; font-size: 1.2rem;"></i>
      <span style="flex: 1;">${message}</span>
      <button onclick="this.parentElement.remove()" style="background: none; border: none; color: #94a3b8; cursor: pointer; font-size: 1.2rem;">
        <i class="fa fa-times"></i>
      </button>
    `;
    
    this.container.appendChild(toast);
    
    setTimeout(() => {
      toast.style.animation = 'slideOut 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  },
  
  success(message, duration) { this.show(message, 'success', duration); },
  error(message, duration) { this.show(message, 'error', duration); },
  warning(message, duration) { this.show(message, 'warning', duration); },
  info(message, duration) { this.show(message, 'info', duration); }
};

// Add animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from { transform: translateX(400px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  @keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(400px); opacity: 0; }
  }
`;
document.head.appendChild(style);

// ── Modal System ─────────────────────────────────────────────────────────────
const Modal = {
  create(title, content, buttons = []) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(5px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9999;
      animation: fadeIn 0.3s ease;
    `;
    
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.cssText = `
      background: #1e293b;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 16px;
      padding: 0;
      max-width: 500px;
      width: 90%;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
      animation: scaleIn 0.3s ease;
    `;
    
    const header = document.createElement('div');
    header.style.cssText = `
      padding: 20px 24px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      justify-content: space-between;
      align-items: center;
    `;
    header.innerHTML = `
      <h3 style="margin: 0; color: #f8fafc; font-size: 1.25rem;">${title}</h3>
      <button onclick="this.closest('.modal-overlay').remove()" style="background: none; border: none; color: #94a3b8; cursor: pointer; font-size: 1.5rem;">
        <i class="fa fa-times"></i>
      </button>
    `;
    
    const body = document.createElement('div');
    body.style.cssText = `padding: 24px; color: #cbd5e1; line-height: 1.6;`;
    body.innerHTML = content;
    
    const footer = document.createElement('div');
    footer.style.cssText = `
      padding: 16px 24px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      gap: 12px;
      justify-content: flex-end;
    `;
    
    buttons.forEach(btn => {
      const button = document.createElement('button');
      button.textContent = btn.text;
      button.className = btn.class || 'btn btn-secondary';
      button.onclick = () => {
        if (btn.onClick) btn.onClick();
        overlay.remove();
      };
      footer.appendChild(button);
    });
    
    modal.appendChild(header);
    modal.appendChild(body);
    if (buttons.length > 0) modal.appendChild(footer);
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) overlay.remove();
    });
    
    return overlay;
  },
  
  confirm(title, message, onConfirm) {
    return this.create(title, message, [
      { text: 'Cancel', class: 'btn btn-secondary' },
      { text: 'Confirm', class: 'btn btn-primary', onClick: onConfirm }
    ]);
  },
  
  alert(title, message) {
    return this.create(title, message, [
      { text: 'OK', class: 'btn btn-primary' }
    ]);
  }
};

// Add modal animations
const modalStyle = document.createElement('style');
modalStyle.textContent = `
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  @keyframes scaleIn {
    from { transform: scale(0.9); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
  }
`;
document.head.appendChild(modalStyle);

// ── Form Validation ──────────────────────────────────────────────────────────
const FormValidator = {
  validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  },
  
  validatePassword(password) {
    return password.length >= 8;
  },
  
  validateRequired(value) {
    return value && value.trim().length > 0;
  },
  
  validateDate(date) {
    return !isNaN(Date.parse(date));
  },
  
  validateNumber(value) {
    return !isNaN(parseFloat(value)) && isFinite(value);
  },
  
  showError(input, message) {
    const error = document.createElement('div');
    error.className = 'validation-error';
    error.style.cssText = `
      color: #ef4444;
      font-size: 0.875rem;
      margin-top: 4px;
    `;
    error.textContent = message;
    
    const existing = input.parentElement.querySelector('.validation-error');
    if (existing) existing.remove();
    
    input.style.borderColor = '#ef4444';
    input.parentElement.appendChild(error);
  },
  
  clearError(input) {
    const error = input.parentElement.querySelector('.validation-error');
    if (error) error.remove();
    input.style.borderColor = '';
  },
  
  validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    let isValid = true;
    const inputs = form.querySelectorAll('[required]');
    
    inputs.forEach(input => {
      this.clearError(input);
      
      if (!this.validateRequired(input.value)) {
        this.showError(input, 'This field is required');
        isValid = false;
      } else if (input.type === 'email' && !this.validateEmail(input.value)) {
        this.showError(input, 'Please enter a valid email');
        isValid = false;
      } else if (input.type === 'password' && !this.validatePassword(input.value)) {
        this.showError(input, 'Password must be at least 8 characters');
        isValid = false;
      } else if (input.type === 'number' && !this.validateNumber(input.value)) {
        this.showError(input, 'Please enter a valid number');
        isValid = false;
      }
    });
    
    return isValid;
  }
};

// ── Real-time Budget Calculator ──────────────────────────────────────────────
function calculateBudget() {
  const budgetInputs = document.querySelectorAll('[data-budget]');
  const costInputs = document.querySelectorAll('[data-cost]');
  
  let totalBudget = 0;
  let totalCost = 0;
  
  budgetInputs.forEach(input => {
    const value = parseFloat(input.value) || 0;
    totalBudget += value;
  });
  
  costInputs.forEach(input => {
    const value = parseFloat(input.value) || 0;
    totalCost += value;
  });
  
  const remaining = totalBudget - totalCost;
  
  const totalBudgetEl = document.getElementById('totalBudget');
  const totalCostEl = document.getElementById('totalCost');
  const remainingEl = document.getElementById('remaining');
  
  if (totalBudgetEl) totalBudgetEl.textContent = `$${totalBudget.toFixed(2)}`;
  if (totalCostEl) totalCostEl.textContent = `$${totalCost.toFixed(2)}`;
  if (remainingEl) {
    remainingEl.textContent = `$${remaining.toFixed(2)}`;
    remainingEl.style.color = remaining >= 0 ? '#22c55e' : '#ef4444';
  }
}

// ── Loading State ────────────────────────────────────────────────────────────
function showLoading(element) {
  const loader = document.createElement('div');
  loader.className = 'loader';
  loader.style.cssText = `
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: #3b82f6;
    animation: spin 1s linear infinite;
  `;
  
  const spinStyle = document.createElement('style');
  spinStyle.textContent = `
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
  `;
  document.head.appendChild(spinStyle);
  
  element.disabled = true;
  element.dataset.originalText = element.innerHTML;
  element.innerHTML = '';
  element.appendChild(loader);
}

function hideLoading(element) {
  element.disabled = false;
  element.innerHTML = element.dataset.originalText || 'Submit';
}

// ── Confirmation Dialogs ─────────────────────────────────────────────────────
function confirmDelete(message, onConfirm) {
  Modal.confirm(
    'Confirm Delete',
    message || 'Are you sure you want to delete this item? This action cannot be undone.',
    onConfirm
  );
}

// ── Image Preview ────────────────────────────────────────────────────────────
function previewImage(input, previewId) {
  const preview = document.getElementById(previewId);
  if (!preview) return;
  
  const file = input.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      preview.src = e.target.result;
      preview.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
}

// ── Copy to Clipboard ────────────────────────────────────────────────────────
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    Toast.success('Copied to clipboard!');
  }).catch(() => {
    Toast.error('Failed to copy');
  });
}

// ── Debounce Function ────────────────────────────────────────────────────────
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// ── Auto-save Functionality ──────────────────────────────────────────────────
function enableAutoSave(formId, saveCallback, interval = 30000) {
  const form = document.getElementById(formId);
  if (!form) return;
  
  let autoSaveTimer;
  const inputs = form.querySelectorAll('input, textarea, select');
  
  inputs.forEach(input => {
    input.addEventListener('input', () => {
      clearTimeout(autoSaveTimer);
      autoSaveTimer = setTimeout(() => {
        saveCallback(new FormData(form));
        Toast.info('Auto-saved', 2000);
      }, interval);
    });
  });
}

// ── Export Functions ─────────────────────────────────────────────────────────
window.Toast = Toast;
window.Modal = Modal;
window.FormValidator = FormValidator;
window.calculateBudget = calculateBudget;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.confirmDelete = confirmDelete;
window.previewImage = previewImage;
window.copyToClipboard = copyToClipboard;
window.debounce = debounce;
window.enableAutoSave = enableAutoSave;

// ── Initialize ───────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Auto-calculate budget on input change
  document.querySelectorAll('[data-budget], [data-cost]').forEach(input => {
    input.addEventListener('input', debounce(calculateBudget, 500));
  });
  
  // Initialize tooltips
  document.querySelectorAll('[data-tooltip]').forEach(el => {
    el.addEventListener('mouseenter', function() {
      const tooltip = document.createElement('div');
      tooltip.className = 'tooltip';
      tooltip.textContent = this.dataset.tooltip;
      tooltip.style.cssText = `
        position: absolute;
        background: #1e293b;
        color: #f8fafc;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 0.875rem;
        z-index: 10000;
        pointer-events: none;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
      `;
      document.body.appendChild(tooltip);
      
      const rect = this.getBoundingClientRect();
      tooltip.style.top = `${rect.top - tooltip.offsetHeight - 8}px`;
      tooltip.style.left = `${rect.left + (rect.width - tooltip.offsetWidth) / 2}px`;
      
      this.addEventListener('mouseleave', () => tooltip.remove(), { once: true });
    });
  });
});
