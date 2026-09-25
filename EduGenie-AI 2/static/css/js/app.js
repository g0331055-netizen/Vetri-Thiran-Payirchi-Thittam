const form = document.querySelector("#learning-form");
const mode = document.querySelector("#mode");
const prompt = document.querySelector("#prompt");
const promptLabel = document.querySelector("#prompt-label");
const levelField = document.querySelector("#level-field");
const questionCountField = document.querySelector("#question-count-field");
const submit = document.querySelector("#submit");
const status = document.querySelector("#status");
const resultCard = document.querySelector("#result-card");
const resultTitle = document.querySelector("#result-title");
const result = document.querySelector("#result");

const modeLabels = {
	qa: ["Your question", "What would you like to know?"],
	explain: ["Topic to explain", "Enter a topic you want explained."],
	summarize: ["Text to summarize", "Paste the text you want summarized."],
	quiz: ["Quiz topic", "Enter a topic for your quiz."],
	learn: ["Learning topic", "What would you like to learn?"]
};

function updateFields() {
	const [label, placeholder] = modeLabels[mode.value];
	promptLabel.textContent = label;
	prompt.placeholder = placeholder;
	levelField.classList.toggle("hidden", !["explain", "learn"].includes(mode.value));
	questionCountField.classList.toggle("hidden", mode.value !== "quiz");
}

function renderResult(data) {
	result.replaceChildren();
	if (data.result) {
		result.textContent = data.result;
	} else if (data.recommendations) {
		const list = document.createElement("ol");
		data.recommendations.forEach((recommendation) => {
			const item = document.createElement("li");
			item.textContent = recommendation;
			list.appendChild(item);
		});
		result.appendChild(list);
	} else if (data.questions) {
		data.questions.forEach((question, index) => {
			const block = document.createElement("article");
			block.className = "quiz-question";
			block.innerHTML = `<h3>${index + 1}. ${question.question}</h3>`;
			const options = document.createElement("div");
			options.className = "options";
			question.options.forEach((option) => {
				const button = document.createElement("button");
				button.className = "option";
				button.type = "button";
				button.textContent = option;
				button.addEventListener("click", () => {
					button.classList.add(option === question.answer ? "good" : "bad");
				});
				options.appendChild(button);
			});
			block.appendChild(options);
			result.appendChild(block);
		});
	}
	resultCard.classList.remove("hidden");
}

mode.addEventListener("change", updateFields);

form.addEventListener("submit", async (event) => {
	event.preventDefault();
	submit.disabled = true;
	status.textContent = "Thinking...";
	resultCard.classList.add("hidden");

	const selectedMode = mode.value;
	const payload = { text: prompt.value.trim() };
	let endpoint = `/${selectedMode}`;
	if (selectedMode === "explain") payload.level = document.querySelector("#level").value;
	if (selectedMode === "learn") {
		endpoint = "/learn/recommendations";
		payload.topic = payload.text;
		delete payload.text;
		payload.level = document.querySelector("#level").value;
	}
	if (selectedMode === "quiz") payload.num_questions = Number(document.querySelector("#question-count").value);

	try {
		const response = await fetch(endpoint, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(payload)
		});
		const data = await response.json();
		if (!response.ok) throw new Error(data.detail?.[0]?.msg || "The request could not be completed.");
		resultTitle.textContent = selectedMode === "quiz" ? "Your quiz" : "Result";
		renderResult(data);
		status.textContent = "";
	} catch (error) {
		status.textContent = error.message;
		status.className = "status error";
	} finally {
		submit.disabled = false;
	}
});

updateFields();
