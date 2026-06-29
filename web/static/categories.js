// BookForge AI — Categories page helpers

document.addEventListener('DOMContentLoaded', () => {
  // Select All / None buttons
  const checkboxes = document.querySelectorAll('input[name="genre_ids"]');

  window.selectAllGenres = () => checkboxes.forEach(cb => cb.checked = true);
  window.selectNoneGenres = () => checkboxes.forEach(cb => cb.checked = false);

  // Warn if submitting batch with 0 genres selected
  const batchForm = document.querySelector('form[action="/batch"]');
  if (batchForm) {
    batchForm.addEventListener('submit', (e) => {
      const selected = [...checkboxes].filter(cb => cb.checked);
      if (selected.length === 0) {
        e.preventDefault();
        alert('Please select at least one genre.');
      }
    });
  }

  // Pre-select genre from URL param
  const params = new URLSearchParams(window.location.search);
  const preGenre = params.get('genre');
  if (preGenre) {
    const cb = document.querySelector(`input[value="${preGenre}"]`);
    if (cb) cb.checked = true;
  }
});
