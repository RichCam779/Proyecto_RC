<script>
	import Navbar from "$lib/components/Navbar.svelte";
	import Footer from "$lib/components/Footer.svelte";
	let { children } = $props();
</script>

<div class="app-container d-flex flex-column min-vh-100 bg-light">
	<Navbar />

	<main class="flex-grow-1">
		{@render children()}
	</main>

	<Footer />
</div>

<style>
	:global(body) {
		font-family:
			"Inter",
			system-ui,
			-apple-system,
			sans-serif;
	}
	.app-container {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}
</style>
