/* =====================================================
   CONFIGURATION
====================================================== */
const API_BASE = "http://localhost:8000";


/* =====================================================
   APPLICATION STATE
====================================================== */
const state = {
    projects: [],
    currentProject: null,
};


/* =====================================================
   API
====================================================== */
async function api(url, options = {}) {
    console.log(`${API_BASE}${url}`)
    const response = await fetch(
        `${API_BASE}${url}`,
        {
            headers: {
                "Accept": "application/json",
                ...(options.body &&
                    !(options.body instanceof FormData)
                    ? { "Content-Type": "application/json" }
                    : {})
            },
            ...options
        }
    );

    if (!response.ok) {

        let message;
        const rawText = response.text()

        try {
            const data = JSON.parse(rawText)// await response.json();
            message =
                data.detail ||
                data.message ||
                JSON.stringify(data);
        }
        catch {
            message = await rawText;//response.text();
        }

        throw new Error(
            `${response.status}: ${message}`
        );
    }

    if (response.status === 204) {
        return null;
    }

    const contentType = response.headers.get("content-type") || "";

    if (contentType.includes("application/json")) {
        return response.json();
    }

    return response;
}


/* =====================================================
   PROJECTS
====================================================== */

async function loadProjects() {
    try {
        state.projects = await api("/projects");
        renderProjects();
    }
    catch (error) {
        showError(error);
    }
}


function renderProjects() {
    const container = document.getElementById("projectList");

    container.innerHTML = "";

    if (!state.projects.length) {
        container.innerHTML = `
                <div style="
                    padding:10px;
                    color:#6b7280;
                    font-size:13px;
                ">
                    Nenhum projeto.
                </div>
            `;

        return;
    }
    console.log(state.projects)
    for (const project of state.projects) {
        const button = document.createElement("button");

        button.className = "project-item";

        if (
            state.currentProject &&
            state.currentProject.id === project.id
        ) {
            button.classList.add("active");
        }

        button.textContent = project.name;

        button.onclick = () =>
            selectProject(project);

        container.appendChild(button);
    }
}


async function createProject() {

    const input = document.getElementById("projectName");
    const name = input.value.trim();

    if (!name) {
        return;
    }

    try {

        const project =
            await api("/projects", {
                method: "POST",
                body: JSON.stringify({
                    name
                })
            });

        state.projects.push(project);

        renderProjects();

        closeProjectModal();

        input.value = "";

        selectProject(project);

    }
    catch (error) {

        showError(error);

    }
}


async function deleteProject() {
    if (!state.currentProject) {
        return;
    }

    const confirmed =
        confirm(
            `Excluir o projeto "${state.currentProject.name}"?`
        );

    if (!confirmed) {
        return;
    }

    try {

        await api(
            `/projects/${state.currentProject.id}`,
            {
                method: "DELETE"
            }
        );
        state.currentProject = null;

        await loadProjects();
        showEmptyState();
    }
    catch (error) {
        showError(error);
    }
}


/* =====================================================
   PROJECT SELECTION
====================================================== */

async function selectProject(project) {
    state.currentProject = project;

    renderProjects();

    document.getElementById("emptyState").style.display = "none";
    document.getElementById("projectWorkspace").style.display = "block";
    document.getElementById("pageTitle").textContent = project.name;

    await Promise.all([
        loadFiles(),
        loadRecipe()
    ]);
}


function showEmptyState() {
    document.getElementById("emptyState")
        .style.display = "block";

    document.getElementById("projectWorkspace")
        .style.display = "none";

    document.getElementById("pageTitle")
        .textContent = "Selecione um projeto";
}


/* =====================================================
   FILES
====================================================== */
async function loadFiles() {
    if (!state.currentProject) {
        return;
    }

    try {
        const files =
            await api(`/projects/${state.currentProject.id}/components`);
        console.log(files.files);
        // renderFiles(files.files);
    }
    catch (error) {
        showError(error);
    }
}


function renderFiles(files) {
    const container = document.getElementById("fileList");

    container.innerHTML = "";

    if (!files.length) {
        container.innerHTML = `
                <div class="empty">
                    <strong>Nenhum componente</strong>
                    <span>
                        Adicione os arquivos utilizados pela recipe.
                    </span>
                </div>
            `;

        return;
    }

    for (const file of files) {
        /*
         * Aceita tanto:
         *
         * ["arquivo.md", "imagem.png"]
         *
         * quanto:
         *
         * [
         *   {"filename": "arquivo.md"},
         *   {"name": "imagem.png"}
         * ]
         */

        const filename =
            typeof file === "string"
                ? file
                : (
                    file.filename ||
                    file.name ||
                    file.path
                );

        const row =
            document.createElement("div");

        row.className = "file";

        row.innerHTML = `
                <div>
                    <div class="file-name">
                        ${escapeHtml(filename)}
                    </div>

                    <div class="file-type">
                        ${getExtension(filename)}
                    </div>
                </div>

                <button
                    class="button danger"
                    onclick="deleteFile('${encodeURIComponent(filename)}')"
                >
                    Excluir
                </button>
            `;

        container.appendChild(row);
    }
}


async function uploadFiles() {

    const input =
        document.getElementById("fileInput");

    if (!input.files.length ||
        !state.currentProject) {
        return;
    }

    try {

        for (const file of input.files) {

            const form =
                new FormData();

            form.append(
                "file",
                file
            );

            await api(
                `/projects/${state.currentProject.id}/components`,
                {
                    method: "POST",
                    body: form
                }
            );
        }

        input.value = "";

        await loadFiles();

    }
    catch (error) {

        showError(error);

    }
}


async function deleteFile(filename) {

    if (!state.currentProject) {
        return;
    }

    filename =
        decodeURIComponent(filename);

    if (!confirm(`Excluir "${filename}"?`)) {
        return;
    }

    try {

        await api(
            `/projects/${state.currentProject.id}/components/${encodeURIComponent(filename)}`,
            {
                method: "DELETE"
            }
        );

        await loadFiles();

    }
    catch (error) {

        showError(error);

    }
}


/* =====================================================
   RECIPE
====================================================== */

async function loadRecipe() {
    if (!state.currentProject) {
        return;
    }

    try {
        const recipe =
            await api(`/projects/${state.currentProject.id}/recipe`);

        document.getElementById("recipeEditor")
            .value =
            JSON.stringify(
                recipe,
                null,
                4
            );

    }
    catch (error) {

        showError(error);

    }
}


async function saveRecipe() {

    if (!state.currentProject) {
        return;
    }

    const editor =
        document.getElementById("recipeEditor");

    let recipe;

    try {

        recipe =
            JSON.parse(
                editor.value
            );

    }
    catch {

        setCompileStatus(
            "Recipe inválida: JSON malformado.",
            "error"
        );

        return;
    }

    try {

        await api(
            `/projects/${state.currentProject.id}/recipe`,
            {
                method: "PUT",
                body: JSON.stringify(recipe)
            }
        );

        setCompileStatus(
            "Recipe salva com sucesso.",
            "success"
        );

    }
    catch (error) {

        setCompileStatus(
            error.message,
            "error"
        );
    }
}


/* =====================================================
   COMPILATION
====================================================== */

async function compileProject() {

    if (!state.currentProject) {
        return;
    }

    const targetFormat =
        document.getElementById(
            "targetFormat"
        ).value;

    const variablesEditor =
        document.getElementById(
            "variablesEditor"
        );

    let variables;

    try {

        variables =
            JSON.parse(
                variablesEditor.value || "{}"
            );

    }
    catch {

        setCompileStatus(
            "As variáveis precisam ser um JSON válido.",
            "error"
        );

        return;
    }

    const button =
        document.getElementById(
            "compileButton"
        );

    button.disabled = true;
    button.textContent = "Compilando...";

    setCompileStatus(
        "Executando assembly e compilação...",
        ""
    );

    try {

        const result =
            await api(
                `/projects/${state.currentProject.id}/compile`,
                {
                    method: "POST",

                    body: JSON.stringify({
                        target_format: targetFormat,
                        variables
                    })
                }
            );

        /*
         * Esperado:
         *
         * {
         *   "project_id": "...",
         *   "target_format": "pdf",
         *   "artifact": "document.pdf"
         * }
         */

        const artifact =
            result.artifact;

        const downloadUrl =
            `/api/projects/${encodeURIComponent(
                state.currentProject.id
            )}/artifacts/${encodeURIComponent(
                artifact
            )}`;

        setCompileStatus(
            `Compilação concluída.\n\n` +
            `Formato: ${targetFormat}\n` +
            `Artefato: ${artifact}`,
            "success"
        );

        const status =
            document.getElementById(
                "compileStatus"
            );

        status.innerHTML += `
                <br><br>
                <a
                    href="${downloadUrl}"
                    class="button primary"
                    download
                >
                    Baixar documento
                </a>
            `;

    }
    catch (error) {

        setCompileStatus(
            `Falha na compilação.\n\n${error.message}`,
            "error"
        );

    }
    finally {

        button.disabled = false;
        button.textContent =
            "Compilar documento";

    }
}


/* =====================================================
   UI
====================================================== */

function openProjectModal() {

    document
        .getElementById("projectModal")
        .classList.add("open");

    document
        .getElementById("projectName")
        .focus();
}


function closeProjectModal() {

    document
        .getElementById("projectModal")
        .classList.remove("open");
}


function setCompileStatus(
    message,
    type
) {

    const status =
        document.getElementById(
            "compileStatus"
        );

    status.style.display = "block";

    status.className =
        "compile-status";

    if (type) {
        status.classList.add(type);
    }

    status.textContent =
        message;
}


function showError(error) {

    console.error(error);

    alert(
        error?.message ||
        "Ocorreu um erro."
    );
}


function getExtension(filename) {

    const parts =
        filename.split(".");

    if (parts.length <= 1) {
        return "arquivo";
    }

    return parts
        .pop()
        .toUpperCase();
}


function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


/* =====================================================
   INITIALIZATION
====================================================== */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadProjects();

    }
);
