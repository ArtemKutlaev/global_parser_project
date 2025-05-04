const filter = document.getElementById('filter');

filter.addEventListener('change', async function() {
    const value = filter.value;

    try {
        const response = await fetch('/parser', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ value: value })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const html = await response.text();

        document.body.innerHTML = html;

    } catch (error) {
        console.error('Error sending data:', error);
    }
});