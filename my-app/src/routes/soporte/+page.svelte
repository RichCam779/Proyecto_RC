<script>
    import { onMount } from "svelte";

    let visible = false;
    onMount(() => {
        visible = true;
    });

    let faqActive = null;
    function toggleFaq(index) {
        faqActive = faqActive === index ? null : index;
    }

    const faqs = [
        {
            q: "¿Por qué no puedo actualizar mi ubicación (País/Ciudad)?",
            a: "Nuestra plataforma se conecta a un microservicio geográfico en tiempo real para garantizar datos precisos. Si experimentas demoras, verifica tu conexión a internet e inténtalo de nuevo en unos segundos.",
        },
        {
            q: "¿Cómo protege NutriScan mis datos médicos y contraseñas?",
            a: "Utilizamos encriptación avanzada de contraseñas (Hash) y mantenemos tu información de salud estrictamente aislada bajo un modelo de arquitectura segura para garantizar tu privacidad.",
        },
        {
            q: "La IA me dio un biotipo con el que no estoy de acuerdo, ¿qué hago?",
            a: "La IA asigna un nivel de confianza a cada evaluación. Si consideras que el resultado requiere ajuste, puedes solicitar una revisión manual desde la sección de tu perfil enviando una solicitud a tu nutricionista.",
        },
    ];
</script>

<svelte:head>
    <title>NutriScan - Soporte Técnico</title>
</svelte:head>

<div class="support-container bg-light py-5">
    <div class="container py-lg-5">
        <!-- Encabezado -->
        <div class="text-center mb-5 {visible ? 'fade-in-up' : 'opacity-0'}">
            <div
                class="d-inline-flex align-items-center justify-content-center bg-success bg-opacity-10 text-success rounded-circle p-3 mb-4"
                style="width: 80px; height: 80px;"
            >
                <i class="bi bi-headset fs-1"></i>
            </div>
            <h1 class="display-4 fw-bold text-dark">
                Centro de Soporte Técnico y Asistencia
            </h1>
            <p class="lead text-muted mx-auto px-2" style="max-width: 800px;">
                "¿Tienes problemas con el escaneo de alimentos, dudas sobre el
                análisis de la IA o inconvenientes con tu cuenta? El equipo de
                ingeniería de NutriScan está aquí para garantizar que tu
                experiencia sea fluida y sin interrupciones."
            </p>
        </div>

        <!-- Opciones de Contacto -->
        <div class="row g-4 mb-5 justify-content-center">
            <!-- Bloque Correo -->
            <div
                class="col-md-5 {visible ? 'fade-in-up delay-1' : 'opacity-0'}"
            >
                <div
                    class="card h-100 border-0 shadow-sm rounded-4 p-4 text-center hover-lift transition-all"
                >
                    <div
                        class="bg-primary bg-opacity-10 text-primary rounded-circle mx-auto mb-4 d-flex align-items-center justify-content-center"
                        style="width: 70px; height: 70px;"
                    >
                        <i class="bi bi-envelope-fill fs-2"></i>
                    </div>
                    <h5 class="fw-bold mb-3">Correo Técnicos</h5>
                    <p class="text-muted small mb-4 px-2">
                        Escríbenos detallando tu problema. Incluye tu correo de
                        registro para una atención más rápida.
                    </p>
                    <a
                        href="mailto:soporte.nutriscan@itsa.edu.co"
                        class="btn btn-primary btn-sm rounded-pill px-3 fw-bold"
                        >soporte.nutriscan@itsa.edu.co</a
                    >
                </div>
            </div>

            <!-- Bloque DevOps -->
            <div
                class="col-md-5 {visible ? 'fade-in-up delay-2' : 'opacity-0'}"
            >
                <div
                    class="card h-100 border-0 shadow-sm rounded-4 p-4 text-center hover-lift transition-all"
                >
                    <div
                        class="bg-dark bg-opacity-10 text-dark rounded-circle mx-auto mb-4 d-flex align-items-center justify-content-center"
                        style="width: 70px; height: 70px;"
                    >
                        <i class="bi bi-github fs-2"></i>
                    </div>
                    <h5 class="fw-bold mb-3">Reporte de Errores</h5>
                    <p class="text-muted small mb-4 px-2">
                        ¿Encontraste un comportamiento inusual? Ayúdanos a
                        mejorar reportando el bug directamente en DevOps.
                    </p>
                    <button
                        class="btn btn-dark btn-sm rounded-pill px-3 fw-bold"
                        on:click={() =>
                            alert(
                                "Abriendo repositorio de GitHub del Proyecto Integrador...",
                            )}>Reportar Issue</button
                    >
                </div>
            </div>
        </div>

        <!-- Preguntas Frecuentes -->
        <div
            class="row justify-content-center {visible
                ? 'fade-in-up delay-4'
                : 'opacity-0'}"
        >
            <div class="col-lg-8">
                <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
                    <div class="card-header bg-white border-0 p-4">
                        <h4 class="fw-bold mb-0">
                            <i class="bi bi-patch-question me-2 text-success"
                            ></i>Preguntas Frecuentes (FAQ)
                        </h4>
                    </div>
                    <div class="accordion accordion-flush" id="faqAccordion">
                        {#each faqs as faq, i}
                            <div class="accordion-item border-bottom">
                                <h2 class="accordion-header">
                                    <button
                                        class="accordion-button {faqActive === i
                                            ? ''
                                            : 'collapsed'} fw-semibold py-3"
                                        type="button"
                                        on:click={() => toggleFaq(i)}
                                    >
                                        {faq.q}
                                    </button>
                                </h2>
                                <div
                                    class="accordion-collapse collapse {faqActive ===
                                    i
                                        ? 'show'
                                        : ''}"
                                >
                                    <div
                                        class="accordion-body text-secondary lh-lg py-4"
                                    >
                                        {faq.a}
                                    </div>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .support-container {
        min-height: calc(100vh - 80px);
    }

    .hover-lift {
        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease;
    }

    .hover-lift:hover {
        transform: translateY(-5px);
        box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.08) !important;
    }

    .fade-in-up {
        animation: fadeInUp 0.8s ease forwards;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
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
    .delay-4 {
        animation-delay: 0.4s;
    }

    .accordion-button:not(.collapsed) {
        background-color: #f8f9fa;
        color: #198754;
        box-shadow: none;
    }

    .accordion-button:focus {
        box-shadow: none;
        border-color: rgba(0, 0, 0, 0.125);
    }
</style>
