const form = document.getElementById('uploadForm');
const studentTable = document.getElementById('studentTableBody');
const highCard = document.getElementById('highRisk');
const mediumCard = document.getElementById('mediumRisk');
const lowCard = document.getElementById('lowRisk');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);

    try {
        const response = await fetch('/upload', { method: 'POST', body: formData });
        if (!response.ok) throw new Error('Upload failed!');
        const data = await response.json();

        // Reset counts
        let high = 0, medium = 0, low = 0;
        studentTable.innerHTML = '';

        data.forEach(student => {
            const tr = document.createElement('tr');
            tr.className = student.risk_level.toLowerCase();
            tr.innerHTML = `
                <td>${student.StudentID}</td>
                <td>${student.Name}</td>
                <td>${student.risk_level}</td>
                <td>${student.AttendancePct}</td>
                <td>${student.AverageScore}</td>
                <td>${student.FeeOverdue ? 'Pending' : 'Paid'}</td>
            `;
            studentTable.appendChild(tr);

            if(student.risk_level === 'High') high++;
            else if(student.risk_level === 'Medium') medium++;
            else low++;
        });

        highCard.textContent = `High Risk: ${high}`;
        mediumCard.textContent = `Medium Risk: ${medium}`;
        lowCard.textContent = `Low Risk: ${low}`;
    } catch (err) {
        alert(err.message);
    }
});
