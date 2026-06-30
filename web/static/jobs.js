/* BookForge AI — Jobs Dashboard auto-refresh */
(function () {
  const STATUS_COLORS = {
    queued: 'badge-neutral',
    generating: 'badge-warning',
    running: 'badge-warning',
    converting: 'badge-warning',
    done: 'badge-success',
    error: 'badge-error',
    failed: 'badge-error',
  };

  function progressHtml(prog) {
    if (!prog || !prog.total) return '<span class="text-xs opacity-40">-</span>';
    return `
      <div class="flex items-center gap-2">
        <progress class="progress progress-primary w-20" value="${prog.done}" max="${prog.total}"></progress>
        <span class="text-xs">${prog.done}/${prog.total}</span>
      </div>`;
  }

  function actionsHtml(job) {
    let html = `<a href="/job/${job.id}" class="btn btn-xs btn-ghost">Detail</a>`;
    if (job.status === 'done') {
      if (job.is_batch) {
        html += `<a href="/download/zip/${job.id}" class="btn btn-xs btn-success">↯ ZIP</a>`;
      } else {
        html += `<a href="/download/${job.id}" class="btn btn-xs btn-success">↯ EPUB</a>`;
      }
    }
    return html;
  }

  async function refresh() {
    try {
      const res = await fetch('/api/jobs');
      if (!res.ok) return;
      const jobs = await res.json();
      const tbody = document.getElementById('jobs-tbody');
      if (!tbody) return;

      if (!jobs.length) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center opacity-40 py-8">No jobs yet.</td></tr>';
        return;
      }

      // Update existing rows or insert new ones
      const existingIds = new Set([...tbody.querySelectorAll('tr[data-job-id]')].map(r => r.dataset.jobId));

      // Reverse for newest-first display
      [...jobs].reverse().forEach(job => {
        const color = STATUS_COLORS[job.status] || 'badge-neutral';
        const typeLabel = job.is_batch
          ? '<span class="badge badge-outline badge-sm">Batch</span>'
          : '<span class="badge badge-outline badge-sm badge-primary">Single</span>';

        if (existingIds.has(job.id)) {
          const row = tbody.querySelector(`tr[data-job-id="${job.id}"]`);
          if (row) {
            row.querySelector('td:nth-child(5)').innerHTML = progressHtml(job.progress);
            row.querySelector('td:nth-child(6)').innerHTML = `<span class="badge ${color}">${job.status}</span>`;
            row.querySelector('td:nth-child(7)').innerHTML = actionsHtml(job);
          }
        } else {
          const tr = document.createElement('tr');
          tr.dataset.jobId = job.id;
          tr.setAttribute('id', `row-${job.id}`);
          tr.innerHTML = `
            <td class="font-mono text-xs opacity-60">${job.id}</td>
            <td class="max-w-xs truncate font-semibold">${job.title}</td>
            <td>${typeLabel}</td>
            <td class="text-sm opacity-70">${job.provider || '-'}</td>
            <td>${progressHtml(job.progress)}</td>
            <td><span class="badge ${color}">${job.status}</span></td>
            <td class="space-x-1">${actionsHtml(job)}</td>`;
          tbody.prepend(tr);
        }
      });
    } catch (e) {
      console.warn('Jobs refresh failed:', e);
    }
  }

  refresh();
  setInterval(refresh, 5000);
})();
