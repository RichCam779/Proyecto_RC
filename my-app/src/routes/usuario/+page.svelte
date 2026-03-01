<script>
    // Estado simulado para la UI
    let caloriasConsumidas = 1200;
    let caloriasMeta = 2000;
    let porcentaje = Math.min(
        100,
        Math.round((caloriasConsumidas / caloriasMeta) * 100),
    );

    let comidas = [
        { id: 1, nombre: "Desayuno", calorias: 450, completado: true },
        { id: 2, nombre: "Almuerzo", calorias: 750, completado: true },
        { id: 3, nombre: "Cena", calorias: 0, completado: false },
    ];

    let chatMensajes = [
        {
            emisor: "ia",
            texto: "¡Hola! Soy tu asistente virtual. He notado que te falta registrar tu cena para hoy. ¿En qué te puedo ayudar?",
            tiempo: "10:30 AM",
        },
    ];
    let nuevoMensaje = "";

    function enviarMensaje() {
        if (nuevoMensaje.trim() !== "") {
            chatMensajes = [
                ...chatMensajes,
                {
                    emisor: "usuario",
                    texto: nuevoMensaje,
                    tiempo: new Date().toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                    }),
                },
            ];
            nuevoMensaje = "";

            // Simulamos respuesta
            setTimeout(() => {
                chatMensajes = [
                    ...chatMensajes,
                    {
                        emisor: "ia",
                        texto: "Entiendo. Recuerda que es importante mantener el balance. Sugiero una cena ligera de aproximadamente 800 calorías.",
                        tiempo: new Date().toLocaleTimeString([], {
                            hour: "2-digit",
                            minute: "2-digit",
                        }),
                    },
                ];
            }, 1000);
        }
    }
</script>

<svelte:head>
    <title>NutriScan - Mi Panel</title>
</svelte:head>

<div class="container-fluid bg-light py-4 min-vh-100">
    <div class="container">
        <!-- Encabezado del Panel con Cerrar Sesión -->
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-bold mb-0 text-dark">Mi Panel de Salud</h2>
            <a
                href="/"
                class="btn btn-outline-danger rounded-pill px-4 fw-bold shadow-sm"
            >
                <i class="bi bi-box-arrow-right me-2"></i>Cerrar Sesión
            </a>
        </div>

        <!-- Mensaje Nutricionista -->
        <div
            class="alert alert-success border-0 shadow-sm d-flex align-items-center mb-4 rounded-4"
            role="alert"
        >
            <i class="bi bi-chat-quote-fill fs-3 me-3 text-success"></i>
            <div>
                <h5 class="alert-heading fw-bold mb-1">
                    Mensaje de tu Nutricionista (Dr. Gomez)
                </h5>
                <p class="mb-0 text-dark">
                    "¡Excelente progreso esta semana! Recuerda aumentar un poco
                    la ingesta de agua durante la tarde. Sigue así."
                </p>
            </div>
        </div>

        <div class="row g-4">
            <!-- Columna Izquierda: Calorías y Comidas -->
            <div class="col-lg-5">
                <!-- Tarjeta de Calorías -->
                <div
                    class="card border-0 shadow-sm rounded-4 mb-4 overflow-hidden"
                >
                    <div class="card-body p-4 text-center">
                        <h5 class="card-title fw-bold text-secondary mb-4">
                            Progreso Diario
                        </h5>

                        <div class="position-relative d-inline-block mb-3">
                            <!-- Círculo de progreso simulado con SVG -->
                            <svg width="180" height="180" viewBox="0 0 100 100">
                                <circle
                                    cx="50"
                                    cy="50"
                                    r="45"
                                    fill="none"
                                    stroke="#e9ecef"
                                    stroke-width="10"
                                />
                                <circle
                                    cx="50"
                                    cy="50"
                                    r="45"
                                    fill="none"
                                    stroke="#198754"
                                    stroke-width="10"
                                    stroke-dasharray="{porcentaje * 2.83} 283"
                                    stroke-dashoffset="0"
                                    transform="rotate(-90 50 50)"
                                    style="transition: stroke-dasharray 1s ease-out;"
                                />
                            </svg>
                            <div
                                class="position-absolute top-50 start-50 translate-middle text-center w-100"
                            >
                                <h2 class="fw-bold mb-0 text-dark">
                                    {caloriasConsumidas}
                                </h2>
                                <small class="text-muted d-block mt-n1"
                                    >/ {caloriasMeta} kcal</small
                                >
                            </div>
                        </div>

                        <p class="text-muted fw-semibold mb-0 mt-2">
                            {porcentaje}% de tu meta diaria
                        </p>
                    </div>
                </div>

                <!-- Registro de Comidas -->
                <div class="card border-0 shadow-sm rounded-4">
                    <div
                        class="card-header bg-white border-bottom-0 pt-4 pb-0 px-4 d-flex justify-content-between align-items-center"
                    >
                        <h5 class="fw-bold text-secondary mb-0">
                            Registro de Comidas
                        </h5>
                        <button
                            class="btn btn-sm btn-outline-success rounded-pill px-3"
                            ><i class="bi bi-plus-lg me-1"></i>Añadir</button
                        >
                    </div>
                    <div class="card-body p-4">
                        <ul class="list-group list-group-flush border-0">
                            {#each comidas as comida}
                                <li
                                    class="list-group-item d-flex justify-content-between align-items-center px-0 py-3 border-bottom border-light"
                                >
                                    <div class="d-flex align-items-center">
                                        <div
                                            class="rounded-circle bg-{comida.completado
                                                ? 'success'
                                                : 'light'} bg-opacity-10 text-{comida.completado
                                                ? 'success'
                                                : 'secondary'} d-flex align-items-center justify-content-center p-2 me-3"
                                            style="width: 40px; height: 40px;"
                                        >
                                            <i
                                                class="bi bi-{comida.completado
                                                    ? 'check2'
                                                    : 'clock'} fs-5"
                                            ></i>
                                        </div>
                                        <div>
                                            <h6 class="mb-0 fw-bold">
                                                {comida.nombre}
                                            </h6>
                                            {#if comida.completado}
                                                <small
                                                    class="text-success fw-semibold"
                                                    >{comida.calorias} kcal</small
                                                >
                                            {:else}
                                                <small
                                                    class="text-muted fst-italic"
                                                    >Pendiente</small
                                                >
                                            {/if}
                                        </div>
                                    </div>
                                    <button
                                        class="btn btn-sm btn-light text-primary rounded-circle"
                                        ><i class="bi bi-pencil"></i></button
                                    >
                                </li>
                            {/each}
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Columna Derecha: Chatbot -->
            <div class="col-lg-7">
                <div
                    class="card border-0 shadow-sm rounded-4 h-100 d-flex flex-column wrapper-chat"
                >
                    <!-- Cabecera de Chat -->
                    <div
                        class="card-header bg-dark text-white p-3 rounded-top-4 d-flex align-items-center shadow-sm z-1"
                    >
                        <div class="position-relative me-3">
                            <div
                                class="bg-success rounded-circle d-flex align-items-center justify-content-center"
                                style="width: 45px; height: 45px;"
                            >
                                <i class="bi bi-robot fs-4"></i>
                            </div>
                            <span
                                class="position-absolute bottom-0 end-0 bg-light border border-dark rounded-circle text-center d-flex align-items-center justify-content-center"
                                style="width: 15px; height: 15px; margin-right: -2px; margin-bottom: -2px;"
                            >
                                <span
                                    class="bg-success rounded-circle"
                                    style="width: 8px; height: 8px;"
                                ></span>
                            </span>
                        </div>
                        <div>
                            <h5 class="mb-0 fw-bold">NutriBot AI</h5>
                            <small class="text-light text-opacity-75"
                                >En línea</small
                            >
                        </div>
                    </div>

                    <!-- Aviso Legal -->
                    <div
                        class="bg-warning bg-opacity-10 text-warning px-3 py-2 text-center text-sm border-bottom z-0"
                    >
                        <i class="bi bi-info-circle-fill me-1"></i>
                        <span class="fw-semibold">Aviso importante:</span> Su chat
                        con la IA será supervisado por un nutricionista certificado.
                    </div>

                    <!-- Cuerpo del Chat -->
                    <div
                        class="card-body bg-light overflow-auto p-4 flex-grow-1"
                        id="chatContainer"
                    >
                        {#each chatMensajes as msj}
                            {#if msj.emisor === "ia"}
                                <div class="d-flex mb-4">
                                    <div
                                        class="flex-shrink-0 me-3 mt-1 text-center"
                                    >
                                        <i
                                            class="bi bi-robot text-secondary fs-4"
                                        ></i>
                                    </div>
                                    <div>
                                        <div
                                            class="bg-white p-3 rounded-4 shadow-sm text-dark d-inline-block position-relative chat-bubble-ia"
                                        >
                                            {msj.texto}
                                        </div>
                                        <div class="text-muted small mt-1 ms-2">
                                            {msj.tiempo}
                                        </div>
                                    </div>
                                </div>
                            {:else}
                                <div class="d-flex mb-4 flex-row-reverse">
                                    <div
                                        class="flex-shrink-0 ms-3 mt-1 text-center"
                                    >
                                        <div
                                            class="bg-success text-white rounded-circle d-flex align-items-center justify-content-center"
                                            style="width: 35px; height: 35px;"
                                        >
                                            TU
                                        </div>
                                    </div>
                                    <div class="text-end">
                                        <div
                                            class="bg-success text-white p-3 rounded-4 shadow-sm d-inline-block text-start position-relative chat-bubble-user"
                                        >
                                            {msj.texto}
                                        </div>
                                        <div class="text-muted small mt-1 me-2">
                                            {msj.tiempo}
                                        </div>
                                    </div>
                                </div>
                            {/if}
                        {/each}
                    </div>

                    <!-- Input del Chat -->
                    <div
                        class="card-footer bg-white p-3 rounded-bottom-4 border-top-0 border-top mt-auto z-1"
                    >
                        <form
                            class="input-group"
                            on:submit|preventDefault={enviarMensaje}
                        >
                            <input
                                type="text"
                                class="form-control form-control-lg border-0 bg-light rounded-start-pill ps-4"
                                placeholder="Escribe tu mensaje aquí..."
                                bind:value={nuevoMensaje}
                            />
                            <button
                                class="btn btn-success btn-lg rounded-end-pill px-4"
                                type="submit"
                            >
                                <i class="bi bi-send-fill"></i>
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .wrapper-chat {
        min-height: 600px;
    }

    .chat-bubble-ia {
        border-top-left-radius: 0 !important;
    }

    .chat-bubble-user {
        border-top-right-radius: 0 !important;
    }

    .form-control:focus {
        box-shadow: none;
        background-color: #f8f9fa !important;
    }
</style>
