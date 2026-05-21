const subjectSelect = document.getElementById("subjectSelect");
const topicSelect = document.getElementById("topicSelect");
const loadQuestionsBtn = document.getElementById("loadQuestionsBtn");
const questionsList = document.getElementById("questionsList");
const generateExamBtn = document.getElementById("generateExamBtn");
const examPreview = document.getElementById("examPreview");

let allQuestions = [];
let selectedQuestions = new Set();

async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function loadSubjects() {
  const subjects = await fetchJSON(`${API_BASE}/subjects`);
  subjects.forEach(subj => {
    const opt = document.createElement("option");
    opt.value = subj;
    opt.textContent = subj;
    subjectSelect.appendChild(opt);
  });
}

async function loadTopics() {
  topicSelect.innerHTML = '<option value="">--Select--</option>';
  const subj = subjectSelect.value;
  if (!subj) return;
  const topics = await fetchJSON(`${API_BASE}/topics?subject=${encodeURIComponent(subj)}`);
  topics.forEach(topic => {
    const opt = document.createElement("option");
    opt.value = topic;
    opt.textContent = topic;
    topicSelect.appendChild(opt);
  });
}

async function loadQuestions() {
  const subj = subjectSelect.value;
  const topic = topicSelect.value;
  let url = `${API_BASE}/questions`;
  const params = [];
  if (subj) params.push(`subject=${encodeURIComponent(subj)}`);
  if (topic) params.push(`topic=${encodeURIComponent(topic)}`);
  if (params.length) url += "?" + params.join("&");

  allQuestions = await fetchJSON(url);
  renderQuestions();
}

function renderQuestions() {
  questionsList.innerHTML = "";
  selectedQuestions.clear();
  allQuestions.forEach(q => {
    const div = document.createElement("div");
    div.className = "question-item";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.addEventListener("change", () => {
      if (checkbox.checked) selectedQuestions.add(q.id);
      else selectedQuestions.delete(q.id);
    });

    const label = document.createElement("span");
    label.textContent = q.text;

    div.appendChild(checkbox);
    div.appendChild(label);
    questionsList.appendChild(div);
  });
}

function generateExam() {
  const chosen = allQuestions.filter(q => selectedQuestions.has(q.id));
  let text = "";
  chosen.forEach((q, idx) => {
    text += `${idx + 1}. ${q.text}\n\n`;
  });
  examPreview.textContent = text || "No questions selected.";
}

subjectSelect.addEventListener("change", loadTopics);
loadQuestionsBtn.addEventListener("click", loadQuestions);
generateExamBtn.addEventListener("click", generateExam);

// Initial load
loadSubjects().catch(err => console.error(err));