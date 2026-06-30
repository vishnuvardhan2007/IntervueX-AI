document.addEventListener('DOMContentLoaded', () => {

  // ── Loading state on form submit ──
  const form = document.getElementById('interview-form');
  if (form) {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('.btn-primary');
      if (btn) {
        btn.classList.add('loading');
        btn.textContent = 'Generating…';
      }
    });
  }

  // ── Toggle follow-up hints ──
  document.querySelectorAll('.toggle-followup').forEach(btn => {
    btn.addEventListener('click', () => {
      const card  = btn.closest('.question-card');
      const hint  = card.querySelector('.q-followup');
      const open  = hint.classList.toggle('visible');
      btn.querySelector('.arrow').textContent = open ? '▲' : '▼';
      btn.querySelector('.label').textContent = open ? 'Hide follow-up' : 'Show follow-up';
    });
  });

  // ── Print button ──
  const printBtn = document.getElementById('print-btn');
  if (printBtn) {
    printBtn.addEventListener('click', () => window.print());
  }

  // ── Expand all / collapse all ──
  const expandAll = document.getElementById('expand-all');
  if (expandAll) {
    let allOpen = false;
    expandAll.addEventListener('click', () => {
      allOpen = !allOpen;
      document.querySelectorAll('.q-followup').forEach(el => {
        el.classList.toggle('visible', allOpen);
      });
      document.querySelectorAll('.toggle-followup').forEach(btn => {
        btn.querySelector('.arrow').textContent = allOpen ? '▲' : '▼';
        btn.querySelector('.label').textContent = allOpen ? 'Hide follow-up' : 'Show follow-up';
      });
      expandAll.textContent = allOpen ? 'Collapse All' : 'Expand All';
    });
  }

});
