<script>
    // Aquí en el futuro se manejará la autenticación
</script>

<svelte:head>
    <title>NutriScan - Iniciar Sesión</title>
</svelte:head>

<div
    class="d-flex align-items-center justify-content-center py-5"
    style="min-height: calc(100vh - 200px);"
>
    <div
        class="card border-0 shadow-lg rounded-4 overflow-hidden"
        style="max-width: 900px; width: 100%;"
    >
        <div class="row g-0">
            <!-- Sección de la imagen / Hero lateral -->
            <div
                class="col-md-5 bg-success d-none d-md-flex align-items-center justify-content-center p-5 text-white login-sidebar"
            >
                <div class="text-center z-1 position-relative">
                    <img
                        src="/favicon.png"
                        alt="Logo"
                        width="80"
                        height="80"
                        class="mb-4 rounded-circle shadow border border-white border-2"
                    />
                    <h2 class="fw-bold mb-3">¡Bienvenido!</h2>
                    <p class="lead">
                        Accede a tu cuenta de NutriScan y continúa tu camino
                        hacia una vida más saludable.
                    </p>
                </div>
                <div
                    class="position-absolute w-100 h-100 top-0 start-0 z-0 bg-pattern opacity-25"
                ></div>
            </div>

            <!-- Sección del formulario -->
            <div class="col-md-7 p-sm-5 p-4 bg-white">
                <div class="text-center mb-4 d-md-none">
                    <img
                        src="/favicon.png"
                        alt="Logo"
                        width="60"
                        height="60"
                        class="rounded-circle shadow-sm"
                    />
                </div>
                <h3 class="fw-bold mb-1 text-center text-md-start">
                    Iniciar Sesión
                </h3>
                <p class="text-muted mb-4 text-center text-md-start">
                    Accede a tu panel personalizado.
                </p>

                <form>
                    <div class="form-floating mb-3">
                        <input
                            type="email"
                            class="form-control rounded-3"
                            id="floatingInput"
                            placeholder="nombre@ejemplo.com"
                        />
                        <label for="floatingInput">Correo Electrónico</label>
                    </div>
                    <div class="form-floating mb-4">
                        <input
                            type="password"
                            class="form-control rounded-3"
                            id="floatingPassword"
                            placeholder="Contraseña"
                        />
                        <label for="floatingPassword">Contraseña</label>
                    </div>

                    <div
                        class="d-flex justify-content-between align-items-center mb-4"
                    >
                        <div class="form-check">
                            <input
                                class="form-check-input"
                                type="checkbox"
                                value=""
                                id="rememberMe"
                            />
                            <label
                                class="form-check-label text-muted"
                                for="rememberMe"
                            >
                                Recordarme
                            </label>
                        </div>
                        <a
                            href="/soporte"
                            class="text-success text-decoration-none fw-semibold"
                            >¿Olvidaste tu contraseña?</a
                        >
                    </div>

                    <a
                        href="/usuario"
                        class="btn btn-success w-100 py-3 rounded-3 fw-bold mb-4 shadow-sm btn-login"
                    >
                        Ingresar a mi cuenta
                    </a>

                    <div class="text-center text-muted">
                        ¿No tienes una cuenta? <a
                            href="/registro"
                            class="text-success text-decoration-none fw-bold"
                            >Regístrate aquí</a
                        >
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<style>
    .btn-login {
        transition: all 0.3s ease;
    }
    .btn-login:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(25, 135, 84, 0.3) !important;
    }

    .login-sidebar {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #198754 0%, #146c43 100%);
    }

    .form-control:focus {
        border-color: #198754;
        box-shadow: 0 0 0 0.25rem rgba(25, 135, 84, 0.25);
    }
</style>
