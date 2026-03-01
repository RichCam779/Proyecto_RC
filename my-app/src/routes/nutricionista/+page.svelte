<script>
    // Mock datos de conversaciones y pacientes
    let pacientes = [
        {
            id: 1,
            nombre: "Carlos Sánchez",
            fecha: "2026-03-01",
            ultimaInteraccion: "10:30 AM",
            estado: "Revisar",
        },
        {
            id: 2,
            nombre: "María López",
            fecha: "2026-02-28",
            ultimaInteraccion: "08:15 PM",
            estado: "Al día",
        },
        {
            id: 3,
            nombre: "Juan Pérez",
            fecha: "2026-02-28",
            ultimaInteraccion: "02:40 PM",
            estado: "Atención Requerida",
        },
    ];

    let mensajeMotivacional = "";
    let pacienteSeleccionado = null;

    function seleccionarPaciente(p) {
        pacienteSeleccionado = p;
    }

    function enviarMensaje() {
        if (mensajeMotivacional.trim() !== "" && pacienteSeleccionado) {
            alert(
                `Mensaje enviado a ${pacienteSeleccionado.nombre}: "${mensajeMotivacional}"`,
            );
            mensajeMotivacional = "";
        }
    }
</script>

<svelte:head>
    <title>NutriScan - Panel de Nutricionista</title>
</svelte:head>

<div class="container-fluid bg-light py-4 min-vh-100">
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h2 class="fw-bold mb-0 text-dark">Portal Profesional</h2>
                <p class="text-muted">
                    Supervisión de interacciones IA y gestión de pacientes
                </p>
            </div>
            <div class="d-flex align-items-center gap-3">
                <div
                    class="d-flex align-items-center bg-white px-4 py-2 rounded-pill shadow-sm"
                >
                    <div
                        class="bg-success rounded-circle me-3 mt-1"
                        style="width: 40px; height: 40px; background-image: url('https://ui-avatars.com/api/?name=Dr+Gomez&background=198754&color=fff'); background-size: cover;"
                    ></div>
                    <div>
                        <h6 class="mb-0 fw-bold">Dr. Gomez</h6>
                        <small class="text-success fw-semibold"
                            ><i
                                class="bi bi-circle-fill me-1"
                                style="font-size: 8px;"
                            ></i>En línea</small
                        >
                    </div>
                </div>
                <a
                    href="/"
                    class="btn btn-outline-danger rounded-pill px-3 fw-bold shadow-sm"
                    aria-label="Cerrar Sesión"
                >
                    <i class="bi bi-box-arrow-right"></i>
                </a>
            </div>
        </div>

        <div class="row g-4">
            <!-- Lista de Pacientes -->
            <div class="col-lg-4">
                <div
                    class="card border-0 shadow-sm rounded-4 h-100 overflow-hidden"
                >
                    <div
                        class="card-header bg-dark text-white p-3 border-bottom-0"
                    >
                        <h5 class="mb-0 fw-bold">
                            <i class="bi bi-people-fill me-2"></i>Pacientes
                            Activos
                        </h5>
                    </div>
                    <div class="card-body p-0">
                        <div class="list-group list-group-flush">
                            {#each pacientes as paciente}
                                <button
                                    type="button"
                                    class="list-group-item list-group-item-action p-4 border-bottom border-light {pacienteSeleccionado?.id ===
                                    paciente.id
                                        ? 'bg-success bg-opacity-10 border-start border-4 border-success'
                                        : ''}"
                                    on:click={() =>
                                        seleccionarPaciente(paciente)}
                                >
                                    <div
                                        class="d-flex w-100 justify-content-between align-items-center mb-1"
                                    >
                                        <h6 class="mb-0 fw-bold">
                                            {paciente.nombre}
                                        </h6>
                                        <small class="text-muted"
                                            >{paciente.fecha}</small
                                        >
                                    </div>
                                    <div
                                        class="d-flex justify-content-between align-items-center mt-2"
                                    >
                                        <small class="text-muted"
                                            ><i class="bi bi-clock me-1"
                                            ></i>Último chat: {paciente.ultimaInteraccion}</small
                                        >
                                        <span
                                            class="badge rounded-pill {paciente.estado ===
                                            'Revisar'
                                                ? 'bg-warning text-dark'
                                                : paciente.estado ===
                                                    'Atención Requerida'
                                                  ? 'bg-danger'
                                                  : 'bg-success'}"
                                            >{paciente.estado}</span
                                        >
                                    </div>
                                </button>
                            {/each}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Panel Principal (Chat y Mensajes) -->
            <div class="col-lg-8">
                {#if pacienteSeleccionado}
                    <div class="card border-0 shadow-sm rounded-4 mb-4">
                        <div
                            class="card-header bg-white p-4 border-bottom border-light d-flex justify-content-between align-items-center"
                        >
                            <div>
                                <h5 class="fw-bold mb-1">
                                    Conversación: {pacienteSeleccionado.nombre} y
                                    NutriBot
                                </h5>
                                <p class="text-muted small mb-0">
                                    Fecha de revisión: {pacienteSeleccionado.fecha}
                                </p>
                            </div>
                            <button
                                class="btn btn-outline-secondary btn-sm"
                                aria-label="Exportar Historial"
                                ><i class="bi bi-download me-1"></i>Exportar
                                Historial</button
                            >
                        </div>

                        <!-- Simulación de Historial de Chat -->
                        <div
                            class="card-body bg-light p-4"
                            style="height: 300px; overflow-y: auto;"
                        >
                            <div class="text-center mb-4">
                                <span
                                    class="badge bg-secondary rounded-pill px-3 py-2 fw-normal"
                                    >Inicio de la conversación - {pacienteSeleccionado.ultimaInteraccion}</span
                                >
                            </div>

                            <div class="d-flex mb-4">
                                <div class="flex-shrink-0 me-3">
                                    <div
                                        class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center"
                                        style="width: 35px; height: 35px;"
                                    >
                                        PT
                                    </div>
                                </div>
                                <div>
                                    <div
                                        class="bg-white p-3 rounded-4 shadow-sm text-dark d-inline-block border"
                                    >
                                        Hola IA, hoy comí 2 rebanadas de pizza
                                        en el almuerzo, ¿eso está muy mal?
                                    </div>
                                </div>
                            </div>

                            <div class="d-flex mb-4 flex-row-reverse">
                                <div class="flex-shrink-0 ms-3">
                                    <div
                                        class="bg-dark text-white rounded-circle d-flex align-items-center justify-content-center"
                                        style="width: 35px; height: 35px;"
                                    >
                                        <i class="bi bi-robot"></i>
                                    </div>
                                </div>
                                <div class="text-end">
                                    <div
                                        class="bg-white p-3 rounded-4 shadow-sm text-dark d-inline-block text-start border"
                                    >
                                        Hola {pacienteSeleccionado.nombre.split(
                                            " ",
                                        )[0]}. No está mal ocasionalmente. Dos
                                        rebanadas de pizza promedian unas
                                        500-600 kcal. Sugiero que tu cena sea
                                        rica en fibra y vegetales para
                                        compensar. ¿Qué planeas cenar?
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Enviar Mensaje Motivacional -->
                    <div
                        class="card border-0 shadow-sm rounded-4 border-start border-4 border-success"
                    >
                        <div class="card-body p-4">
                            <h5 class="fw-bold mb-3">
                                <i
                                    class="bi bi-chat-heart-fill text-success me-2"
                                ></i>Enviar Mensaje al Paciente
                            </h5>
                            <p class="text-muted small mb-3">
                                Este mensaje aparecerá destacado en el panel
                                principal del usuario.
                            </p>

                            <form on:submit|preventDefault={enviarMensaje}>
                                <div class="mb-3">
                                    <textarea
                                        class="form-control bg-light border-0"
                                        rows="3"
                                        placeholder="Escribe un mensaje de apoyo, recomendación o ajuste a su dieta..."
                                        bind:value={mensajeMotivacional}
                                        required
                                    ></textarea>
                                </div>
                                <div class="text-end">
                                    <button
                                        type="submit"
                                        class="btn btn-success px-4 rounded-pill fw-semibold shadow-sm"
                                    >
                                        <i class="bi bi-send me-2"></i>Enviar
                                        Mensaje
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                {:else}
                    <div
                        class="card border-0 shadow-sm rounded-4 h-100 d-flex align-items-center justify-content-center text-center p-5 bg-white"
                    >
                        <div class="text-muted opacity-50 mb-3">
                            <i class="bi bi-inboxes display-1"></i>
                        </div>
                        <h4 class="fw-bold text-secondary">
                            Selecciona un paciente
                        </h4>
                        <p class="text-muted max-w-sm mx-auto">
                            Haz clic en un paciente de la lista a la izquierda
                            para revisar sus interacciones con la IA e impartir
                            recomendaciones.
                        </p>
                    </div>
                {/if}
            </div>
        </div>
    </div>
</div>

<style>
    .list-group-item {
        transition: all 0.2s ease;
    }
    .list-group-item:hover {
        background-color: #f8f9fa;
    }
    textarea:focus {
        box-shadow: none;
        border-color: transparent;
        background-color: #fff !important;
        border: 1px solid #198754 !important;
    }
</style>
