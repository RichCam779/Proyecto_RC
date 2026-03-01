<footer class="footer bg-dark text-light pt-5 pb-3">
    <div class="container py-4">
        <div class="row g-4 mb-4">
            <!-- Columna 1: Marca y Misión -->
            <div class="col-lg-4 col-md-12">
                <div class="d-flex align-items-center mb-3">
                    <img
                        src="/favicon.png"
                        alt="Logo NutriScan"
                        width="35"
                        height="35"
                        class="me-2 rounded-circle"
                    />
                    <h5 class="fw-bold text-success mb-0">
                        NutriScan <span class="text-white">Pro</span>
                    </h5>
                </div>
                <p class="text-white-50 lh-lg" style="max-width: 320px;">
                    Transformando la nutrición a través de la Inteligencia
                    Artificial y el análisis de datos. Tu salud, respaldada por
                    la tecnología.
                </p>
                <div class="d-flex gap-3 mt-4">
                    <a
                        href="/"
                        class="text-white-50 hover-success transition-all fs-5"
                        aria-label="Facebook"><i class="bi bi-facebook"></i></a
                    >
                    <a
                        href="/"
                        class="text-white-50 hover-success transition-all fs-5"
                        aria-label="Instagram"
                        ><i class="bi bi-instagram"></i></a
                    >
                    <a
                        href="/"
                        class="text-white-50 hover-success transition-all fs-5"
                        aria-label="LinkedIn"><i class="bi bi-linkedin"></i></a
                    >
                    <a
                        href="/"
                        class="text-white-50 hover-success transition-all fs-5"
                        aria-label="Twitter X"
                        ><i class="bi bi-twitter-x"></i></a
                    >
                </div>
            </div>

            <!-- Columna 2: Navegación Rápida -->
            <div class="col-lg-2 col-md-4 col-6 ms-lg-auto">
                <h6 class="fw-bold text-white mb-4">Enlaces Útiles</h6>
                <ul class="list-unstyled">
                    <li class="mb-2">
                        <a
                            href="/"
                            class="text-white-50 text-decoration-none hover-success transition-all small"
                            >Inicio</a
                        >
                    </li>
                    <li class="mb-2">
                        <a
                            href="/acerca"
                            class="text-white-50 text-decoration-none hover-success transition-all small"
                            >Acerca de nosotros</a
                        >
                    </li>
                    <li class="mb-2">
                        <a
                            href="/soporte"
                            class="text-white-50 text-decoration-none hover-success transition-all small"
                            >Soporte Técnico</a
                        >
                    </li>
                </ul>
            </div>

            <!-- Columna 3: Tecnología y Confianza -->
            <div class="col-lg-4 col-md-8 col-6">
                <h6 class="fw-bold text-white mb-4">Desarrollado con</h6>
                <div class="d-flex flex-wrap gap-2 mb-4">
                    <span
                        class="badge bg-secondary bg-opacity-25 text-white-50 fw-normal rounded-pill px-3 py-2 small border border-secondary border-opacity-25"
                        >Python (FastAPI)</span
                    >
                    <span
                        class="badge bg-secondary bg-opacity-25 text-white-50 fw-normal rounded-pill px-3 py-2 small border border-secondary border-opacity-25"
                        >Node.js</span
                    >
                    <span
                        class="badge bg-secondary bg-opacity-25 text-white-50 fw-normal rounded-pill px-3 py-2 small border border-secondary border-opacity-25"
                        >SvelteKit</span
                    >
                    <span
                        class="badge bg-secondary bg-opacity-25 text-white-50 fw-normal rounded-pill px-3 py-2 small border border-secondary border-opacity-25"
                        >PostgreSQL</span
                    >
                </div>
                <div class="d-flex align-items-center">
                    <div class="status-indicator me-2 pulsate-green"></div>
                    <span class="text-white-50 small"
                        >Estado del Sistema:
                    </span>
                    <span class="text-success small fw-bold ms-1"
                        >Operacional</span
                    >
                </div>
            </div>
        </div>

        <hr class="border-secondary opacity-25 my-4" />

        <!-- Barra Inferior -->
        <div class="row align-items-center">
            <div class="col-md-6 text-center text-md-start">
                <p class="text-white-50 small mb-0">
                    &copy; 2026 NutriScan Pro. Todos los derechos reservados.
                </p>
            </div>
            <div class="col-md-6 text-center text-md-end mt-3 mt-md-0">
                <p class="text-white-50 small mb-0">
                    Proyecto Integrador — Desarrollado por el equipo de
                    tecnología de la <span class="text-success fw-bold"
                        >Institución Universitaria de Barranquilla (IUB)</span
                    >
                </p>
            </div>
        </div>
    </div>
</footer>

<style>
    .footer {
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    .hover-success:hover {
        color: #198754 !important;
        transform: translateY(-2px);
    }

    .transition-all {
        transition: all 0.3s ease;
    }

    .status-indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #198754;
    }

    .pulsate-green {
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(25, 135, 84, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(25, 135, 84, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(25, 135, 84, 0);
        }
    }
</style>
