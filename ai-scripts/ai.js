// import { ChatPromptTemplate } from "@langchain/core/prompts";

// const promptTemplate = ChatPromptTemplate.fromMessages([
//   ["system", "You are a helpful assistant"],
//   ["user", "Tell me a joke about {topic}"],
// ]);

// await promptTemplate.invoke({ topic: "cats" });

const questionForm = document.querySelector('form [name="question"]').closest('form');
const solutionForm = document.querySelector('form [name="solution"]').closest('form');
const responseElement = document.querySelector('.post-desc');

questionForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío normal del formulario

    const questionInput = questionForm.querySelector('input[name="question"]').value;

    if (questionInput) {
        responseElement.textContent = "Miaw";
    } else {
        responseElement.textContent = "";
    }
});

solutionForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío normal del formulario

    const solutionInput = questionForm.querySelector('input[name="solution"]').value;

    if (solutionInput) {
        responseElement.textContent = "Mow";
    } else {
        responseElement.textContent = "";
    }
});