const questionForm = document.querySelector('form [name="question"]').closest('form');
const solutionForm = document.querySelector('form [name="solution"]').closest('form');
const responseElement = document.querySelector('.post-desc');

questionForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío normal del formulario

    const questionInput = questionForm.querySelector('input[name="question"]').value;

    if (questionInput) {
        fetch('http://127.0.0.1:8000/generate_response/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ input: questionInput })
        })
        .then(response => response.json())
        .then(data => {
            responseElement.textContent = data.response; // Muestra la respuesta de la API
        })
        .catch(error => {
            console.error('Error:', error);
            responseElement.textContent = "Error al obtener la respuesta";
        });
    } else {
        responseElement.textContent = "";
    }
});

solutionForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío normal del formulario

    const solutionInput = solutionForm.querySelector('input[name="solution"]').value;

    if (solutionInput) {
        fetch('http://127.0.0.1:8000/generate_response/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ input: solutionInput })
        })
        .then(response => response.json())
        .then(data => {
            responseElement.textContent = data.response; // Muestra la respuesta de la API
        })
        .catch(error => {
            console.error('Error:', error);
            responseElement.textContent = "Error al obtener la respuesta";
        });
    } else {
        responseElement.textContent = "";
    }
});
