let BASE_URL = '';

fetch('/static/config.json')
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error al cargar config.json: ${response.statusText}`);
        }
        return response.json();
    })
    .then(config => {
        BASE_URL = config.baseUrl;
        setupEventListeners();
    })
    .catch(error => {
        console.error('Error cargando config.json:', error);
    });

const questionForm = document.querySelector('form [name="question"]').closest('form');
const solutionForm = document.querySelector('form [name="solution"]').closest('form');
const responseElement = document.querySelector('.post-desc');

questionForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío normal del formulario

    const questionInput = questionForm.querySelector('input[name="question"]').value;
    const selectElement = document.getElementById("card-select");
    const id = parseInt(selectElement.value, 10);
    responseElement.textContent = "Cargando...";

    if (questionInput) {
        fetch(`${BASE_URL}/question/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: questionInput, story_id: id})
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
    const selectElement = document.getElementById("card-select");
    const id = parseInt(selectElement.value, 10);
    responseElement.textContent = "Cargando...";

    if (solutionInput) {
        fetch(`${BASE_URL}/response/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ proposal: solutionInput, story_id: id})
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
