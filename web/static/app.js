/* BookForge AI — frontend polling for job status */

async function pollJob(jobId) {
  const logEl      = document.getElementById('job-log');
  const statusEl   = document.getElementById('job-status');
  const progressEl = document.getElementById('job-progress');
  const dlBtn      = document.getElementById('download-btn');
  const spinner    = document.getElementById('spinner');

  if (!logEl) return;

  const poll = async () => {
    try {
      const res  = await fetch(`/api/job/${jobId}`);
      const data = await res.json();

      // Status badge
      const statusMap = {
        queued:     ['⏳ Queued',      'badge-warning'],
        generating: ['⚙️ Generating',  'badge-info'],
        converting: ['📦 Converting',  'badge-info'],
        done:       ['✅ Done',         'badge-success'],
        error:      ['❌ Error',        'badge-error'],
      };
      const [label, cls] = statusMap[data.status] || ['Unknown', 'badge-ghost'];
      statusEl.className = `badge ${cls} badge-lg`;
      statusEl.textContent = label;

      // Progress bar
      const { done, total } = data.progress || {};
      if (total > 0) {
        const pct = Math.round((done / total) * 100);
        progressEl.style.width = pct + '%';
        progressEl.textContent = `${done}/${total}`;
      }

      // Log lines
      logEl.innerHTML = (data.log || []).map(l =>
        `<div class="font-mono text-sm ${l.startsWith('ERROR') ? 'text-error' : 'text-base-content'}">${l}</div>`
      ).join('');
      logEl.scrollTop = logEl.scrollHeight;

      if (data.status === 'done') {
        if (spinner) spinner.classList.add('hidden');
        if (dlBtn)   dlBtn.classList.remove('hidden');
        return;
      }
      if (data.status === 'error') {
        if (spinner) spinner.classList.add('hidden');
        return;
      }

      setTimeout(poll, 4000);
    } catch (e) {
      console.error('Poll error:', e);
      setTimeout(poll, 8000);
    }
  };

  poll();
}
