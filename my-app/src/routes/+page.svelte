<script>
    // No necesitamos importar Navbar ni Footer aquí porque ya están en +layout.svelte
</script>

<svelte:head>
    <title>NutriScan - Inicio</title>
</svelte:head>

<div
    class="hero-section bg-dark text-white text-center py-5 position-relative overflow-hidden shadow-lg"
>
    <div class="container py-4 py-md-5 my-md-5 position-relative z-1">
        <!-- Logo Grande y Centrado -->
        <div class="mb-4 slide-up">
            <img
                src="/favicon.png"
                alt="NutriScan Logo"
                width="180"
                height="180"
                class="img-fluid rounded-circle shadow-lg border border-white border-4 mx-auto logo-pulse"
                style="max-width: 150px;"
            />
        </div>

        <h1 class="display-3 fw-bold mb-4 slide-up delay-1 text-gradient px-2">
            Transforma tu alimentación sin complicaciones.
        </h1>

        <p
            class="lead mb-5 slide-up delay-2 fw-light fs-4 mx-auto px-3"
            style="max-width: 900px;"
        >
            NutriScan une la tecnología de vanguardia con el rigor profesional.
            Registra tu consumo diario, resuelve tus dudas al instante y toma el
            control de tu salud con datos precisos.
        </p>

        <div
            class="d-flex flex-column flex-sm-row justify-content-center gap-3 slide-up delay-3 mt-4 px-4"
        >
            <a
                href="/registro"
                class="btn btn-success btn-lg px-5 py-3 rounded-pill shadow-lg hover-scale fw-bold"
            >
                Crear mi cuenta
            </a>
            <a
                href="/login"
                class="btn btn-outline-light btn-lg px-5 py-3 rounded-pill hover-scale fw-bold"
            >
                Iniciar sesión
            </a>
        </div>

        <!-- Nueva Sección de Credibilidad -->
        <div class="mt-5 pt-4 slide-up delay-3">
            <p class="text-white-50 small text-uppercase letter-spacing-2 mb-4">
                Avalado por expertos en salud y nutrición
            </p>
            <div
                class="d-flex justify-content-center align-items-center gap-3 gap-md-4 flex-wrap grayscale-icons opacity-75 px-3"
            >
                <span
                    class="badge bg-light text-dark p-2 rounded-3 shadow-sm px-3 fw-bold"
                >
                    SaludCertificada
                </span>
                <span
                    class="badge bg-light text-dark p-2 rounded-3 shadow-sm px-3 fw-bold"
                >
                    NutriPro 2026
                </span>
                <span
                    class="badge bg-light text-dark p-2 rounded-3 shadow-sm px-3 fw-bold"
                >
                    IA-Safe Health
                </span>
            </div>
        </div>
    </div>

    <!-- Elementos de diseño decorativos -->
    <div
        class="position-absolute top-0 start-0 w-100 h-100 overflow-hidden z-0 opacity-25"
    >
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
    </div>
</div>

<div class="container py-5 mt-5">
    <div class="row g-4 text-center">
        <div class="col-md-4">
            <div
                class="card h-100 border-0 shadow-sm feature-card p-4 rounded-4"
            >
                <div class="card-body">
                    <div
                        class="feature-icon bg-success text-white rounded-circle mb-4 mx-auto d-flex align-items-center justify-content-center"
                        style="width: 80px; height: 80px;"
                    >
                        <i class="bi bi-robot fs-1"></i>
                    </div>
                    <h3 class="fw-bold mb-3">IA Avanzada</h3>
                    <p class="text-muted">
                        Chat inteligente que te ayuda a llevar el control de tus
                        calorías y resolver tus dudas nutricionales al instante.
                    </p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div
                class="card h-100 border-0 shadow-sm feature-card p-4 rounded-4"
            >
                <div class="card-body">
                    <div
                        class="feature-icon bg-success text-white rounded-circle mb-4 mx-auto d-flex align-items-center justify-content-center"
                        style="width: 80px; height: 80px;"
                    >
                        <i class="bi bi-shield-check fs-1"></i>
                    </div>
                    <h3 class="fw-bold mb-3">Supervisión Profesional</h3>
                    <p class="text-muted">
                        Todas tus interacciones y progresos son revisados por
                        nutricionistas certificados para garantizar tu
                        bienestar.
                    </p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div
                class="card h-100 border-0 shadow-sm feature-card p-4 rounded-4"
            >
                <div class="card-body">
                    <div
                        class="feature-icon bg-success text-white rounded-circle mb-4 mx-auto d-flex align-items-center justify-content-center"
                        style="width: 80px; height: 80px;"
                    >
                        <i class="bi bi-graph-up fs-1"></i>
                    </div>
                    <h3 class="fw-bold mb-3">Seguimiento Real</h3>
                    <p class="text-muted">
                        Registra tus 3 comidas diarias y visualiza tu progreso
                        calórico con barras dinámicas e intuitivas.
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    /* Animaciones personalizadas */
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .slide-up {
        animation: slideUp 0.8s ease forwards;
    }

    .delay-1 {
        animation-delay: 0.1s;
    }
    .delay-2 {
        animation-delay: 0.3s;
    }
    .delay-3 {
        animation-delay: 0.5s;
    }

    /* Efectos hover */
    .hover-scale {
        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease;
    }
    .hover-scale:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
    }

    .feature-card {
        transition: transform 0.3s ease;
        background: linear-gradient(to bottom, #ffffff, #f8f9fa);
    }
    .feature-card:hover {
        transform: translateY(-10px);
    }

    /* Decoraciones de fondo (Glassmorphism blobs) */
    .hero-section {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }

    .blob {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
    }
    .blob-1 {
        width: 400px;
        height: 400px;
        background: rgba(25, 135, 84, 0.4); /* Bootstrap Success color */
        top: -100px;
        left: -100px;
        animation: float 10s infinite alternate ease-in-out;
    }
    .blob-2 {
        width: 300px;
        height: 300px;
        background: rgba(13, 110, 253, 0.3); /* Bootstrap Primary color */
        bottom: -50px;
        right: 10%;
        animation: float 8s infinite alternate-reverse ease-in-out;
    }

    .text-gradient {
        background: linear-gradient(135deg, #ffffff 0%, #198754 100%);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    @media (max-width: 576px) {
        .display-3 {
            font-size: 2.2rem;
        }
        .lead {
            font-size: 1.1rem !important;
        }
    }

    .logo-pulse {
        animation: pulse 3s infinite ease-in-out;
    }

    @keyframes pulse {
        0% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(25, 135, 84, 0.4);
        }
        70% {
            transform: scale(1.05);
            box-shadow: 0 0 0 20px rgba(25, 135, 84, 0);
        }
        100% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(25, 135, 84, 0);
        }
    }

    .letter-spacing-2 {
        letter-spacing: 2px;
    }

    @keyframes float {
        from {
            transform: translate(0, 0);
        }
        to {
            transform: translate(50px, 50px);
        }
    }
</style>
