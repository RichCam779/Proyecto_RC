<script>
    import { onMount } from "svelte";

    // Campos sincronizados con la estructura de la base de datos (usuarios)
    let identificacion = "";
    let nombreCompleto = "";
    let email = "";
    let genero = "";
    let pais = "";
    let departamento = "";
    let ciudad = "";
    let password = "";
    let confirmPassword = "";

    // Datos del servicio de ubicaciones
    let ubicacionesTotales = [];
    let paisesDisponibles = [];
    let departamentosDisponibles = [];
    let ciudadesDisponibles = [];

    onMount(async () => {
        try {
            // Intentamos conectar con el servicio externo de geografía
            const response = await fetch(
                "http://localhost:3000/api/ubicaciones",
            );
            if (response.ok) {
                const result = await response.json();
                ubicacionesTotales = result.data;

                // Extraer países únicos
                paisesDisponibles = [
                    ...new Set(ubicacionesTotales.map((u) => u.pais)),
                ].sort();
            }
        } catch (error) {
            console.error(
                "Error al conectar con el servicio de ubicaciones:",
                error,
            );
            // Fallback si el servicio no está corriendo
            paisesDisponibles = ["Colombia", "México", "Argentina"];
        }
    });

    // Reactividad para departamentos cuando cambia el país
    $: if (pais) {
        departamentosDisponibles = [
            ...new Set(
                ubicacionesTotales
                    .filter((u) => u.pais === pais)
                    .map((u) => u.departamento),
            ),
        ].sort();
        departamento = ""; // Resetear selección
        ciudad = "";
    }

    // Reactividad para ciudades cuando cambia el departamento
    $: if (departamento) {
        ciudadesDisponibles = [
            ...new Set(
                ubicacionesTotales
                    .filter(
                        (u) =>
                            u.pais === pais && u.departamento === departamento,
                    )
                    .map((u) => u.ciudad),
            ),
        ].sort();
        ciudad = ""; // Resetear selección
    }

    let fotoArchivo = null;
    let analizandoIA = false;
    let biotipoResultado = "";

    function onFileSelected(e) {
        fotoArchivo = e.target.files[0];
    }

    async function handleRegistro() {
        if (password !== confirmPassword) {
            alert("Las contraseñas no coinciden");
            return;
        }

        analizandoIA = true;

        try {
            // 1. Crear el usuario (Simulación de POST a /usuarios)
            // En una app real, aquí harías el fetch a tu API de usuarios
            const userData = {
                identificacion,
                nombre_completo: nombreCompleto,
                email,
                genero,
                pais,
                departamento,
                ciudad,
                password_hash: password, // Debería ser hashed en el server o aquí
                id_rol: 3, // Paciente
            };

            console.log("Datos listos para el registro:", userData);

            // Simulación de éxito y obtención de ID (Ejemplo: ID 11)
            const userId = 11;

            // 2. Si hay foto, enviarla a la IA para análisis de biótipo
            if (userId && fotoArchivo) {
                const formData = new FormData();
                formData.append("file", fotoArchivo);

                const aiResponse = await fetch(
                    `http://localhost:8000/ai/biotype/${userId}`,
                    {
                        method: "POST",
                        body: formData,
                    },
                );

                if (aiResponse.ok) {
                    const aiResult = await aiResponse.json();
                    biotipoResultado = aiResult.biotipo_detectado;
                    alert(
                        `¡Registro exitoso! La IA ha determinado que tu biótipo es: ${biotipoResultado}`,
                    );
                }
            }

            console.log("Registro completo:", userData);
            window.location.href = "/login";
        } catch (error) {
            console.error("Error en el registro:", error);
            alert("Hubo un error al procesar tu solicitud.");
        } finally {
            analizandoIA = false;
        }
    }
</script>

<svelte:head>
    <title>NutriScan - Crear Cuenta</title>
</svelte:head>

<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-lg-10 col-xl-8">
            <div class="card border-0 shadow-lg mt-3 rounded-4 overflow-hidden">
                <div class="bg-success text-white p-4 text-center">
                    <img
                        src="/favicon.png"
                        alt="Logo"
                        width="60"
                        height="60"
                        class="mb-2 rounded-circle shadow-sm border border-white border-2"
                    />
                    <h2 class="fw-bold mt-2 mb-0">Crea tu cuenta</h2>
                    <p class="text-white-50 mb-0 mt-1">
                        Sincroniza tu salud con nuestra ingeniería nutricional
                    </p>
                </div>

                <div class="card-body p-4 p-md-5">
                    <form on:submit|preventDefault={handleRegistro}>
                        <div class="row g-4">
                            <!-- Datos de Identidad -->
                            <div class="col-md-6">
                                <label
                                    for="identificacion"
                                    class="form-label fw-semibold text-secondary"
                                    >Identificación</label
                                >
                                <div class="input-group">
                                    <span
                                        class="input-group-text bg-light border-end-0"
                                        ><i
                                            class="bi bi-card-heading text-muted"
                                        ></i></span
                                    >
                                    <input
                                        type="text"
                                        class="form-control border-start-0 ps-0"
                                        id="identificacion"
                                        bind:value={identificacion}
                                        placeholder="C.C. / Pasaporte"
                                        required
                                    />
                                </div>
                            </div>

                            <div class="col-md-6">
                                <label
                                    for="nombreCompleto"
                                    class="form-label fw-semibold text-secondary"
                                    >Nombre Completo</label
                                >
                                <div class="input-group">
                                    <span
                                        class="input-group-text bg-light border-end-0"
                                        ><i class="bi bi-person text-muted"
                                        ></i></span
                                    >
                                    <input
                                        type="text"
                                        class="form-control border-start-0 ps-0"
                                        id="nombreCompleto"
                                        bind:value={nombreCompleto}
                                        placeholder="Nombre y Apellidos"
                                        required
                                    />
                                </div>
                            </div>

                            <!-- Contacto y Perfil -->
                            <div class="col-md-6">
                                <label
                                    for="email"
                                    class="form-label fw-semibold text-secondary"
                                    >Correo Electrónico</label
                                >
                                <div class="input-group">
                                    <span
                                        class="input-group-text bg-light border-end-0"
                                        ><i class="bi bi-envelope text-muted"
                                        ></i></span
                                    >
                                    <input
                                        type="email"
                                        class="form-control border-start-0 ps-0"
                                        id="email"
                                        bind:value={email}
                                        placeholder="tucorreo@ejemplo.com"
                                        required
                                    />
                                </div>
                            </div>

                            <div class="col-md-6">
                                <label
                                    for="genero"
                                    class="form-label fw-semibold text-secondary"
                                    >Género</label
                                >
                                <div class="input-group">
                                    <span
                                        class="input-group-text bg-light border-end-0"
                                        ><i
                                            class="bi bi-gender-ambiguous text-muted"
                                        ></i></span
                                    >
                                    <select
                                        class="form-select border-start-0 ps-0"
                                        id="genero"
                                        bind:value={genero}
                                        required
                                    >
                                        <option value="" disabled selected
                                            >Selecciona tu género</option
                                        >
                                        <option value="Masculino"
                                            >Masculino</option
                                        >
                                        <option value="Femenino"
                                            >Femenino</option
                                        >
                                        <option value="Otro">Otro</option>
                                    </select>
                                </div>
                            </div>

                            <!-- Ubicación -->
                            <div class="col-md-4">
                                <label
                                    for="pais"
                                    class="form-label fw-semibold text-secondary"
                                    >País</label
                                >
                                <div class="input-group">
                                    <span
                                        class="input-group-text bg-light border-end-0"
                                        ><i class="bi bi-geo-alt text-muted"
                                        ></i></span
                                    >
                                    <select
                                        class="form-select border-start-0 ps-0"
                                        id="pais"
                                        bind:value={pais}
                                        required
                                    >
                                        <option value="" disabled selected
                                            >Selecciona País</option
                                        >
                                        {#each paisesDisponibles as p}
                                            <option value={p}>{p}</option>
                                        {/each}
                                    </select>
                                </div>
                            </div>

                            <div class="col-md-4">
                                <label
                                    for="departamento"
                                    class="form-label fw-semibold text-secondary"
                                    >Departamento</label
                                >
                                <div class="input-group">
                                    <span
                                        class="input-group-text bg-light border-end-0"
                                        ><i class="bi bi-map text-muted"
                                        ></i></span
                                    >
                                    <select
                                        class="form-select border-start-0 ps-0"
                                        id="departamento"
                                        bind:value={departamento}
                                        required
                                        disabled={!pais}
                                    >
                                        <option value="" disabled selected
                                            >Selecciona Depto</option
                                        >
                                        {#each departamentosDisponibles as d}
                                            <option value={d}>{d}</option>
                                        {/each}
                                    </select>
                                </div>
                            </div>

                            <div class="col-md-4">
                                <label
                                    for="ciudad"
                                    class="form-label fw-semibold text-secondary"
                                    >Ciudad</label
                                >
                                <div class="input-group">
                                    <span
                                        class="input-group-text bg-light border-end-0"
                                        ><i class="bi bi-building text-muted"
                                        ></i></span
                                    >
                                    <select
                                        class="form-select border-start-0 ps-0"
                                        id="ciudad"
                                        bind:value={ciudad}
                                        required
                                        disabled={!departamento}
                                    >
                                        <option value="" disabled selected
                                            >Selecciona Ciudad</option
                                        >
                                        {#each ciudadesDisponibles as c}
                                            <option value={c}>{c}</option>
                                        {/each}
                                    </select>
                                </div>
                            </div>

                            <!-- Seguridad -->
                            <div class="col-md-6">
                                <label
                                    for="password"
                                    class="form-label fw-semibold text-secondary"
                                    >Contraseña</label
                                >
                                <div class="input-group">
                                    <span
                                        class="input-group-text bg-light border-end-0"
                                        ><i class="bi bi-lock text-muted"
                                        ></i></span
                                    >
                                    <input
                                        type="password"
                                        class="form-control border-start-0 ps-0"
                                        id="password"
                                        bind:value={password}
                                        placeholder="Mínimo 8 caracteres"
                                        required
                                    />
                                </div>
                            </div>

                            <div class="col-md-6">
                                <label
                                    for="confirmPassword"
                                    class="form-label fw-semibold text-secondary"
                                    >Confirmar Contraseña</label
                                >
                                <div class="input-group">
                                    <span
                                        class="input-group-text bg-light border-end-0"
                                        ><i class="bi bi-shield-lock text-muted"
                                        ></i></span
                                    >
                                    <input
                                        type="password"
                                        class="form-control border-start-0 ps-0"
                                        id="confirmPassword"
                                        bind:value={confirmPassword}
                                        required
                                    />
                                </div>
                            </div>

                            <!-- Subida de Foto (YOLO Scanning) -->
                            <div class="col-12 mt-4">
                                <label
                                    for="fotoPerfil"
                                    class="form-label fw-bold text-success"
                                    ><i class="bi bi-camera me-2"></i>Foto para
                                    Análisis NutriScan (YOLO Scanning)</label
                                >
                                <div
                                    class="card border-dashed p-4 text-center bg-light rounded-4"
                                >
                                    <input
                                        type="file"
                                        id="fotoPerfil"
                                        class="d-none"
                                        accept="image/*"
                                        on:change={onFileSelected}
                                        required
                                    />
                                    <label
                                        for="fotoPerfil"
                                        class="mb-0 cursor-pointer"
                                    >
                                        <i
                                            class="bi bi-cloud-arrow-up display-5 text-{fotoArchivo
                                                ? 'primary'
                                                : 'success'}"
                                        ></i>
                                        <p class="mb-1 fw-bold mt-2">
                                            {fotoArchivo
                                                ? fotoArchivo.name
                                                : "Sube tu foto aquí"}
                                        </p>
                                        <p class="text-muted small mb-0">
                                            La IA analizará tu biotipo mediante
                                            visión por computadora (YOLOv8).
                                        </p>
                                    </label>
                                </div>
                                <div class="text-center mt-2">
                                    <small class="text-danger fw-semibold"
                                        >* Este campo es obligatorio para el
                                        análisis de salud inicial.</small
                                    >
                                </div>
                            </div>

                            <div class="col-12 mt-4 pt-2">
                                <div class="form-check">
                                    <input
                                        class="form-check-input"
                                        type="checkbox"
                                        value=""
                                        id="terminos"
                                        required
                                    />
                                    <label
                                        class="form-check-label text-muted small"
                                        for="terminos"
                                    >
                                        Acepto los <a
                                            href="/terminos"
                                            class="text-success text-decoration-none"
                                            >Términos de servicio</a
                                        >
                                        y la
                                        <a
                                            href="/privacidad"
                                            class="text-success text-decoration-none"
                                            >Política de privacidad</a
                                        >.
                                    </label>
                                </div>
                            </div>

                            <div class="col-12 mt-4">
                                <button
                                    type="submit"
                                    class="btn btn-success w-100 py-3 fw-bold rounded-3 shadow-sm btn-register"
                                    disabled={analizandoIA}
                                >
                                    {#if analizandoIA}
                                        <span
                                            class="spinner-border spinner-border-sm me-2"
                                        ></span>
                                        Analizando Biotipo con IA...
                                    {:else}
                                        Finalizar Registro y Crear Cuenta
                                    {/if}
                                </button>
                            </div>
                        </div>
                    </form>

                    <div class="text-center mt-4">
                        <p class="text-muted mb-0">
                            ¿Ya tienes una cuenta? <a
                                href="/login"
                                class="text-success fw-bold text-decoration-none"
                                >Inicia sesión</a
                            >
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .btn-register {
        transition: all 0.3s ease;
    }
    .btn-register:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(25, 135, 84, 0.3) !important;
    }

    .form-control:focus,
    .input-group-text {
        border-color: #198754;
    }
    .form-control:focus {
        box-shadow: none;
    }
    .input-group-text:has(+ .form-control:focus) {
        border-color: #198754;
    }
</style>
