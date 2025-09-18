document.addEventListener('DOMContentLoaded', function() {
	const form = document.getElementById('uploadForm');
	const studentTable = document.getElementById('studentTableBody');

	if (form) {
		form.addEventListener('submit', async (e) => {
			e.preventDefault();
			const formData = new FormData(form);

			try {
				const response = await fetch('/', { method: 'POST', body: formData });
				if (!response.ok) throw new Error('Upload failed!');
				const html = await response.text();
				// Replace the body with the new HTML (simple way)
				document.body.innerHTML = html;
			} catch (err) {
				alert(err.message);
			}
		});
	}
});
