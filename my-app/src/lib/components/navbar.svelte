<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
	<div class="container-fluid">
		<a
			class="navbar-brand fw-bold text-success d-flex align-items-center"
			href="/"
		>
			<img
				src="/favicon.png"
				alt="Logo"
				width="40"
				height="40"
				class="me-2 rounded-circle shadow-sm"
			/>NutriScan
		</a>
		<button
			class="navbar-toggler"
			type="button"
			data-bs-toggle="collapse"
			data-bs-target="#navbarNav"
			aria-controls="navbarNav"
			aria-expanded="false"
			aria-label="Toggle navigation"
		>
			<span class="navbar-toggler-icon"></span>
		</button>
		<div class="collapse navbar-collapse" id="navbarNav">
			<ul class="navbar-nav ms-auto fw-semibold">
				<li class="nav-item">
					<a class="nav-link" href="/acerca">Acerca de</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="/soporte">Soporte Técnico</a>
				</li>
				<li class="nav-item ms-lg-2 mt-2 mt-lg-0">
					<a
						class="btn btn-outline-success rounded-pill px-4 fw-bold shadow-sm transition-all"
						href="/login"
					>
						<i class="bi bi-person-circle me-2"></i>Iniciar sesión
					</a>
				</li>
			</ul>
		</div>
	</div>
</nav>

<style>
	.navbar {
		box-shadow:
			0 4px 6px -1px rgba(0, 0, 0, 0.1),
			0 2px 4px -1px rgba(0, 0, 0, 0.06);
		padding-top: 1rem;
		padding-bottom: 1rem;
	}
	.navbar-brand {
		font-size: 1.5rem;
		letter-spacing: -0.5px;
	}
</style>
