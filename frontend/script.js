const API_BASE = "https://capstone-project-psw7.onrender.com";

const taskForm = document.getElementById("task-form");
const taskListEl = document.getElementById("task-list");
const titleInput = document.getElementById("title");
const titleError = document.getElementById("title-error");

let editingTaskId = null;

document.addEventListener("DOMContentLoaded", () => {
  renderFromCache();
  fetchTasksFromBackend();
});

function renderFromCache() {
  const cached = localStorage.getItem("taskflow_tasks");
  if (cached) {
    const tasks = JSON.parse(cached);
    renderTasks(tasks);
  }
}

function saveToCache(tasks) {
  localStorage.setItem("taskflow_tasks", JSON.stringify(tasks));
}

async function fetchTasksFromBackend() {
  try {
    const response = await fetch(`${API_BASE}/tasks`);
    if (!response.ok) throw new Error("Tasks load nahi ho paye");
    const tasks = await response.json();
    renderTasks(tasks);
    saveToCache(tasks);
  } catch (err) {
    console.error("Fetch error:", err);
  }
}

function renderTasks(tasks) {
  taskListEl.innerHTML = "";

  if (tasks.length === 0) {
    const emptyMsg = document.createElement("p");
    emptyMsg.textContent = "Koi task nahi hai. Upar se ek add karo!";
    taskListEl.appendChild(emptyMsg);
    return;
  }

  tasks.forEach((task) => {
    const item = document.createElement("div");
    item.className = "task-item";

    const info = document.createElement("div");
    info.className = "task-info";

    const titleEl = document.createElement("strong");
    titleEl.textContent = task.title;

    const meta = document.createElement("small");
    meta.textContent = `Due: ${task.due_date || "N/A"} | Project #${task.project_id}`;

    const badge = document.createElement("span");
    badge.className = `priority-badge priority-${task.priority}`;
    badge.textContent = task.priority;

    info.appendChild(titleEl);
    info.appendChild(badge);
    info.appendChild(document.createElement("br"));
    info.appendChild(meta);

    const actions = document.createElement("div");
    actions.className = "task-actions";

    const editBtn = document.createElement("button");
    editBtn.className = "edit-btn";
    editBtn.textContent = "Edit";
    editBtn.addEventListener("click", () => startEditTask(task));

    const deleteBtn = document.createElement("button");
    deleteBtn.className = "delete-btn";
    deleteBtn.textContent = "Delete";
    deleteBtn.addEventListener("click", () => deleteTask(task.id));

    actions.appendChild(editBtn);
    actions.appendChild(deleteBtn);

    item.appendChild(info);
    item.appendChild(actions);
    taskListEl.appendChild(item);
  });
}

taskForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const title = titleInput.value.trim();

  if (!title) {
    titleError.textContent = "Title khali nahi ho sakta";
    return;
  }
  titleError.textContent = "";

  const payload = {
    title: title,
    priority: document.getElementById("priority").value,
    due_date: document.getElementById("due_date").value || null,
  };

  try {
    if (editingTaskId) {
      await fetch(`${API_BASE}/tasks/${editingTaskId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      editingTaskId = null;
      taskForm.querySelector("button[type='submit']").textContent = "Add Task";
    } else {
      payload.project_id = Number(document.getElementById("project_id").value);
      await fetch(`${API_BASE}/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    }

    taskForm.reset();
    fetchTasksFromBackend();
  } catch (err) {
    console.error("Save error:", err);
  }
});

function startEditTask(task) {
  editingTaskId = task.id;
  titleInput.value = task.title;
  document.getElementById("priority").value = task.priority;
  document.getElementById("due_date").value = task.due_date || "";
  taskForm.querySelector("button[type='submit']").textContent = "Update Task";
  titleInput.focus();
}

async function deleteTask(taskId) {
  try {
    await fetch(`${API_BASE}/tasks/${taskId}`, { method: "DELETE" });
    fetchTasksFromBackend();
  } catch (err) {
    console.error("Delete error:", err);
  }
}

titleInput.addEventListener("input", () => {
  if (titleInput.value.trim()) {
    titleError.textContent = "";
  }
});