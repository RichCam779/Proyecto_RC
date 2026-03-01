<script>
    import { onMount } from "svelte";

    // Animación simple para los elementos al cargar
    let visible = false;
    onMount(() => {
        visible = true;
    });
</script>

<svelte:head>
    <title>NutriScan Pro - Acerca de Nosotros</title>
</svelte:head>

<div class="acerca-container bg-light py-5">
    <div class="container py-lg-5">
        <!-- Título Principal -->
        <div class="text-center mb-5 {visible ? 'fade-in-up' : 'opacity-0'}">
            <img
                src="/favicon.png"
                alt="NutriScan Logo"
                width="100"
                height="100"
                class="mb-4 rounded-circle shadow-sm border border-success border-2"
            />
            <h1 class="display-3 fw-bold text-dark">
                NutriScan <span class="text-success">Pro</span>
            </h1>
            <p class="lead text-muted fs-3 fw-light">
                Revolucionando tu bienestar con datos e Inteligencia Artificial
            </p>
            <div
                class="mx-auto bg-success"
                style="width: 80px; height: 4px; border-radius: 2px;"
            ></div>
        </div>

        <!-- Introducción (El Propósito) -->
        <div class="row justify-content-center mb-5">
            <div
                class="col-lg-10 {visible ? 'fade-in-up delay-1' : 'opacity-0'}"
            >
                <div
                    class="card border-0 shadow-sm rounded-4 p-4 p-md-5 bg-white overflow-hidden position-relative"
                >
                    <div class="position-absolute top-0 end-0 p-4 opacity-10">
                        <i class="bi bi-quote display-1 text-success"></i>
                    </div>
                    <h2
                        class="fw-bold mb-4 text-success border-start border-4 border-success ps-3"
                    >
                        Nuestra Visión
                    </h2>
                    <p class="fs-5 text-secondary lh-lg mb-0 text-justify">
                        "En <strong>NutriScan Pro</strong>, creemos que alcanzar
                        tus metas de salud no debería ser un proceso genérico ni
                        confuso. Nacimos con la visión de democratizar el acceso
                        a la nutrición personalizada, combinando el rigor del
                        análisis clínico con la velocidad y precisión de la
                        Inteligencia Artificial de vanguardia. No somos solo un
                        contador de calorías; somos tu ecosistema integral de
                        salud."
                    </p>
                </div>
            </div>
        </div>

        <!-- Nuestros Pilares -->
        <h2
            class="text-center fw-bold mb-5 {visible
                ? 'fade-in-up delay-2'
                : 'opacity-0'}"
        >
            Nuestros Pilares Tecnológicos
        </h2>
        <div class="row g-4 mb-5">
            <div
                class="col-md-4 {visible ? 'fade-in-up delay-2' : 'opacity-0'}"
            >
                <div
                    class="card h-100 border-0 shadow-sm rounded-4 text-center p-4 p-lg-5 hover-lift transition-all"
                >
                    <div
                        class="feature-icon-circle bg-success bg-opacity-10 text-success rounded-circle mx-auto mb-4 d-flex align-items-center justify-content-center"
                        style="width: 80px; height: 80px;"
                    >
                        <i class="bi bi-cpu fs-1"></i>
                    </div>
                    <h4 class="fw-bold mb-3">Inteligencia Artificial Ética</h4>
                    <p class="text-muted mb-0">
                        Nuestro motor de IA no solo analiza tu consumo, sino que
                        aprende de tu biotipo y tus interacciones en el chat
                        para ofrecerte respuestas supervisadas, contextuales y
                        seguras.
                    </p>
                </div>
            </div>
            <div
                class="col-md-4 {visible ? 'fade-in-up delay-3' : 'opacity-0'}"
            >
                <div
                    class="card h-100 border-0 shadow-sm rounded-4 text-center p-4 p-lg-5 hover-lift transition-all"
                >
                    <div
                        class="feature-icon-circle bg-primary bg-opacity-10 text-primary rounded-circle mx-auto mb-4 d-flex align-items-center justify-content-center"
                        style="width: 80px; height: 80px;"
                    >
                        <i class="bi bi-clipboard-pulse fs-1"></i>
                    </div>
                    <h4 class="fw-bold mb-3">Rigor Clínico y Seguimiento</h4>
                    <p class="text-muted mb-0">
                        Pasamos de la teoría a la práctica. Conectamos tus
                        perfiles de salud directamente con bases de datos
                        nutricionales para que cada gramo registrado cuente
                        hacia tu meta real.
                    </p>
                </div>
            </div>
            <div
                class="col-md-4 {visible ? 'fade-in-up delay-4' : 'opacity-0'}"
            >
                <div
                    class="card h-100 border-0 shadow-sm rounded-4 text-center p-4 p-lg-5 hover-lift transition-all"
                >
                    <div
                        class="feature-icon-circle bg-dark bg-opacity-10 text-dark rounded-circle mx-auto mb-4 d-flex align-items-center justify-content-center"
                        style="width: 80px; height: 80px;"
                    >
                        <i class="bi bi-shield-lock-fill fs-1"></i>
                    </div>
                    <h4 class="fw-bold mb-3">Arquitectura Segura</h4>
                    <p class="text-muted mb-0">
                        Diseñados bajo estrictos estándares de ingeniería
                        telemática, garantizamos que tu información personal,
                        médica y de consumo esté protegida en sistemas
                        descentralizados.
                    </p>
                </div>
            </div>
        </div>

        <!-- El Equipo / El Proyecto -->
        <div class="row justify-content-center mb-5">
            <div
                class="col-lg-10 {visible ? 'fade-in-up delay-5' : 'opacity-0'}"
            >
                <div class="card border-0 shadow rounded-4 overflow-hidden">
                    <div class="row g-0 align-items-center">
                        <div
                            class="col-md-5 bg-dark p-5 text-center text-white d-flex flex-column justify-content-center h-100 min-vh-25"
                        >
                            <i
                                class="bi bi-code-square display-2 text-success mb-3"
                            ></i>
                            <h3 class="fw-bold">Ingeniería de Software</h3>
                            <p class="text-white-50 small mb-0">
                                Arquitectura de Microservicios & IA Generativa
                            </p>
                        </div>
                        <div class="col-md-7 p-4 p-md-5 bg-white">
                            <h3 class="fw-bold mb-4">El Proyecto</h3>
                            <p class="text-secondary lh-lg mb-4 text-justify">
                                "<strong>NutriScan Pro</strong> fue concebido y desarrollado
                                como un Proyecto Integrador de alto nivel. Nuestro
                                equipo de desarrollo ha fusionado arquitecturas de
                                microservicios, bases de datos relacionales complejas
                                y modelos de IA generativa para crear una solución
                                de software escalable. Nuestra pasión es demostrar
                                cómo la tecnología bien aplicada puede tener un impacto
                                directo y positivo en la vida diaria de las personas."
                            </p>
                            <div class="d-flex align-items-center gap-2">
                                <span
                                    class="badge bg-success bg-opacity-10 text-success px-3 py-2 rounded-pill"
                                    >SvelteKit</span
                                >
                                <span
                                    class="badge bg-primary bg-opacity-10 text-primary px-3 py-2 rounded-pill"
                                    >Node.js</span
                                >
                                <span
                                    class="badge bg-dark bg-opacity-10 text-dark px-3 py-2 rounded-pill"
                                    >PostgreSQL</span
                                >
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- CTA Final -->
        <div
            class="text-center mt-5 {visible
                ? 'fade-in-up delay-6'
                : 'opacity-0'}"
        >
            <h3 class="fw-bold mb-4">¿Listo para transformar tu salud?</h3>
            <div class="d-flex justify-content-center gap-3 flex-wrap">
                <a
                    href="/registro"
                    class="btn btn-success btn-lg px-5 py-3 rounded-pill shadow-lg hover-scale fw-bold"
                >
                    Empieza a cuidar tu salud hoy
                </a>
                <a
                    href="/"
                    class="btn btn-outline-secondary btn-lg px-4 py-3 rounded-pill hover-scale"
                >
                    Volver al Inicio
                </a>
            </div>
        </div>
    </div>
</div>

<style>
    .acerca-container {
        min-height: calc(100vh - 80px);
    }

    .hover-lift {
        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease;
    }

    .hover-lift:hover {
        transform: translateY(-10px);
        box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.1) !important;
    }

    .fade-in-up {
        animation: fadeInUp 0.8s ease forwards;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .delay-1 {
        animation-delay: 0.1s;
    }
    .delay-2 {
        animation-delay: 0.2s;
    }
    .delay-3 {
        animation-delay: 0.3s;
    }
    .delay-4 {
        animation-delay: 0.4s;
    }
    .delay-5 {
        animation-delay: 0.5s;
    }
    .delay-6 {
        animation-delay: 0.6s;
    }

    .transition-all {
        transition: all 0.3s ease;
    }

    .text-justify {
        text-align: justify;
    }
</style>
