<script>
    import { onMount } from "svelte";

    let visible = false;
    onMount(() => {
        visible = true;
    });

    let estadisticas = [
        {
            label: "Usuarios Totales",
            valor: "1,254",
            icono: "bi-people",
            color: "primary",
        },
        {
            label: "Nutricionistas",
            valor: "42",
            icono: "bi-person-badge",
            color: "success",
        },
        {
            label: "Consultas IA/Hoy",
            valor: "856",
            icono: "bi-robot",
            color: "info",
        },
        {
            label: "Estado BD",
            valor: "Online",
            icono: "bi-database-check",
            color: "dark",
        },
    ];

    let logs = [
        { h: "14:05", msg: "Nuevo registro de usuario: ID 1024", tipo: "info" },
        {
            h: "13:40",
            msg: "Respaldo de base de datos completado",
            tipo: "success",
        },
        {
            h: "12:15",
            msg: "Alerta: Intento de acceso no autorizado IP: 192.168.1.5",
            tipo: "danger",
        },
        {
            h: "11:00",
            msg: "Actualización de microservicio IA exitosa",
            tipo: "warning",
        },
    ];
</script>

<svelte:head>
    <title>NutriScan - Administración</title>
</svelte:head>

<div class="admin-container bg-light py-4 min-vh-100">
    <div class="container">
        <!-- Encabezado -->
        <div
            class="d-flex justify-content-between align-items-center mb-4 {visible
                ? 'fade-in'
                : 'opacity-0'}"
        >
            <div>
                <h2 class="fw-bold mb-0 text-dark">Panel de Control Admin</h2>
                <p class="text-muted small mb-0">
                    Gestión de infraestructura y servicios de NutriScan Pro
                </p>
            </div>
            <div class="d-flex gap-2">
                <button
                    class="btn btn-white border shadow-sm rounded-pill px-3"
                >
                    <i class="bi bi-gear-fill me-2"></i>Ajustes
                </button>
                <a
                    href="/"
                    class="btn btn-outline-danger rounded-pill px-3 fw-bold shadow-sm"
                    aria-label="Cerrar Sesión"
                >
                    <i class="bi bi-box-arrow-right"></i>
                </a>
            </div>
        </div>

        <!-- Métricas Rápidas -->
        <div class="row g-4 mb-5">
            {#each estadisticas as stat, i}
                <div
                    class="col-md-3 {visible ? 'fade-in-up' : 'opacity-0'}"
                    style="animation-delay: {i * 0.1}s"
                >
                    <div
                        class="card border-0 shadow-sm rounded-4 p-3 hover-lift transition-all"
                    >
                        <div class="d-flex align-items-center">
                            <div
                                class="bg-{stat.color} bg-opacity-10 text-{stat.color} rounded-3 p-3 me-3"
                            >
                                <i class="bi {stat.icono} fs-3"></i>
                            </div>
                            <div>
                                <h6 class="text-muted small mb-1">
                                    {stat.label}
                                </h6>
                                <h4 class="fw-bold mb-0">{stat.valor}</h4>
                            </div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>

        <div class="row g-4">
            <!-- Gestión de Usuarios -->
            <div
                class="col-lg-8 {visible ? 'fade-in-up delay-2' : 'opacity-0'}"
            >
                <div
                    class="card border-0 shadow-sm rounded-4 overflow-hidden h-100"
                >
                    <div
                        class="card-header bg-white border-bottom-0 p-4 d-flex justify-content-between align-items-center"
                    >
                        <h5 class="fw-bold mb-0">Control de Usuarios</h5>
                        <div class="input-group w-50">
                            <span class="input-group-text bg-light border-0"
                                ><i class="bi bi-search text-muted"></i></span
                            >
                            <input
                                type="text"
                                class="form-control bg-light border-0 small"
                                placeholder="Buscar ID o Email..."
                            />
                        </div>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover align-middle mb-0">
                                <thead class="bg-light">
                                    <tr>
                                        <th class="ps-4 border-0">Usuario</th>
                                        <th class="border-0">Rol</th>
                                        <th class="border-0">Estado</th>
                                        <th class="border-0">Registro</th>
                                        <th class="border-0 pe-4">Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td class="ps-4">
                                            <div
                                                class="d-flex align-items-center"
                                            >
                                                <div
                                                    class="bg-success rounded-circle p-2 me-2 text-white small"
                                                >
                                                    JD
                                                </div>
                                                <div>
                                                    <div class="fw-bold small">
                                                        Juan Diego
                                                    </div>
                                                    <div
                                                        class="text-muted"
                                                        style="font-size: 0.75rem;"
                                                    >
                                                        juan@app.com
                                                    </div>
                                                </div>
                                            </div>
                                        </td>
                                        <td
                                            ><span
                                                class="badge bg-primary bg-opacity-10 text-primary px-2"
                                                >Paciente</span
                                            ></td
                                        >
                                        <td
                                            ><span
                                                class="badge bg-success rounded-pill px-2"
                                                >Activo</span
                                            ></td
                                        >
                                        <td class="text-muted small"
                                            >01/03/2026</td
                                        >
                                        <td class="pe-4">
                                            <button
                                                class="btn btn-sm btn-light rounded-pill px-3"
                                                aria-label="Editar usuario"
                                                ><i class="bi bi-pencil"
                                                ></i></button
                                            >
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="ps-4">
                                            <div
                                                class="d-flex align-items-center"
                                            >
                                                <div
                                                    class="bg-info rounded-circle p-2 me-2 text-white small"
                                                >
                                                    MG
                                                </div>
                                                <div>
                                                    <div class="fw-bold small">
                                                        Dr. Gomez
                                                    </div>
                                                    <div
                                                        class="text-muted"
                                                        style="font-size: 0.75rem;"
                                                    >
                                                        gomez.nutri@app.com
                                                    </div>
                                                </div>
                                            </div>
                                        </td>
                                        <td
                                            ><span
                                                class="badge bg-info bg-opacity-10 text-info px-2"
                                                >Nutricionista</span
                                            ></td
                                        >
                                        <td
                                            ><span
                                                class="badge bg-success rounded-pill px-2"
                                                >Activo</span
                                            ></td
                                        >
                                        <td class="text-muted small"
                                            >15/02/2026</td
                                        >
                                        <td class="pe-4">
                                            <button
                                                class="btn btn-sm btn-light rounded-pill px-3"
                                                aria-label="Editar nutricionista"
                                                ><i class="bi bi-pencil"
                                                ></i></button
                                            >
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div
                        class="card-footer bg-white border-top-0 p-3 text-center"
                    >
                        <button
                            class="btn btn-link text-success text-decoration-none fw-bold small"
                            >Ver todos los usuarios</button
                        >
                    </div>
                </div>
            </div>

            <!-- Monitor de Sistema -->
            <div
                class="col-lg-4 {visible ? 'fade-in-up delay-3' : 'opacity-0'}"
            >
                <div class="card border-0 shadow-sm rounded-4 h-100">
                    <div class="card-header bg-dark text-white p-4 border-0">
                        <h5 class="fw-bold mb-0">
                            <i class="bi bi-terminal me-2"></i>Monitor de Logs
                        </h5>
                    </div>
                    <div
                        class="card-body p-4 bg-dark text-light font-monospace"
                        style="font-size: 0.8rem;"
                    >
                        {#each logs as log}
                            <div
                                class="mb-3 border-start border-2 border-{log.tipo} ps-3"
                            >
                                <span class="text-white-50">[{log.h}]</span>
                                <span class="text-{log.tipo} ms-1"
                                    >{log.msg}</span
                                >
                            </div>
                        {/each}
                    </div>
                    <div
                        class="card-footer bg-dark border-top border-secondary p-3 text-center"
                    >
                        <button
                            class="btn btn-outline-light btn-sm rounded-pill px-4"
                            >Descargar Informe Mensual</button
                        >
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .admin-container {
        padding-top: 5rem !important;
    }

    .hover-lift {
        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }
    .hover-lift:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05) !important;
    }

    .fade-in {
        animation: fadeIn 0.8s ease forwards;
    }
    .fade-in-up {
        animation: fadeInUp 0.8s ease forwards;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
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

    .delay-2 {
        animation-delay: 0.2s;
    }
    .delay-3 {
        animation-delay: 0.3s;
    }
</style>
