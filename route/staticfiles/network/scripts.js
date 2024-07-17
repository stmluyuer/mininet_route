document.addEventListener('DOMContentLoaded', (event) => {
    const tabs = document.querySelectorAll('.navbar ul li a');
    tabs.forEach(tab => {
        tab.addEventListener('click', function(event) {
            event.preventDefault();
            document.querySelector('.active').classList.remove('active');
            this.parentElement.classList.add('active');

            const url = this.getAttribute('data-url');
            fetch(url)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newContent = doc.getElementById('content').innerHTML;
                    document.getElementById('content').innerHTML = newContent;
                })
                .catch(error => {
                    console.warn('Error fetching content:', error);
                });
        });
    });
});
