const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const lessonIdInput = document.getElementById('lessonId');
const saveBtn = document.getElementById('saveBtn');
const editBtn = document.getElementById('editBtn');
const fetchBtn = document.getElementById('fetchBtn');
const generateBtn = document.getElementById('generateBtn');
const message = document.getElementById('message');
const loader = document.getElementById('loader');
const report = document.getElementById('report');

let lessonData = null;

generateBtn.disabled = true;

// =========================
// ЗАГРУЗКА СОХРАНЁННЫХ КРЕДОВ
// =========================
window.onload = () => {
  const savedCreds = localStorage.getItem('softiumCreds');
  if (savedCreds) {
    const creds = JSON.parse(savedCreds);
    usernameInput.value = creds.username;
    passwordInput.value = creds.password;
    usernameInput.disabled = true;
    passwordInput.disabled = true;
    saveBtn.style.display = 'none';
    editBtn.style.display = 'block';
  }
};

// =========================
// СОХРАНЕНИЕ КРЕДОВ
// =========================
saveBtn.addEventListener('click', () => {
  const username = usernameInput.value.trim();
  const password = passwordInput.value.trim();
  if (!username || !password) {
    message.style.color = 'red';
    message.innerText = 'Введите логин и пароль!';
    return;
  }
  localStorage.setItem('softiumCreds', JSON.stringify({ username, password }));
  usernameInput.disabled = true;
  passwordInput.disabled = true;
  saveBtn.style.display = 'none';
  editBtn.style.display = 'block';
  message.style.color = 'green';
  message.innerText = 'Креды сохранены!';
});

// =========================
// РЕДАКТИРОВАНИЕ КРЕДОВ
// =========================
editBtn.addEventListener('click', () => {
  usernameInput.disabled = false;
  passwordInput.disabled = false;
  saveBtn.style.display = 'block';
  editBtn.style.display = 'none';
  message.innerText = '';
});

// =========================
// ПОЛУЧЕНИЕ ДАННЫХ УРОКА
// =========================
fetchBtn.addEventListener('click', async () => {
  const savedCreds = JSON.parse(localStorage.getItem('softiumCreds') || '{}');
  const lessonId = lessonIdInput.value.trim();
  if (!savedCreds.username || !savedCreds.password || !lessonId) {
    message.style.color = 'red';
    message.innerText = 'Заполните креды и ID урока!';
    return;
  }

  message.style.color = 'black';
  message.innerText = 'Загрузка данных...';
  loader.style.display = 'block';
  report.innerHTML = '';
  generateBtn.disabled = true;

  try {
    const response = await fetch(`/scraper/get_lesson_data?username=${encodeURIComponent(savedCreds.username)}&password=${encodeURIComponent(savedCreds.password)}&lesson_id=${lessonId}`);
    if (!response.ok) throw new Error(response.statusText);

    lessonData = await response.json();

    if (!lessonData.children || lessonData.children.length === 0) {
      message.style.color = 'red';
      message.innerText = 'Не удалось получить данные об уроке.';
      report.innerHTML = '';
      lessonData = null;
      return;
    }

    displayLessonData(lessonData);

    message.style.color = 'green';
    message.innerText = 'Данные успешно получены!';
    generateBtn.disabled = false;
  } catch (err) {
    message.style.color = 'red';
    message.innerText = `Ошибка: ${err.message}`;
    generateBtn.disabled = true;
  } finally {
    loader.style.display = 'none';
  }
});

// =========================
// ГЕНЕРАЦИЯ ОТЧЁТА
// =========================
generateBtn.addEventListener('click', async () => {
  if (!lessonData) return;

  message.style.color = 'black';
  message.innerText = 'Генерация отчёта...';
  loader.style.display = 'block';
  report.innerHTML = '';

  try {
    const response = await fetch('/reports/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(lessonData),
    });

    if (!response.ok) throw new Error(response.statusText);

    const result = await response.json();

    renderGeneratedReport(result);

    message.style.color = 'green';
    message.innerText = 'Отчёт успешно сгенерирован!';
  } catch (err) {
    message.style.color = 'red';
    message.innerText = `Ошибка при генерации: ${err.message}`;
  } finally {
    loader.style.display = 'none';
  }
});

// =========================
// КРАСИВЫЙ ВЫВОД СГЕНЕРИРОВАННОГО ОТЧЁТА
// =========================
function renderGeneratedReport(result) {
  if (result.status !== "success") {
    report.innerHTML = `<div class="error">Ошибка: ${result.message || 'Неизвестно'}</div>`;
    return;
  }

  const paragraphs = result.report
    .split("\n")
    .filter(p => p.trim())
    .map(p => `<p style="margin-bottom: 12px; line-height: 1.5;">${p}</p>`)
    .join('');

  report.innerHTML = `
    <div style="
      background: #fff;
      border-radius: 8px;
      padding: 15px;
      line-height: 1.6;
      border-left: 4px solid #007BFF;
    ">
      ${paragraphs}
    </div>
  `;
}

// =========================
// КРАСИВОЕ ОТОБРАЖЕНИЕ ДАННЫХ УРОКА
// =========================
function displayLessonData(data) {
  const html = data.children.map(child => {
    const tasksHtml = child.tasks.map(task => `
      <div class="task-card" style="
        background: white;
        padding: 12px;
        margin-top: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
      ">
        <div style="font-weight: bold; margin-bottom: 5px;">${task.name}</div>

        <div style="margin-bottom: 8px;">
          <span style="background:#d1ecf1;color:#0c5460;padding:3px 6px;border-radius:4px;font-size:12px;">
            ${task.direction}
          </span>
          <span style="background:#ffeeba;color:#856404;padding:3px 6px;border-radius:4px;font-size:12px;margin-left:5px;">
            Уровень: ${task.level}
          </span>
          <span style="background:#c3e6cb;color:#155724;padding:3px 6px;border-radius:4px;font-size:12px;margin-left:5px;">
            Награда: ${task.reward}
          </span>
        </div>

        <div style="color:#444; font-size:14px; white-space:pre-wrap;">${task.text}</div>
      </div>
    `).join('');

    return `
      <div class="child-block" style="
        background:#eef1f4;
        padding:15px;
        border-radius:10px;
        margin-bottom:20px;
      ">
        <h3 style="margin-top:0;color:#333;">${child.name}</h3>
        <div style="margin-bottom:10px;color:#555;">Сделано заданий: <strong>${child.done_tasks_count}</strong></div>
        ${tasksHtml}
      </div>
    `;
  }).join('');

  report.innerHTML = html;
}
